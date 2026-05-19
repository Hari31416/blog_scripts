import sys
import pathlib

# Append current directory to path for clean relative imports
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

from manim import *
from rag_metrics_scenes import (
    IntroMixin,
    PrecisionRecallMixin,
    HitRateMixin,
    MRRMixin,
    MAPMixin,
    NDCGMixin,
    OutroMixin,
)
from rag_metrics_scenes.common import BG_COLOR


class RAGMetrics(
    Scene,
    IntroMixin,
    PrecisionRecallMixin,
    HitRateMixin,
    MRRMixin,
    MAPMixin,
    NDCGMixin,
    OutroMixin,
):
    def construct(self):
        # 1. Setup Camera Background
        self.camera.background_color = BG_COLOR

        # 2. Execute Scenes sequentially
        self.intro_scene()
        self.precision_recall_scene()
        self.hit_rate_scene()
        self.mrr_scene()
        self.map_scene()
        self.ndcg_scene()
        self.outro_scene()
