import os
import textwrap

import matplotlib

matplotlib.use("Agg")  # save to a file, no window needed
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "docs", "pareto_chart.png")

# Defect counts from the Checksheet in docs/defect_log.md (Round 1)
DEFECTS = {
    "Duplicate entries accepted": 5,
    "Invalid item name accepted": 4,
    "Invalid price accepted": 4,
    "Missing confirmation": 2,
    "Wrong way of running the application": 1,
}


def build_pareto():
    # Sort from the highest count to the lowest
    data = sorted(DEFECTS.items(), key=lambda pair: pair[1], reverse=True)
    labels = [name for name, _ in data]
    counts = [count for _, count in data]
    total = sum(counts)

    cumulative = []
    running = 0
    for count in counts:
        running += count
        cumulative.append(running / total * 100)

    positions = list(range(len(labels)))

    fig, ax = plt.subplots(figsize=(10, 6.5))

    bars = ax.bar(positions, counts, color="#1f6aa5", width=0.6, label="Defect count")
    ax.set_ylim(0, total * 1.05)
    ax.set_ylabel("Number of defects")
    ax.set_xticks(positions)
    ax.set_xticklabels([textwrap.fill(label, 16) for label in labels])

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() - 0.25,
            str(count),
            ha="center",
            va="top",
            color="white",
            fontsize=12,
            fontweight="bold",
        )

    ax2 = ax.twinx()
    ax2.plot(positions, cumulative, color="#e67e22", marker="o", linewidth=2, label="Cumulative %")
    ax2.set_ylim(0, 105)
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel("Cumulative percentage")
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
    ax2.text(len(labels) - 0.5, 81.5, "80% line", ha="right", color="gray")

    for x, value in zip(positions, cumulative):
        ax2.text(x, value + 3, f"{value:.2f}%", ha="center", color="#b9770e", fontsize=9)

    ax.set_title(
        "Pareto Chart - Defects in Restaurant Billing System (before Q06 features)",
        fontweight="bold",
        pad=22,
    )
    handles1, names1 = ax.get_legend_handles_labels()
    handles2, names2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, names1 + names2, loc="center right")

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)

    print("Pareto chart saved:", OUTPUT_PATH)
    print(f"Total defects: {total}")
    for label, count, cum in zip(labels, counts, cumulative):
        print(f"  {label}: {count} (cumulative {cum:.2f}%)")


if __name__ == "__main__":
    build_pareto()