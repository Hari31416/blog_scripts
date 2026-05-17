import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

from manim import *
from hnsw_build_scenes import (
    IntroSceneMixin,
    LayerSelectionMixin,
    GreedyWalkMixin,
    HeuristicMixin,
    BaseLayerMixin,
)
from hnsw_build_scenes.common import BG_COLOR


class HNSWBuild(
    ThreeDScene,
    IntroSceneMixin,
    LayerSelectionMixin,
    GreedyWalkMixin,
    HeuristicMixin,
    BaseLayerMixin,
):
    def construct(self):
        # 1. Setup Camera Background
        self.camera.background_color = BG_COLOR

        # Initial Camera Setup
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        # 2. Execute Scenes sequentially
        self.intro_scene()
        self.layer_selection_scene()
        self.greedy_walk_scene()
        self.heuristic_connection_scene()
        self.base_layer_scene()
