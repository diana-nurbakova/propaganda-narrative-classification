import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import DebertaV2PreTrainedModel, DebertaV2Model
import re

def sanitize_name(name):
    """Creates a safe name for dictionary keys. Must be IDENTICAL to the one in preprocessing."""
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.lower()


def sigmoid_focal_loss(logits, targets, alpha=None, gamma=2.0, reduction='mean'):
    """
    Sigmoid focal loss for multi-label classification.

    FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)

    Down-weights easy examples so the model focuses on hard misclassifications.
    With gamma=0, this reduces to standard (weighted) BCE.

    Args:
        logits: Raw logits (before sigmoid), shape [batch, num_labels]
        targets: Binary targets, shape [batch, num_labels]
        alpha: Per-class weight tensor, shape [num_labels].
               Derived from pos_weights as alpha = pw / (1 + pw).
        gamma: Focusing parameter. 0 = standard CE, 2.0 = standard focal.
        reduction: 'mean', 'sum', or 'none'
    """
    probs = torch.sigmoid(logits)

    # Numerically stable BCE via logsigmoid
    bce = -targets * F.logsigmoid(logits) - (1 - targets) * F.logsigmoid(-logits)

    # p_t = p if y=1, (1-p) if y=0
    p_t = probs * targets + (1 - probs) * (1 - targets)

    # Focal modulating factor
    focal_weight = (1 - p_t) ** gamma

    loss = focal_weight * bce

    # Apply alpha weighting for class imbalance
    if alpha is not None:
        alpha_t = alpha * targets + (1 - alpha) * (1 - targets)
        loss = alpha_t * loss

    if reduction == 'mean':
        return loss.mean()
    elif reduction == 'sum':
        return loss.sum()
    return loss


class MultiHeadDebertaForHierarchicalClassification(DebertaV2PreTrainedModel):

    def __init__(self, config, parent_label2id, child_label_maps, pos_weight_dict=None):
        super().__init__(config)

        self.parent_label2id = parent_label2id
        self.child_label_maps = child_label_maps
        self.pos_weight_dict = pos_weight_dict
        self.num_parent_labels = len(parent_label2id)

        self.deberta = DebertaV2Model(config)
        self.dropout = nn.Dropout(0.1)

        self.parent_classifier = nn.Linear(config.hidden_size, self.num_parent_labels)

        self.child_classifiers = nn.ModuleDict()
        for parent_name, child_map in child_label_maps.items():
            num_child_labels = len(child_map['label2id'])
            self.child_classifiers[sanitize_name(parent_name)] = nn.Linear(config.hidden_size, num_child_labels)

        # Precompute focal loss alpha from pos_weights: alpha = pw / (1 + pw)
        self.focal_gamma = 2.0
        self.alpha_dict = {}
        if pos_weight_dict is not None:
            for key, pw in pos_weight_dict.items():
                self.alpha_dict[key] = pw / (1.0 + pw)

        self.post_init()

    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, parent_labels=None, **kwargs):
        outputs = self.deberta(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )

        pooled_output = outputs[0][:, 0]
        pooled_output = self.dropout(pooled_output)

        parent_logits = self.parent_classifier(pooled_output)

        child_logits = {}
        for sanitized_key, child_head in self.child_classifiers.items():
            child_logits[sanitized_key] = child_head(pooled_output)

        loss = None
        if parent_labels is not None:
            total_loss = 0
            device = parent_labels.device

            # Parent loss: focal loss with alpha from capped pos_weights
            parent_alpha = self.alpha_dict.get('parent_labels', None)
            if parent_alpha is not None:
                parent_alpha = parent_alpha.to(device)
            parent_loss = sigmoid_focal_loss(
                parent_logits, parent_labels.float(),
                alpha=parent_alpha, gamma=self.focal_gamma
            )
            total_loss += parent_loss

            # Child losses: only computed on samples where parent is present
            for original_parent_name, child_info in self.child_label_maps.items():
                sanitized_name_key = sanitize_name(original_parent_name)
                child_label_key = f"child_labels_{sanitized_name_key}"

                if child_label_key in kwargs:
                    child_label_tensor = kwargs[child_label_key]

                    parent_id = self.parent_label2id[original_parent_name]
                    parent_mask = parent_labels[:, parent_id] > 0

                    if parent_mask.sum() > 0:
                        active_child_logits = child_logits[sanitized_name_key][parent_mask]
                        active_child_labels = child_label_tensor[parent_mask]

                        child_alpha = self.alpha_dict.get(child_label_key, None)
                        if child_alpha is not None:
                            child_alpha = child_alpha.to(device)

                        child_loss = sigmoid_focal_loss(
                            active_child_logits, active_child_labels.float(),
                            alpha=child_alpha, gamma=self.focal_gamma
                        )
                        total_loss += child_loss

            loss = total_loss

        return {
            "loss": loss,
            "parent_logits": parent_logits,
            "child_logits": child_logits,
        }
