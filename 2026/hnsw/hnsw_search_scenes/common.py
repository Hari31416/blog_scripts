from manim import *
import numpy as np

# Premium Color Palette matching Part 1
BG_COLOR = "#05070D"
QUERY_COLOR = "#FF5A5F"      # Rose Red
SEARCHER_COLOR = "#A78BFA"   # Violet
PROBE_GREEN = "#22C55E"      # Emerald Green
PROBE_RED = "#EF4444"        # Rose Red

# Layer Graphic Colors
PLANE_L2_COLOR = "#4C1D95"
PLANE_L1_COLOR = "#312E81"
PLANE_L0_COLOR = "#1E293B"

NODE_L2_COLOR = "#C7D2FE"
EDGE_L2_COLOR = "#6B7280"

NODE_L1_COLOR = "#E5E7EB"
EDGE_L1_COLOR = "#64748B"

NODE_L0_COLOR = "#FFFFFF"
EDGE_L0_COLOR = "#475569"

# Path colors in Scene 5
PATH_L2_COLOR = "#A78BFA"
PATH_L1_COLOR = "#6366F1"
PATH_L0_COLOR = "#FFFFFF"

# 2D/3D Coordinates for search nodes
# We structure coordinates as a dictionary of np.array([x, y]) for ease of 2D use.
# When in 3D, z coordinates will be added dynamically based on layer.
COORDS = {
    # Layer 2 Nodes (Sparse)
    "A": np.array([-3.0, 2.5]),
    "D": np.array([-1.0, 2.0]),
    "E": np.array([-0.5, 0.5]),
    "X": np.array([-2.0, -1.0]),
    
    # Layer 1 Nodes (Coarse)
    "H": np.array([0.5, 0.2]),
    "I": np.array([1.2, -0.4]),
    "K": np.array([1.8, -0.6]),
    "Y": np.array([1.0, -1.5]),
    "Z": np.array([2.5, 0.5]),
    
    # Layer 0 Nodes (Dense)
    "R": np.array([2.4, -1.2]),
    "P": np.array([2.7, -1.6]),
    
    # Clutter nodes to make L0 look dense
    "C1": np.array([-2.5, 1.0]),
    "C2": np.array([-1.5, -0.5]),
    "C3": np.array([0.0, -1.8]),
    "C4": np.array([1.5, 1.8]),
    "C5": np.array([0.2, 2.2]),
    "C6": np.array([3.0, 1.0]),
}

# The Query Point Q (which remains fixed and pulsed)
COORD_Q = np.array([3.0, -2.0])

# Graph connectivity per layer
L2_EDGES = [("A", "D"), ("D", "E"), ("E", "X")]

L1_EDGES = L2_EDGES + [
    ("D", "H"), ("E", "H"), ("H", "I"), ("I", "K"), ("K", "Y"), ("K", "Z")
]

L0_EDGES = L1_EDGES + [
    ("K", "R"), ("R", "P"),
    # Clutter connections
    ("A", "C4"), ("C4", "C5"), ("D", "C5"),
    ("X", "C2"), ("E", "C2"),
    ("H", "C3"), ("I", "C3"),
    ("Y", "C3"), ("Z", "C6"), ("P", "C6"),
]
