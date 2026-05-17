from manim import *
import numpy as np

# Premium Color Palette
BG_COLOR = "#05070D"
QUERY_COLOR = "#FF5A5F"  # Rose Red
SEARCHER_COLOR = "#A78BFA"  # Violet
EMERALD_COLOR = "#10B981"  # Emerald Green
ROSE_COLOR = "#EF4444"  # Red / Failure
GOLD_COLOR = "#FBBF24"  # Gold / Warning
SLATE_COLOR = "#64748B"  # Slate Gray
DARK_SLATE = "#334155"  # Darker Slate

# Scene 2: M Parameter Coordinates and Graphs
# Standard coordinates for 15 nodes
COORDS_M = {
    "N0": np.array([-2.5, 2.0]),  # Entry
    "N1": np.array([-2.0, 1.2]),
    "N2": np.array([-1.5, 0.7]),
    "N3": np.array([-1.0, 0.1]),
    "N4": np.array([-0.7, -0.5]),
    "N5": np.array([-0.3, -1.2]),
    "N6": np.array([-0.1, -1.9]),  # Local Min for Low M
    "N7": np.array([-1.8, -1.5]),
    "N8": np.array([0.8, 0.5]),
    "N9": np.array([-0.5, 1.8]),
    "N10": np.array([0.2, 1.4]),
    "N11": np.array([1.2, 1.8]),
    "N12": np.array([0.5, -0.8]),
    "N13": np.array([1.0, -1.8]),
    "N14": np.array([1.9, -1.0]),  # True NN
}

COORD_Q_M = np.array([2.2, -1.2])

LOW_M_EDGES = [
    ("N0", "N1"),
    ("N1", "N2"),
    ("N2", "N3"),
    ("N3", "N4"),
    ("N4", "N5"),
    ("N5", "N6"),
    ("N2", "N9"),
    ("N9", "N10"),
    ("N10", "N11"),
    ("N8", "N12"),
    ("N12", "N13"),
    ("N13", "N14"),
    ("N7", "N4"),
]

# High M contains low M edges plus shortcuts
HIGH_M_EDGES = LOW_M_EDGES + [
    ("N0", "N8"),
    ("N8", "N14"),
    ("N1", "N8"),
    ("N3", "N12"),
    ("N5", "N13"),
    ("N6", "N13"),
    ("N11", "N14"),
    ("N10", "N8"),
]

# Scene 3: ef Parameter Coordinates and Graphs
COORDS_EF = {
    "E": np.array([-2.0, 0.0]),  # Entry node
    "B1": np.array([-0.7, 1.2]),  # Crescent barrier
    "B2": np.array([-0.1, 0.6]),
    "B3": np.array([0.1, 0.0]),  # Crescent center (Local Min)
    "B4": np.array([-0.1, -0.6]),
    "B5": np.array([-0.7, -1.2]),
    "C1": np.array([0.5, 1.1]),  # Escape path
    "C2": np.array([1.4, 0.7]),
    "TrueNN": np.array([2.0, 0.0]),  # True Nearest Neighbor
}

COORD_Q_EF = np.array([2.2, 0.0])

# Graph is identical for both left & right
EF_EDGES = [
    ("E", "B1"),
    ("E", "B2"),
    ("E", "B3"),
    ("E", "B4"),
    ("E", "B5"),
    ("B1", "B2"),
    ("B2", "B3"),
    ("B3", "B4"),
    ("B4", "B5"),
    ("B2", "C1"),
    ("C1", "C2"),
    ("C2", "TrueNN"),
]
