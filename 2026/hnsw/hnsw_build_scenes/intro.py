from manim import *
from .common import *


class IntroSceneMixin:
    def intro_scene(self):
        # Title Overlay (fixed in frame)
        title = Text("HNSW Index Construction", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = Text(
            "How elements find their layers and connect", font_size=24, color=GRAY
        )
        subtitle.next_to(title, DOWN, buff=0.2)

        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.add_fixed_in_frame_mobjects(subtitle)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # --- Create 3D Planes for Layers ---
        # L2 (Top, z = 2)
        self.plane_l2 = Rectangle(
            width=7.5,
            height=5.0,
            fill_color=PLANE_L2_COLOR,
            fill_opacity=0.15,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).shift(OUT * 2)

        # L1 (Middle, z = 0)
        self.plane_l1 = Rectangle(
            width=7.5,
            height=5.0,
            fill_color=PLANE_L1_COLOR,
            fill_opacity=0.15,
            stroke_color=WHITE,
            stroke_width=1.5,
        )

        # L0 (Bottom, z = -2)
        self.plane_l0 = Rectangle(
            width=7.5,
            height=5.0,
            fill_color=PLANE_L0_COLOR,
            fill_opacity=0.15,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).shift(OUT * -2)

        # --- Create Nodes on Planes ---
        # Layer 2 Nodes (Only E)
        self.nodes_l2 = VGroup(
            Dot(
                point=[COORDS["E"][0], COORDS["E"][1], 2.0],
                color=NODE_COLOR,
                radius=0.08,
            )
        )

        # Layer 1 Nodes (E, P, Q, B, D)
        self.nodes_l1 = VGroup(
            *[
                Dot(
                    point=[COORDS[k][0], COORDS[k][1], 0.0],
                    color=NODE_COLOR,
                    radius=0.08,
                )
                for k in ["E", "P", "Q", "B", "D"]
            ]
        )

        # Layer 0 Nodes (All nodes)
        self.nodes_l0 = VGroup(
            *[
                Dot(
                    point=[COORDS[k][0], COORDS[k][1], -2.0],
                    color=NODE_COLOR,
                    radius=0.08,
                )
                for k in COORDS.keys()
            ]
        )

        # --- Create Node Labels on Planes ---
        # Layer 2 Labels
        self.labels_l2 = VGroup(
            *[
                Text(k, font_size=14, color=NODE_COLOR).move_to(
                    [COORDS[k][0], COORDS[k][1] + 0.25, 2.0]
                )
                for k in ["E"]
            ]
        )

        # Layer 1 Labels
        self.labels_l1 = VGroup(
            *[
                Text(k, font_size=14, color=NODE_COLOR).move_to(
                    [COORDS[k][0], COORDS[k][1] + 0.25, 0.0]
                )
                for k in ["E", "P", "Q", "B", "D"]
            ]
        )

        # Layer 0 Labels
        self.labels_l0 = VGroup(
            *[
                Text(k, font_size=14, color=NODE_COLOR).move_to(
                    [COORDS[k][0], COORDS[k][1] + 0.25, -2.0]
                )
                for k in COORDS.keys()
            ]
        )

        # --- Create Edges on Planes ---
        # L1 Edges (E-D, E-B, D-B)
        self.edges_l1 = VGroup(
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], 0.0],
                end=[COORDS["D"][0], COORDS["D"][1], 0.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], 0.0],
                end=[COORDS["B"][0], COORDS["B"][1], 0.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["D"][0], COORDS["D"][1], 0.0],
                end=[COORDS["B"][0], COORDS["B"][1], 0.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
        )

        # L0 Edges
        self.edges_l0 = VGroup(
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], -2.0],
                end=[COORDS["D"][0], COORDS["D"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], -2.0],
                end=[COORDS["B"][0], COORDS["B"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], -2.0],
                end=[COORDS["A"][0], COORDS["A"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["E"][0], COORDS["E"][1], -2.0],
                end=[COORDS["F"][0], COORDS["F"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["D"][0], COORDS["D"][1], -2.0],
                end=[COORDS["B"][0], COORDS["B"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["D"][0], COORDS["D"][1], -2.0],
                end=[COORDS["G"][0], COORDS["G"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["B"][0], COORDS["B"][1], -2.0],
                end=[COORDS["G"][0], COORDS["G"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["B"][0], COORDS["B"][1], -2.0],
                end=[COORDS["C"][0], COORDS["C"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["A"][0], COORDS["A"][1], -2.0],
                end=[COORDS["C"][0], COORDS["C"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["A"][0], COORDS["A"][1], -2.0],
                end=[COORDS["F"][0], COORDS["F"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["C"][0], COORDS["C"][1], -2.0],
                end=[COORDS["G"][0], COORDS["G"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
            Line(
                start=[COORDS["C"][0], COORDS["C"][1], -2.0],
                end=[COORDS["F"][0], COORDS["F"][1], -2.0],
                color=EDGE_COLOR,
                stroke_width=2,
            ),
        )

        # --- Vertical Dashed Connectors ---
        self.vertical_connectors = VGroup(
            # Node E duplicate line
            DashedLine(
                start=[COORDS["E"][0], COORDS["E"][1], 2.0],
                end=[COORDS["E"][0], COORDS["E"][1], -2.0],
                color=GRAY,
                stroke_width=1,
            ),
            # Node B, D, P, Q duplicate lines
            *[
                DashedLine(
                    start=[COORDS[k][0], COORDS[k][1], 0.0],
                    end=[COORDS[k][0], COORDS[k][1], -2.0],
                    color=GRAY,
                    stroke_width=1,
                )
                for k in ["B", "D", "P", "Q"]
            ]
        )

        # --- Animate Elements ---
        self.play(
            FadeIn(self.plane_l0),
            FadeIn(self.nodes_l0),
            FadeIn(self.labels_l0),
            FadeIn(self.edges_l0),
        )
        self.wait(0.5)
        self.play(
            FadeIn(self.plane_l1),
            FadeIn(self.nodes_l1),
            FadeIn(self.labels_l1),
            FadeIn(self.edges_l1),
        )
        self.wait(0.5)
        self.play(
            FadeIn(self.plane_l2),
            FadeIn(self.nodes_l2),
            FadeIn(self.labels_l2),
        )
        self.play(Create(self.vertical_connectors))

        # Display static labels on the side
        labels_group = (
            VGroup(
                Text("Layer 2: Sparse Expressway", font_size=30, color=PLANE_L2_COLOR),
                Text("Layer 1: Coarse Navigation", font_size=30, color=PLANE_L1_COLOR),
                Text("Layer 0: Dense Base Data", font_size=30, color=PLANE_L0_COLOR),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .to_corner(UL)
        )

        self.add_fixed_in_frame_mobjects(labels_group)
        self.play(FadeIn(labels_group, shift=RIGHT))
        self.wait(2.5)

        # Cleanup labels for next scene
        self.play(FadeOut(labels_group))
