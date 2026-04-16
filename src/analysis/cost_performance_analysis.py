"""
Cost-Performance Analysis and Visualization.

Creates Pareto curves and comparison tables for ensemble cost-performance tradeoffs.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_metrics(metrics_path: str) -> Dict[str, Any]:
    """Load metrics from JSON file."""
    with open(metrics_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_all_metrics(metrics_dir: str) -> List[Dict[str, Any]]:
    """Load all metrics files from a directory."""
    metrics_dir = Path(metrics_dir)
    metrics = []

    for metrics_file in metrics_dir.glob("**/cost_metrics.json"):
        try:
            data = load_metrics(str(metrics_file))
            data['_source_file'] = str(metrics_file)
            metrics.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {metrics_file}: {e}")

    return metrics


def create_comparison_dataframe(metrics_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a DataFrame for cost-performance comparison.

    Columns: config, model, num_agents, aggregation, validation, retrieval,
             api_calls, cost_usd, latency_sec, f1_samples
    """
    rows = []

    for m in metrics_list:
        num_docs = m.get('total_documents', 1)

        row = {
            'config': m.get('config_name', 'unknown'),
            'model': m.get('model_name', 'unknown').split(':')[-1],
            'experiment_id': m.get('experiment_id', 'unknown'),
            'num_narrative_agents': m.get('num_narrative_agents', 1),
            'num_subnarrative_agents': m.get('num_subnarrative_agents', 1),
            'aggregation': m.get('aggregation_method', 'union'),
            'validation': m.get('enable_validation', False),
            'retrieval': m.get('enable_retrieval', False),
            'total_api_calls': m.get('total_api_calls', 0),
            'total_cost_usd': m.get('total_cost_usd', 0),
            'total_latency_sec': m.get('total_latency_ms', 0) / 1000,
            'avg_latency_sec': (m.get('total_latency_ms', 0) / num_docs / 1000) if num_docs > 0 else 0,
            'avg_cost_usd': (m.get('total_cost_usd', 0) / num_docs) if num_docs > 0 else 0,
            'avg_api_calls': (m.get('total_api_calls', 0) / num_docs) if num_docs > 0 else 0,
            'total_documents': num_docs,
            'f1_samples': m.get('f1_samples'),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def identify_pareto_frontier(df: pd.DataFrame, cost_col: str, f1_col: str) -> pd.DataFrame:
    """
    Identify Pareto-optimal configurations (maximize F1, minimize cost).

    Returns DataFrame with Pareto-optimal points marked.
    """
    df = df.copy()
    df['is_pareto_optimal'] = False

    # Filter to rows with valid F1 scores
    valid_mask = df[f1_col].notna()
    valid_df = df[valid_mask].copy()

    if len(valid_df) == 0:
        return df

    # Sort by cost ascending
    valid_df = valid_df.sort_values(cost_col)

    # Find Pareto frontier
    pareto_indices = []
    max_f1_so_far = -np.inf

    for idx, row in valid_df.iterrows():
        if row[f1_col] > max_f1_so_far:
            pareto_indices.append(idx)
            max_f1_so_far = row[f1_col]

    df.loc[pareto_indices, 'is_pareto_optimal'] = True
    return df


def plot_cost_performance_curve(
    df: pd.DataFrame,
    cost_col: str = 'total_cost_usd',
    f1_col: str = 'f1_samples',
    output_path: Optional[str] = None,
    title: str = "Cost-Performance Tradeoff",
    group_by: str = 'model',
) -> plt.Figure:
    """
    Plot cost vs F1 performance with Pareto frontier.

    Args:
        df: DataFrame with metrics
        cost_col: Column name for cost metric
        f1_col: Column name for F1 score
        output_path: Optional path to save the figure
        title: Plot title
        group_by: Column to use for grouping/coloring points
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Get Pareto frontier
    df = identify_pareto_frontier(df, cost_col, f1_col)

    # Filter to valid F1 scores
    plot_df = df[df[f1_col].notna()].copy()

    if len(plot_df) == 0:
        ax.text(0.5, 0.5, "No valid F1 scores available",
                ha='center', va='center', transform=ax.transAxes)
        return fig

    # Get unique groups for coloring
    groups = plot_df[group_by].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))
    group_colors = dict(zip(groups, colors))

    # Plot each group
    for group in groups:
        group_df = plot_df[plot_df[group_by] == group]

        # Non-Pareto points
        non_pareto = group_df[~group_df['is_pareto_optimal']]
        ax.scatter(
            non_pareto[cost_col],
            non_pareto[f1_col],
            c=[group_colors[group]],
            alpha=0.5,
            s=100,
            label=f"{group}",
        )

        # Pareto-optimal points
        pareto = group_df[group_df['is_pareto_optimal']]
        ax.scatter(
            pareto[cost_col],
            pareto[f1_col],
            c=[group_colors[group]],
            alpha=1.0,
            s=200,
            marker='*',
            edgecolors='black',
            linewidths=1,
        )

    # Plot Pareto frontier line
    pareto_df = plot_df[plot_df['is_pareto_optimal']].sort_values(cost_col)
    if len(pareto_df) > 1:
        ax.plot(
            pareto_df[cost_col],
            pareto_df[f1_col],
            'k--',
            alpha=0.5,
            linewidth=2,
            label='Pareto Frontier',
        )

    # Add annotations for Pareto-optimal points
    for idx, row in pareto_df.iterrows():
        label = f"{row['config']}\n({row['num_narrative_agents']}A, {row['aggregation']})"
        ax.annotate(
            label,
            (row[cost_col], row[f1_col]),
            textcoords="offset points",
            xytext=(10, 5),
            fontsize=8,
            alpha=0.8,
        )

    ax.set_xlabel(f"Cost (USD)", fontsize=12)
    ax.set_ylabel("F1-Samples", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    # Set axis limits with padding
    x_padding = (plot_df[cost_col].max() - plot_df[cost_col].min()) * 0.1
    y_padding = (plot_df[f1_col].max() - plot_df[f1_col].min()) * 0.1
    ax.set_xlim(
        plot_df[cost_col].min() - x_padding,
        plot_df[cost_col].max() + x_padding
    )
    ax.set_ylim(
        plot_df[f1_col].min() - y_padding,
        min(1.0, plot_df[f1_col].max() + y_padding)
    )

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved figure to {output_path}")

    return fig


def plot_latency_performance_curve(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Plot latency vs F1 performance."""
    return plot_cost_performance_curve(
        df,
        cost_col='avg_latency_sec',
        f1_col='f1_samples',
        output_path=output_path,
        title="Latency-Performance Tradeoff",
    )


def plot_api_calls_performance_curve(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Plot API calls vs F1 performance."""
    return plot_cost_performance_curve(
        df,
        cost_col='avg_api_calls',
        f1_col='f1_samples',
        output_path=output_path,
        title="API Calls vs Performance",
    )


def plot_multi_panel_comparison(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
) -> plt.Figure:
    """
    Create a 2x2 panel plot showing different cost-performance tradeoffs.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    plot_df = df[df['f1_samples'].notna()].copy()

    if len(plot_df) == 0:
        return fig

    # Panel 1: Cost vs F1
    ax = axes[0, 0]
    df_pareto = identify_pareto_frontier(plot_df, 'total_cost_usd', 'f1_samples')
    ax.scatter(df_pareto['total_cost_usd'], df_pareto['f1_samples'],
               c=df_pareto['num_narrative_agents'], cmap='viridis', s=100, alpha=0.7)
    pareto = df_pareto[df_pareto['is_pareto_optimal']].sort_values('total_cost_usd')
    if len(pareto) > 1:
        ax.plot(pareto['total_cost_usd'], pareto['f1_samples'], 'r--', alpha=0.5)
    ax.set_xlabel('Total Cost (USD)')
    ax.set_ylabel('F1-Samples')
    ax.set_title('Cost vs Performance')
    ax.grid(True, alpha=0.3)

    # Panel 2: Latency vs F1
    ax = axes[0, 1]
    df_pareto = identify_pareto_frontier(plot_df, 'avg_latency_sec', 'f1_samples')
    ax.scatter(df_pareto['avg_latency_sec'], df_pareto['f1_samples'],
               c=df_pareto['num_narrative_agents'], cmap='viridis', s=100, alpha=0.7)
    pareto = df_pareto[df_pareto['is_pareto_optimal']].sort_values('avg_latency_sec')
    if len(pareto) > 1:
        ax.plot(pareto['avg_latency_sec'], pareto['f1_samples'], 'r--', alpha=0.5)
    ax.set_xlabel('Avg Latency per Doc (sec)')
    ax.set_ylabel('F1-Samples')
    ax.set_title('Latency vs Performance')
    ax.grid(True, alpha=0.3)

    # Panel 3: API Calls vs F1
    ax = axes[1, 0]
    df_pareto = identify_pareto_frontier(plot_df, 'avg_api_calls', 'f1_samples')
    ax.scatter(df_pareto['avg_api_calls'], df_pareto['f1_samples'],
               c=df_pareto['num_narrative_agents'], cmap='viridis', s=100, alpha=0.7)
    pareto = df_pareto[df_pareto['is_pareto_optimal']].sort_values('avg_api_calls')
    if len(pareto) > 1:
        ax.plot(pareto['avg_api_calls'], pareto['f1_samples'], 'r--', alpha=0.5)
    ax.set_xlabel('Avg API Calls per Doc')
    ax.set_ylabel('F1-Samples')
    ax.set_title('API Calls vs Performance')
    ax.grid(True, alpha=0.3)

    # Panel 4: Agents vs F1 (box plot by number of agents)
    ax = axes[1, 1]
    agents = sorted(plot_df['num_narrative_agents'].unique())
    f1_by_agents = [plot_df[plot_df['num_narrative_agents'] == a]['f1_samples'].values for a in agents]
    bp = ax.boxplot(f1_by_agents, labels=[str(a) for a in agents], patch_artist=True)
    for patch, color in zip(bp['boxes'], plt.cm.viridis(np.linspace(0, 1, len(agents)))):
        patch.set_facecolor(color)
    ax.set_xlabel('Number of Agents')
    ax.set_ylabel('F1-Samples')
    ax.set_title('F1 Distribution by Agent Count')
    ax.grid(True, alpha=0.3, axis='y')

    # Add colorbar for the scatter plots
    sm = plt.cm.ScalarMappable(
        cmap='viridis',
        norm=plt.Normalize(vmin=plot_df['num_narrative_agents'].min(),
                           vmax=plot_df['num_narrative_agents'].max())
    )
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes[:, :], shrink=0.6, aspect=30)
    cbar.set_label('Number of Agents')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved figure to {output_path}")

    return fig


def create_summary_table(df: pd.DataFrame, output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Create a summary table comparing all configurations.
    """
    summary_cols = [
        'config', 'model', 'num_narrative_agents', 'aggregation', 'validation',
        'avg_api_calls', 'avg_cost_usd', 'avg_latency_sec', 'f1_samples'
    ]

    summary = df[summary_cols].copy()
    summary = summary.sort_values('f1_samples', ascending=False)

    # Round numeric columns
    for col in ['avg_api_calls', 'avg_cost_usd', 'avg_latency_sec']:
        summary[col] = summary[col].round(4)
    summary['f1_samples'] = summary['f1_samples'].round(4)

    if output_path:
        summary.to_csv(output_path, index=False)
        print(f"Saved summary table to {output_path}")

    return summary


def analyze_cost_scaling(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze how cost scales with number of agents.
    """
    if 'num_narrative_agents' not in df.columns:
        return {}

    analysis = {}

    for agents in sorted(df['num_narrative_agents'].unique()):
        subset = df[df['num_narrative_agents'] == agents]
        analysis[f'{agents}_agents'] = {
            'count': len(subset),
            'avg_cost': subset['avg_cost_usd'].mean(),
            'avg_latency': subset['avg_latency_sec'].mean(),
            'avg_f1': subset['f1_samples'].mean() if subset['f1_samples'].notna().any() else None,
            'cost_per_f1_point': (
                subset['avg_cost_usd'].mean() / subset['f1_samples'].mean()
                if subset['f1_samples'].notna().any() and subset['f1_samples'].mean() > 0
                else None
            ),
        }

    return analysis


def main():
    """Command-line interface for cost-performance analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze cost-performance tradeoffs across experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--metrics-dir',
        type=str,
        required=True,
        help='Directory containing cost_metrics.json files'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results/cost_analysis/',
        help='Directory to save analysis outputs'
    )
    parser.add_argument(
        '--format',
        choices=['png', 'pdf', 'svg'],
        default='png',
        help='Output format for figures'
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load all metrics
    print(f"Loading metrics from {args.metrics_dir}...")
    metrics_list = load_all_metrics(args.metrics_dir)
    print(f"Found {len(metrics_list)} experiment metrics")

    if not metrics_list:
        print("No metrics found. Exiting.")
        return 1

    # Create DataFrame
    df = create_comparison_dataframe(metrics_list)
    print(f"Created comparison DataFrame with {len(df)} rows")

    # Save raw data
    df.to_csv(output_dir / 'all_metrics.csv', index=False)

    # Create visualizations
    print("\nGenerating visualizations...")

    # Cost vs Performance
    plot_cost_performance_curve(
        df,
        output_path=str(output_dir / f'cost_vs_f1.{args.format}'),
    )

    # Latency vs Performance
    plot_latency_performance_curve(
        df,
        output_path=str(output_dir / f'latency_vs_f1.{args.format}'),
    )

    # Multi-panel comparison
    plot_multi_panel_comparison(
        df,
        output_path=str(output_dir / f'multi_panel_comparison.{args.format}'),
    )

    # Create summary table
    summary = create_summary_table(df, output_path=str(output_dir / 'summary_table.csv'))
    print("\nSummary Table:")
    print(summary.to_string(index=False))

    # Analyze cost scaling
    scaling = analyze_cost_scaling(df)
    with open(output_dir / 'cost_scaling_analysis.json', 'w') as f:
        json.dump(scaling, f, indent=2)

    print(f"\nAnalysis complete. Results saved to {output_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
