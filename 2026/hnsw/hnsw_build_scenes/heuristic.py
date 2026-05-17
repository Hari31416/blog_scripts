from manim import *
from .common import *


class HeuristicMixin:
    def heuristic_connection_scene(self):
        header = Text(
            "Connection & HNSW Diversity Heuristic",
            font_size=24,
            color=EMERALD_COLOR,
        ).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(header)

        # Smooth camera orientation transition: Zoom in to Layer 1 (move to top-down view)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.1, run_time=2)

        # Node N drops into its exact spot on Layer 1 (z = 0.0)
        self.play(self.node_n.animate.move_to([COORDS["P"][0], COORDS["P"][1], 0.0]))
        self.node_n_label = Text("N", font_size=18, color=GOLD_COLOR).next_to(
            self.node_n, UP, buff=0.08
        )
        self.add(self.node_n_label)
        self.wait(0.5)

        # priority queue / candidate list container
        pq_title = Text("Layer 1 Candidates", font_size=18, weight=BOLD).to_corner(
            UR, buff=0.8
        )
        pq_items = (
            VGroup(
                Text("1. Node P (d = 0.90)", font_size=16, color=GOLD_COLOR),
                Text("2. Node E (d = 1.12)", font_size=16, color=GRAY),
                Text("3. Node Q (d = 1.12)", font_size=16, color=GRAY),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .next_to(pq_title, DOWN, buff=0.25)
        )

        pq_bg = SurroundingRectangle(
            VGroup(pq_title, pq_items),
            color=GRAY_A,
            fill_color=BG_COLOR,
            fill_opacity=0.8,
            buff=0.2,
        )

        pq_group = VGroup(pq_bg, pq_title, pq_items)
        self.add_fixed_in_frame_mobjects(pq_group)
        self.play(FadeIn(pq_group, shift=LEFT))
        self.wait(1)

        # Sequential Comparison
        mode_text = Text(
            "Connecting to M = 2 neighbors", font_size=20, color=GOLD_COLOR
        ).to_corner(UL, buff=0.8)
        self.add_fixed_in_frame_mobjects(mode_text)
        self.play(Write(mode_text))

        # NAIVE CONNECTION demonstration
        naive_title = Text(
            "Naive Proximity Selection (Clustered)", font_size=18, color=ROSE_COLOR
        ).next_to(mode_text, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(naive_title)
        self.play(Write(naive_title))

        # Position self.node_n and its label at correct N coordinates (1.0, -0.5)
        self.node_n.move_to([1.0, -0.5, 0.0])
        self.node_n_label.move_to([1.0, -0.5 + 0.35, 0.0])

        # Naive selection connects to the 2 closest: Node P and Node E using correct N coordinates
        naive_edge_p = Line(
            start=[1.0, -0.5, 0.0],
            end=[COORDS["P"][0], COORDS["P"][1], 0.0],
            color=ROSE_COLOR,
            stroke_width=3,
        )
        naive_edge_e = Line(
            start=[1.0, -0.5, 0.0],
            end=[COORDS["E"][0], COORDS["E"][1], 0.0],
            color=ROSE_COLOR,
            stroke_width=3,
        )

        self.play(Create(naive_edge_p), Create(naive_edge_e))
        self.wait(1.5)

        naive_desc = Text(
            "Both edges point left. Clustered!", font_size=16, color=ROSE_COLOR
        ).next_to(naive_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(naive_desc)
        self.play(Write(naive_desc))
        self.wait(2)

        # Fade out Naive representation
        self.play(
            FadeOut(naive_edge_p),
            FadeOut(naive_edge_e),
            FadeOut(naive_title),
            FadeOut(naive_desc),
        )

        # HNSW HEURISTIC SELECTION
        heuristic_title = Text(
            "HNSW Diversity Heuristic Selection", font_size=18, color=EMERALD_COLOR
        ).next_to(mode_text, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(heuristic_title)
        self.play(Write(heuristic_title))
        self.wait(1)

        # 1. Candidate P (d = 0.90)
        pq_items[0].set_color(EMERALD_COLOR)
        heuristic_edge_p = Line(
            start=[1.0, -0.5, 0.0],
            end=[COORDS["P"][0], COORDS["P"][1], 0.0],
            color=EMERALD_COLOR,
            stroke_width=3,
        )

        p_desc = Text(
            "1. Node P is closest. Accept!", font_size=16, color=EMERALD_COLOR
        ).next_to(heuristic_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(p_desc)

        self.play(Create(heuristic_edge_p), Write(p_desc))
        self.play(Flash(self.nodes_l1[1], color=EMERALD_COLOR, flash_radius=0.15))
        self.wait(1.5)
        self.play(FadeOut(p_desc))

        # 2. Candidate E (d = 1.12)
        pq_items[1].set_color(ROSE_COLOR)

        e_desc = Text(
            "2. Node E is closer to P than N.\nd(E, P) = 0.61 < d(E, N) = 1.12\nReject (Redundant)!",
            font_size=16,
            color=ROSE_COLOR,
        ).next_to(heuristic_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(e_desc)

        heuristic_edge_e = Line(
            start=[1.0, -0.5, 0.0],
            end=[COORDS["E"][0], COORDS["E"][1], 0.0],
            color=ROSE_COLOR,
            stroke_width=2,
        )
        self.play(Create(heuristic_edge_e), Write(e_desc))
        self.wait(1.5)
        self.play(Flash(self.nodes_l1[0], color=ROSE_COLOR, flash_radius=0.15))
        self.play(FadeOut(heuristic_edge_e), FadeOut(e_desc))

        # 3. Candidate Q (d = 1.12)
        pq_items[2].set_color(EMERALD_COLOR)

        q_desc = Text(
            "3. Node Q is far from P.\nd(Q, P) = 1.94 > d(Q, N) = 1.12\nAccept (Diverse direction)!",
            font_size=16,
            color=EMERALD_COLOR,
        ).next_to(heuristic_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(q_desc)

        heuristic_edge_q = Line(
            start=[1.0, -0.5, 0.0],
            end=[COORDS["Q"][0], COORDS["Q"][1], 0.0],
            color=EMERALD_COLOR,
            stroke_width=3,
        )
        self.play(Create(heuristic_edge_q), Write(q_desc))
        self.play(Flash(self.nodes_l1[2], color=EMERALD_COLOR, flash_radius=0.15))
        self.wait(2.5)

        # Success! Save these edges on L1
        self.l1_n_edges = VGroup(
            Line(
                start=[1.0, -0.5, 0.0],
                end=[COORDS["P"][0], COORDS["P"][1], 0.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[1.0, -0.5, 0.0],
                end=[COORDS["Q"][0], COORDS["Q"][1], 0.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
        )
        self.add(self.l1_n_edges)

        # Clear out scene drawings
        self.play(
            FadeOut(header),
            FadeOut(mode_text),
            FadeOut(heuristic_title),
            FadeOut(q_desc),
            FadeOut(pq_group),
            FadeOut(heuristic_edge_p),
            FadeOut(heuristic_edge_q),
        )
