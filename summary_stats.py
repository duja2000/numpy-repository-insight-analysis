import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
df = pd.read_csv(DATA_DIR / "monthly_activity.csv")

summary_path = DATA_DIR / "summary_stats.txt"

with open(summary_path, "w", encoding="utf-8") as f:
    f.write("Repository Insight Analysis: NumPy Monthly Activity Summary\n")
    f.write("=" * 65 + "\n\n")

    f.write(f"Number of monthly observations: {len(df)}\n")
    f.write(f"Time period: {df['month'].min()} to {df['month'].max()}\n")
    f.write(f"Total commits analyzed: {df['commit_count'].sum()}\n")
    f.write(f"Total lines added: {df['lines_added'].sum()}\n")
    f.write(f"Total lines removed: {df['lines_removed'].sum()}\n")
    f.write(f"Total churn: {df['total_churn'].sum()}\n")
    f.write(f"Average monthly commits: {df['commit_count'].mean():.2f}\n")
    f.write(f"Average monthly churn: {df['total_churn'].mean():.2f}\n\n")

    f.write("Top 10 months by commit count:\n")
    f.write(df.sort_values("commit_count", ascending=False)
              [["month", "commit_count", "total_churn", "lines_added", "lines_removed"]]
              .head(10)
              .to_string(index=False))
    f.write("\n\n")

    f.write("Top 10 months by total churn:\n")
    f.write(df.sort_values("total_churn", ascending=False)
              [["month", "commit_count", "total_churn", "lines_added", "lines_removed"]]
              .head(10)
              .to_string(index=False))
    f.write("\n\n")

    f.write("Recent 12 months:\n")
    f.write(df.tail(12)[["month", "commit_count", "total_churn", "lines_added", "lines_removed"]]
              .to_string(index=False))

print("Summary statistics saved to data/summary_stats.txt")