import sys
import pathlib

# Append current directory to path for clean relative imports
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

from manim import *
from hnsw_search_scenes import HNSWSearchMixin
from hnsw_search_scenes.common import BG_COLOR


class HNSWSearch(ThreeDScene, HNSWSearchMixin):
    def construct(self):
        # 1. Title Intro Card
        self.intro_scene()

        # 2. Initial Camera Setup and Scene Variables
        self.init_search_scene()

        # 3. Run Search Scenes Sequentially
        # Scene 1: Top Layer walk A -> D -> E
        self.scene_1_l2_walk()

        # Scene 2: Dive to Layer 1 (camera zoom center E)
        self.scene_2_dive_to_l1()

        # Scene 3: Refinement on Layer 1: E -> H -> I -> K
        self.scene_3_l1_refinement()

        # Scene 4: Final Dive to Layer 0 (zoom center K) + walk K -> R -> P
        self.scene_4_dive_to_l0_and_walk()

        # Scene 5: Replay complete path in 3D (camera tilt + layer vertical stacking)
        self.scene_5_3d_replay()
