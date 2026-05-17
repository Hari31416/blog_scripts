from manim import *
from .common import *


class BaseLayerMixin:
    def base_layer_scene(self):
        header = Text(
            "Connection on Layer 0 & Edge Pruning",
            font_size=24,
            color=AMBER_COLOR,
        ).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(header)

        # Restore camera to 3D perspective to see the drop down to L0
        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.9, run_time=2)
        self.wait(0.5)

        # Connectors for N and its neighbors down to L0
        proj_n = DashedLine(
            start=[1.0, -0.5, 0.0],
            end=[1.0, -0.5, -2.0],
            color=GOLD_COLOR,
            stroke_width=1.5,
        )
        self.play(Create(proj_n))

        # Clone N to Layer 0
        node_n_l0 = Dot(point=[1.0, -0.5, -2.0], color=GOLD_COLOR, radius=0.08)
        self.play(
            self.node_n.animate.move_to([1.0, -0.5, -2.0]),
            self.node_n_label.animate.move_to([1.0, -0.5 + 0.35, -2.0]),
            FadeIn(node_n_l0),
            run_time=1.5,
        )

        # Draw L0 connections for N (P, Q, A, C)
        l0_edges_n = VGroup(
            Line(
                start=[1.0, -0.5, -2.0],
                end=[COORDS["P"][0], COORDS["P"][1], -2.0],
                color=EMERALD_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[1.0, -0.5, -2.0],
                end=[COORDS["Q"][0], COORDS["Q"][1], -2.0],
                color=EMERALD_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[1.0, -0.5, -2.0],
                end=[COORDS["A"][0], COORDS["A"][1], -2.0],
                color=EMERALD_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[1.0, -0.5, -2.0],
                end=[COORDS["C"][0], COORDS["C"][1], -2.0],
                color=EMERALD_COLOR,
                stroke_width=2,
            ),
        )
        self.play(Create(l0_edges_n, lag_ratio=0.1, run_time=1.5))
        self.wait(1)

        # --- PRUNING DEMONSTRATION ---
        # Highlight Node P because it now has 5 connections (limit is M = 4)
        prune_desc = Text(
            "Edge Budget Exceeded! Node P has 5 connections (Limit = 4)\nPruning redundant connections using Diversity Heuristic...",
            font_size=18,
            color=AMBER_COLOR,
        ).to_corner(UL, buff=0.8)
        self.add_fixed_in_frame_mobjects(prune_desc)

        # Highlight Node P on Layer 0 in Amber
        p_node_l0 = self.nodes_l0[
            1
        ]  # Node P is index 1 in ["E", "P", "Q", "B", "D", "A", "C", "F", "G"]
        self.play(p_node_l0.animate.set_color(AMBER_COLOR))
        self.wait(1)

        # Redundant connection for P is its connection to D. Let's make it turn red and shake/crack.
        pruning_edge = Line(
            start=[COORDS["P"][0], COORDS["P"][1], -2.0],
            end=[COORDS["D"][0], COORDS["D"][1], -2.0],
            color=ROSE_COLOR,
            stroke_width=3,
        )
        self.play(FadeIn(pruning_edge))

        # Visual wiggle effect of pruning edge
        for _ in range(5):
            self.play(
                pruning_edge.animate.shift(UP * 0.05 + RIGHT * 0.05), run_time=0.08
            )
            self.play(
                pruning_edge.animate.shift(DOWN * 0.05 + LEFT * 0.05), run_time=0.08
            )

        self.play(FadeOut(pruning_edge), run_time=0.5)

        # Fade out the original P-D edge as well
        p_d_original = self.edges_l0[4]
        self.play(p_d_original.animate.set_stroke(opacity=0.0))

        success_prune = Text(
            "Pruned connection P-D to maintain navigability!", font_size=18, color=GREEN
        ).next_to(prune_desc, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(success_prune)
        self.play(Write(success_prune))
        self.wait(2)

        # Solidify all emerald edges into EDGE_COLOR
        self.play(
            l0_edges_n.animate.set_color(EDGE_COLOR),
            p_node_l0.animate.set_color(NODE_COLOR),
        )
        self.wait(1)

        # Complete full stack glow
        final_text = Text(
            "HNSW Index Bounded and Fully Navigable", font_size=24, color=GOLD_COLOR
        ).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(final_text)

        # Final Glow animation: flash all planes and nodes
        self.play(
            FadeOut(header),
            FadeOut(prune_desc),
            FadeOut(success_prune),
            FadeIn(final_text),
        )

        self.play(
            self.plane_l2.animate.set_color(GOLD_COLOR),
            self.plane_l1.animate.set_color(GOLD_COLOR),
            self.plane_l0.animate.set_color(GOLD_COLOR),
            run_time=1.0,
        )
        self.wait(0.5)
        self.play(
            self.plane_l2.animate.set_color(PLANE_L2_COLOR),
            self.plane_l1.animate.set_color(PLANE_L1_COLOR),
            self.plane_l0.animate.set_color(PLANE_L0_COLOR),
            run_time=1.0,
        )
        self.wait(3.5)

        # Clean up
        self.play(
            FadeOut(self.plane_l0),
            FadeOut(self.plane_l1),
            FadeOut(self.plane_l2),
            FadeOut(self.nodes_l0),
            FadeOut(self.nodes_l1),
            FadeOut(self.nodes_l2),
            FadeOut(self.labels_l0),
            FadeOut(self.labels_l1),
            FadeOut(self.labels_l2),
            FadeOut(self.edges_l0),
            FadeOut(self.edges_l1),
            FadeOut(self.vertical_connectors),
            FadeOut(proj_n),
            FadeOut(node_n_l0),
            FadeOut(l0_edges_n),
            FadeOut(self.node_n),
            FadeOut(self.node_n_label),
            FadeOut(self.l1_n_edges),
            FadeOut(final_text),
        )
        self.wait(1)
