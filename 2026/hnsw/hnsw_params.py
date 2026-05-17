import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

from manim import *
from hnsw_params_scenes import (
    DashboardMixin,
    MParamMixin,
    EfParamMixin,
    ConclusionMixin,
)
from hnsw_params_scenes.common import BG_COLOR


class HNSWParams(
    Scene,
    DashboardMixin,
    MParamMixin,
    EfParamMixin,
    ConclusionMixin,
):
    def construct(self):
        # 1. Setup Camera Background
        self.camera.background_color = BG_COLOR

        # 2. Execute Scenes sequentially
        self.run_dashboard_scene()
        self.run_m_parameter_scene()
        self.run_ef_parameter_scene()
        self.run_conclusion_scene()
