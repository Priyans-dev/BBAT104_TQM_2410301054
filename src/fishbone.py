import os
import textwrap

import matplotlib

matplotlib.use("Agg")  # save to a file, no window needed
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "docs", "fishbone.png")

# Effect = the biggest defect found in the Pareto chart (5 of 16 defects)
EFFECT = "Duplicate entries\naccepted in the menu"

# Root causes of the effect, grouped by category
CAUSES = {
    "People": [
        "Same item typed with different capitals",
        "Extra spaces typed by mistake",
        "Rush while adding items",
    ],
    "Process": [
        "No step to search the menu first",
        "No confirmation before saving",
        "No review of the menu data",
    ],
    "Software (Code)": [
        "No unique constraint on item name",
        "Names not cleaned before saving",
        "No check for existing items",
    ],
    "Data": [
        "Old duplicate rows in database",
        "No standard naming for items",
        "No fixed list of categories",
    ],
    "Environment": [
        "Single local database file",
        "No backup of the database",
        "Wrong file run by mistake",
    ],
    "Testing": [
        "No test cases before release",
        "Capital and space cases not tested",
        "No defect log kept",
    ],
}

TOP = ["People", "Process", "Software (Code)"]
BOTTOM = ["Data", "Environment", "Testing"]

BONE_COLOR = "#1f6aa5"
CAUSE_COLOR = "#333333"


def draw_bone(ax, spine_x, spine_y, category, causes, direction):
    """direction = +1 for a bone above the spine, -1 for a bone below it."""
    top_x = spine_x - 1.7
    top_y = spine_y + direction * 3.1

    ax.plot([top_x, spine_x], [top_y, spine_y], color=BONE_COLOR, linewidth=2.5)

    ax.text(
        top_x,
        top_y + direction * 0.28,
        category,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="white",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=BONE_COLOR, edgecolor="none"),
    )

    for index, cause in enumerate(causes):
        t = 0.22 + index * 0.26
        point_x = top_x + (spine_x - top_x) * t
        point_y = top_y + (spine_y - top_y) * t
        ax.plot([point_x - 0.45, point_x], [point_y, point_y], color=CAUSE_COLOR, linewidth=1)
        ax.text(
            point_x - 0.5,
            point_y,
            textwrap.fill(cause, 22),
            ha="right",
            va="center",
            fontsize=8.5,
            color=CAUSE_COLOR,
        )


def build_fishbone():
    fig, ax = plt.subplots(figsize=(16, 8.5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8.6)
    ax.axis("off")

    spine_y = 4.3
    ax.annotate(
        "",
        xy=(12.6, spine_y),
        xytext=(0.5, spine_y),
        arrowprops=dict(arrowstyle="-|>", color=BONE_COLOR, linewidth=3.5),
    )

    # Effect box (head of the fish)
    ax.add_patch(
        FancyBboxPatch(
            (12.7, spine_y - 0.85),
            3.1,
            1.7,
            boxstyle="round,pad=0.05",
            facecolor="#c0392b",
            edgecolor="none",
        )
    )
    ax.text(
        14.25,
        spine_y,
        EFFECT,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="white",
    )

    spine_positions = [5.1, 8.8, 12.5]
    for x, category in zip(spine_positions, TOP):
        draw_bone(ax, x, spine_y, category, CAUSES[category], direction=+1)
    for x, category in zip(spine_positions, BOTTOM):
        draw_bone(ax, x, spine_y, category, CAUSES[category], direction=-1)

    ax.set_title(
        "Fishbone (Cause and Effect) Diagram - Restaurant Billing System",
        fontsize=14,
        fontweight="bold",
        pad=10,
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)
    print("Fishbone diagram saved:", OUTPUT_PATH)


if __name__ == "__main__":
    build_fishbone()