from manim import *
import numpy as np

# Premium Color Palette
GOLD_COLOR = "#FBBF24"
VIOLET_COLOR = "#A78BFA"
EMERALD_COLOR = "#10B981"
ROSE_COLOR = "#EF4444"
AMBER_COLOR = "#F59E0B"
BG_COLOR = "#05070D"
PLANE_L2_COLOR = "#4C1D95"
PLANE_L1_COLOR = "#312E81"
PLANE_L0_COLOR = "#1E293B"
NODE_COLOR = "#E5E7EB"
EDGE_COLOR = "#4B5563"

# Node coordinates in 2D
COORDS = {
    "E": np.array([0.0, 0.0]),
    "P": np.array([0.1, -0.6]),
    "Q": np.array([2.0, -1.0]),
    "B": np.array([-2.0, -1.0]),
    "D": np.array([-1.0, 1.5]),
    "A": np.array([1.5, 1.0]),
    "C": np.array([2.0, -1.5]),
    "F": np.array([2.5, 0.5]),
    "G": np.array([-1.5, -2.0]),
}
