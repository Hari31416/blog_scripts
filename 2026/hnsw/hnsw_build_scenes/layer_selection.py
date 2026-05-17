from manim import *
import numpy as np
from .common import *


class LayerSelectionMixin:
    def layer_selection_scene(self):
        # Header Overlay
        header = Text(
            "Layer Selection via Exponential Decay",
            font_size=24,
            color=GOLD_COLOR,
        ).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(header)

        # Formula Overlay
        formula = MathTex(
            r"L_{\text{max}} = \left\lfloor -\ln(u) \cdot m_L \right\rfloor",
            font_size=32,
        ).to_corner(UL, buff=0.8)

        self.camera.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(0.5)

        # Dice Roll / Decaying bar UI
        u_label = MathTex(r"u = ", font_size=28)
        u_val = DecimalNumber(0.25, num_decimal_places=2, font_size=28)
        u_group = VGroup(u_label, u_val).arrange(RIGHT, buff=0.1)
        res_val = MathTex(
            r"L_{\text{max}} = \lfloor -\ln(0.25) \cdot 1.0 \rfloor = 1",
            font_size=28,
            color=GOLD_COLOR,
        )

        u_group.next_to(formula, DOWN, aligned_edge=LEFT, buff=0.4)
        res_val.next_to(u_group, DOWN, aligned_edge=LEFT, buff=0.3)

        self.add_fixed_in_frame_mobjects(u_group)

        # Roll animation: rapidly change decimal values
        for _ in range(12):
            u_val.set_value(np.random.uniform(0.01, 0.99))
            self.camera.add_fixed_in_frame_mobjects(u_val)
            self.wait(0.08)

        # Land on 0.25
        u_val.set_value(0.25)
        self.camera.add_fixed_in_frame_mobjects(u_val)
        self.camera.add_fixed_in_frame_mobjects(res_val)
        self.play(Write(res_val))
        self.wait(1)

        # Glowing gold node N appears above Layer 2
        # Position N at [1.0, -0.5, 3.0] (high above stack, completely in frame)
        self.node_n = Dot(
            point=[COORDS["P"][0], COORDS["P"][1], 3.0], color=GOLD_COLOR, radius=0.12
        )
        n_label = Text("New Node N", font_size=18, color=GOLD_COLOR).next_to(
            self.node_n, UP, buff=0.2
        )

        self.play(FadeIn(self.node_n), FadeIn(n_label))

        # N descends to hover above Layer 1 (z = 0.8)
        self.play(
            self.node_n.animate.move_to([COORDS["P"][0], COORDS["P"][1], 0.8]),
            n_label.animate.next_to(self.node_n, UP, buff=0.2),
            run_time=2,
        )
        self.wait(1.5)

        # Clean up scene elements
        self.play(
            FadeOut(header),
            FadeOut(formula),
            FadeOut(u_group),
            FadeOut(res_val),
            FadeOut(n_label),
        )
