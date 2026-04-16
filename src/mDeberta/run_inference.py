import os
import json
import torch
import re
import argparse
from tqdm import tqdm
from transformers import AutoTokenizer

# Import the custom model class and the utility function
from multihead_deberta import MultiHeadDebertaForHierarchicalClassification, sanitize_name

def run_inference(model_path, input_dir, output_file, mc_dropout=False, seed=None):
    """
    Runs inference on a directory of text files using a trained hierarchical model.

    Args:
        model_path (str): Path to the saved model directory.
        input_dir (str): Path to the directory containing input .txt files.
        output_file (str): Path to the output .tsv file.
        mc_dropout (bool): If True, keep dropout active during inference (MC Dropout)
                           for uncertainty estimation across multiple runs.
        seed (int): Random seed for reproducibility (used with mc_dropout).
    """
    # -------------------------------------------------------------------------
    # 1. Setup and Configuration
    # -------------------------------------------------------------------------
    print("Step 1: Setting up configuration...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # -------------------------------------------------------------------------
    # 2. Load Artifacts (Model, Tokenizer, Mappings, Threshold)
    # -------------------------------------------------------------------------
    print("Step 2: Loading model and artifacts...")

    # Load training configuration to get the best thresholds
    try:
        with open(os.path.join(model_path, 'training_config.json'), 'r') as f:
            training_config = json.load(f)
            parent_threshold = training_config.get('best_parent_threshold',
                                                   training_config.get('best_threshold', 0.5))
            child_threshold = training_config.get('best_child_threshold', parent_threshold)
            max_length = training_config.get('max_length', 512)
            print(f"Loaded thresholds — parent: {parent_threshold:.3f}, child: {child_threshold:.3f}")
            print(f"Max length: {max_length}")
    except (FileNotFoundError, json.JSONDecodeError):
        parent_threshold = 0.5
        child_threshold = 0.5
        max_length = 512
        print("Warning: training_config.json not found or invalid. Using default thresholds of 0.5")

    # Load hierarchical label mappings
    with open(os.path.join(model_path, 'label_mappings_hierarchical.json'), 'r') as f:
        label_mappings = json.load(f)
        parent_label2id = label_mappings['parent_label2id']
        # JSON keys are strings, so convert parent_id back to int for indexing
        parent_id2label = {int(k): v for k, v in label_mappings['parent_id2label'].items()}
        child_label_maps = label_mappings['child_label_maps']
    print("Loaded hierarchical label mappings.")

    # Load tokenizer from base model (tokenizer is unchanged by fine-tuning,
    # and saved tokenizer files may have version-incompatible special_tokens format)
    tokenizer = AutoTokenizer.from_pretrained('microsoft/mdeberta-v3-base')

    # Load model via from_pretrained (handles DeBERTa LayerNorm gamma/beta remapping)
    model = MultiHeadDebertaForHierarchicalClassification.from_pretrained(
        model_path,
        parent_label2id=parent_label2id,
        child_label_maps=child_label_maps
    )
    model.to(device)

    if mc_dropout:
        model.train()  # Keep dropout active for MC Dropout inference
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        print(f"Model loaded in MC Dropout mode (seed={seed}).")
    else:
        model.eval()
        print("Model loaded and set to evaluation mode.")

    # -------------------------------------------------------------------------
    # 3. Find and Process Input Files
    # -------------------------------------------------------------------------
    print("Step 3: Finding and processing input text files...")
    try:
        text_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
        if not text_files:
            print(f"Error: No .txt files found in directory '{input_dir}'")
            return
        print(f"Found {len(text_files)} text files to process.")
    except FileNotFoundError:
        print(f"Error: Input directory not found at '{input_dir}'")
        return

    all_predictions = []
    for filename in tqdm(text_files, desc="Inferring"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        # Tokenize the text for the model
        inputs = tokenizer(
            text,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=max_length
        ).to(device)

        # ---------------------------------------------------------------------
        # 4. Run Inference and Decode Predictions
        # ---------------------------------------------------------------------
        with torch.no_grad(): # Disable gradient calculation for efficiency
            outputs = model(**inputs)

        # Unpack the logits from the model's output dictionary
        parent_logits = outputs['parent_logits']
        child_logits_dict = outputs['child_logits']

        # DEBUG: Print raw probabilities for the first 3 files
        if len(all_predictions) < 3:
            parent_probs_debug = torch.sigmoid(parent_logits).cpu().numpy().flatten()
            print(f"\n[DEBUG] {filename}")
            print(f"  Parent logits (raw): min={parent_logits.min().item():.4f}, max={parent_logits.max().item():.4f}")
            print(f"  Parent probs: min={parent_probs_debug.min():.4f}, max={parent_probs_debug.max():.4f}, mean={parent_probs_debug.mean():.4f}")
            top5_idx = parent_probs_debug.argsort()[-5:][::-1]
            for idx in top5_idx:
                print(f"    {parent_id2label[idx]}: {parent_probs_debug[idx]:.4f}")

        # Get parent predictions using parent threshold
        parent_probs = torch.sigmoid(parent_logits).cpu().numpy().flatten()
        parent_preds_indices = (parent_probs >= parent_threshold).astype(int)

        predicted_parents = []
        predicted_subnarratives = []

        # Loop through parent predictions to decode them
        for i, is_present in enumerate(parent_preds_indices):
            if is_present:
                parent_name = parent_id2label[i]
                predicted_parents.append(parent_name)

                # If a parent is predicted, check for its children
                if parent_name in child_label_maps:
                    safe_key = sanitize_name(parent_name)
                    child_logits = child_logits_dict[safe_key]
                    child_probs = torch.sigmoid(child_logits).cpu().numpy().flatten()
                    child_preds_indices = (child_probs >= child_threshold).astype(int)
                    
                    # Get the specific id->label map for this parent's children
                    child_id2label = child_label_maps[parent_name]['id2label']

                    # Loop through child predictions to decode them
                    for j, child_is_present in enumerate(child_preds_indices):
                        if child_is_present:
                            # JSON keys are strings, so we access with str(j)
                            child_name = child_id2label[str(j)]
                            # child_name already contains the full hierarchical path
                            predicted_subnarratives.append(child_name)

        # Format the predictions into semicolon-separated strings
        if not predicted_parents:
            narratives_str = "Other"
            subnarratives_str = "Other"
        else:
            narratives_str = ";".join(sorted(predicted_parents))
            subnarratives_str = ";".join(sorted(predicted_subnarratives))

        all_predictions.append((filename, narratives_str, subnarratives_str))

    # -------------------------------------------------------------------------
    # 5. Write Output File
    # -------------------------------------------------------------------------
    print(f"Step 4: Writing {len(all_predictions)} predictions to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for filename, narratives, subnarratives in all_predictions:
            f.write(f"{filename}\t{narratives}\t{subnarratives}\n")

    print("Inference complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run inference with a hierarchical text classification model.")
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the directory containing the saved model and artifacts."
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Path to the directory containing the input .txt files."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="predictions.tsv",
        help="Path to the output file where predictions will be saved (default: predictions.tsv)."
    )
    parser.add_argument(
        "--mc-dropout",
        action="store_true",
        help="Enable MC Dropout: keep dropout active during inference for uncertainty estimation."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (used with --mc-dropout)."
    )
    args = parser.parse_args()

    run_inference(args.model_path, args.input_dir, args.output_file,
                  mc_dropout=args.mc_dropout, seed=args.seed)