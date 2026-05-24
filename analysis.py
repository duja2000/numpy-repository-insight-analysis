from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import calendar

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

RAW_LOG = DATA_DIR / "raw_git_log.txt"
OUTPUT_CSV = DATA_DIR / "monthly_activity.csv"

PLOTS_DIR.mkdir(exist_ok=True)


def parse_git_log(raw_log_path: Path) -> pd.DataFrame:
    records = []
    current_commit = None

    with raw_log_path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("@@@"):
                parts = line.replace("@@@", "").split("|")
                if len(parts) >= 4:
                    current_commit = {
                        "commit_hash": parts[0],
                        "date": parts[1],
                        "author_name": parts[2],
                        "author_email": parts[3],
                        "lines_added": 0,
                        "lines_removed": 0,
                        "files_changed": 0,
                    }
                    records.append(current_commit)

            else:
                if current_commit is None:
                    continue

                parts = line.split("\t")
                if len(parts) >= 3:
                    added = parts[0]
                    removed = parts[1]

                    if added.isdigit() and removed.isdigit():
                        current_commit["lines_added"] += int(added)
                        current_commit["lines_removed"] += int(removed)
                        current_commit["files_changed"] += 1

    return pd.DataFrame(records)


def build_monthly_activity(commits: pd.DataFrame) -> pd.DataFrame:
    commits["date"] = pd.to_datetime(commits["date"], errors="coerce")
    commits = commits.dropna(subset=["date"])

    commits["month"] = commits["date"].dt.to_period("M").astype(str)
    commits["total_churn"] = commits["lines_added"] + commits["lines_removed"]

    monthly = (
        commits.groupby("month")
        .agg(
            commit_count=("commit_hash", "count"),
            lines_added=("lines_added", "sum"),
            lines_removed=("lines_removed", "sum"),
            total_churn=("total_churn", "sum"),
            files_changed=("files_changed", "sum"),
        )
        .reset_index()
    )

    monthly["month_date"] = pd.to_datetime(monthly["month"])
    return monthly


def plot_time_series(monthly: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.plot(monthly["month_date"], monthly["commit_count"], label="Monthly commits")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Commit count")

    ax2 = ax1.twinx()
    ax2.plot(monthly["month_date"], monthly["total_churn"], linestyle="--", label="Total churn")
    ax2.set_ylabel("Total churn: lines added + removed")

    plt.title("Monthly NumPy Development Activity: Commits and Code Churn")
    fig.tight_layout()
    plt.savefig(PLOTS_DIR / "monthly_commits_churn_timeseries.png", dpi=300)
    plt.close()


def plot_churn_distribution(monthly: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    plt.hist(monthly["total_churn"], bins=40)
    plt.xlabel("Monthly total churn")
    plt.ylabel("Number of months")
    plt.title("Distribution of Monthly Code Churn")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "churn_distribution.png", dpi=300)
    plt.close()


def plot_activity_heatmap(monthly: pd.DataFrame):
    monthly["year"] = monthly["month_date"].dt.year
    monthly["month_num"] = monthly["month_date"].dt.month

    heatmap_data = monthly.pivot(index="year", columns="month_num", values="commit_count")
    heatmap_data = heatmap_data.fillna(0)

    plt.figure(figsize=(12, 8))
    plt.imshow(heatmap_data, aspect="auto")
    plt.colorbar(label="Commit count")

    plt.xticks(
        ticks=range(12),
        labels=[calendar.month_abbr[i] for i in range(1, 13)],
        rotation=45,
    )
    plt.yticks(ticks=range(len(heatmap_data.index)), labels=heatmap_data.index)

    plt.xlabel("Month")
    plt.ylabel("Year")
    plt.title("Monthly Commit Activity Heatmap")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "activity_heatmap.png", dpi=300)
    plt.close()


def main():
    print("Parsing git history...")
    commits = parse_git_log(RAW_LOG)
    print(f"Parsed commits: {len(commits)}")

    monthly = build_monthly_activity(commits)
    monthly.to_csv(OUTPUT_CSV, index=False)

    print("Saved cleaned data to:", OUTPUT_CSV)

    print("Generating plots...")
    plot_time_series(monthly)
    plot_churn_distribution(monthly)
    plot_activity_heatmap(monthly)

    print("Done. Plots saved in the plots folder.")
    print(monthly.head())
    print(monthly.tail())


if __name__ == "__main__":
    main()