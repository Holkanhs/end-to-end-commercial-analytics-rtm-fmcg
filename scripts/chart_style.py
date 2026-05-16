"""SWD-style matplotlib defaults — vendored so the project is self-contained.

Call apply_style() once at the top of any chart script. It returns the palette
dict so colors can be referenced by name (PALETTE["blue"], etc.).
"""
import matplotlib.pyplot as plt

PALETTE = {
    "blue":   "#2563EB",
    "orange": "#F97316",
    "red":    "#DC2626",
    "green":  "#16A34A",
    "grey":   "#9CA3AF",
    "dark":   "#374151",
}


def apply_style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#E5E7EB",
        "grid.linestyle": "-",
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "figure.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.dpi": 150,
    })
    return PALETTE
