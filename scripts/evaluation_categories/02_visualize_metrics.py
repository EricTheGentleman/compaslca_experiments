import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def plot_metric_distributions(csv_path, output_dir):
    df = pd.read_csv(csv_path)

    # Add new metrics
    metrics = ["jaccard_index", "precision", "recall", "f1_score", "f0.5_score"]
    binary_flags = ["success_f1", "success_f05"]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Histogram for each continuous metric
    for metric in metrics:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[metric], kde=True, bins=20)
        plt.title(f"Distribution of {metric.replace('_', ' ').title()}")
        plt.xlabel(metric.replace('_', ' ').title())
        plt.ylabel("Count")
        plt.tight_layout()
        hist_path = output_dir / f"{metric}_distribution.png"
        plt.savefig(hist_path)
        plt.close()
        print(f"📊 Saved histogram to: {hist_path}")

    # Combined boxplot for all continuous metrics
    melted = df.melt(value_vars=metrics, var_name="Metric", value_name="Score")
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Metric", y="Score", data=melted)
    plt.title("Boxplot of Evaluation Metrics")
    plt.tight_layout()
    boxplot_path = output_dir / "boxplot_all_metrics.png"
    plt.savefig(boxplot_path)
    plt.close()
    print(f"📊 Saved boxplot to: {boxplot_path}")

    # Bar chart for each binary success flag
    for flag in binary_flags:
        plt.figure(figsize=(6, 4))
        sns.countplot(x=flag, data=df)
        plt.title(f"Success Count: {flag}")
        plt.xlabel("Success (1) / Failure (0)")
        plt.ylabel("Count")
        plt.tight_layout()
        bar_path = output_dir / f"{flag}_bar_chart.png"
        plt.savefig(bar_path)
        plt.close()
        print(f"📊 Saved success bar chart to: {bar_path}")

# === Example usage ===
if __name__ == "__main__":
    input_csv = "data/output/material/02_combinations/t_t_t_t_t_t/metrics_all.csv"
    output_dir = "data/output/material/02_combinations/t_t_t_t_t_t/plots"
    plot_metric_distributions(input_csv, output_dir)
