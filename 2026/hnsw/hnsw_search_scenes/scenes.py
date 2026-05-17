from manim import *
import numpy as np
from .common import *
from .status import StatusMixin
from .graph import GraphMixin


class HNSWSearchMixin(GraphMixin, StatusMixin):
    def intro_scene(self):
        # 1. Background setup
        self.camera.background_color = BG_COLOR
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        # 2. Title Overlay (fixed in frame)
        title = Text("HNSW Hierarchical Search", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = Text(
            "Visualizing the query routing path", font_size=24, color=GRAY
        )
        subtitle.next_to(title, DOWN, buff=0.2)

        self.camera.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.camera.add_fixed_in_frame_mobjects(subtitle)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def init_search_scene(self):
        # 1. Background setup
        self.camera.background_color = BG_COLOR

        # 2. Camera starting orientation: Flat top-down (2D) with stable zoom = 1.0
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        # 3. Create status bar directly as a fixed-in-frame overlay (completely flat!)
        self.init_status_bar()

        # 4. Create Query Point Q at z=2.0 (initial scale=1.0, center=[0.0, 0.0])
        self.query_line = DashedLine(
            start=[COORD_Q[0], COORD_Q[1], 2.0],
            end=[COORD_Q[0], COORD_Q[1], -2.0],
            color=QUERY_COLOR,
            stroke_width=1.5,
        )

        self.query_pt = Dot(
            point=[COORD_Q[0], COORD_Q[1], 2.0], color=QUERY_COLOR, radius=0.12
        )
        self.query_label = Tex(r"Query $Q$", font_size=20)
        self.query_label.next_to(self.query_pt, DR, buff=0.15)

        # Save track of visited points for the path replay
        self.path_points = []

    # ==================== SCENE 1: Layer 2 Greedy Walk ====================
    def scene_1_l2_walk(self):
        self.wait(1)
        self.update_status("Sparse Top Layer (Layer 2)")

        self.current_center = [0.0, 0.0, 2.0]
        self.current_scale = 1.0

        # Container plane: perfectly matching the screen's 16:9 aspect ratio!
        self.plane_l2 = Rectangle(
            width=12.0,
            height=6.8,
            fill_color=PLANE_L2_COLOR,
            fill_opacity=0.1,
            stroke_color=PLANE_L2_COLOR,
            stroke_width=1.5,
        ).shift(OUT * 2.0)

        l2_nodes_list = ["A", "D", "E", "X"]
        self.nodes_l2_group, self.edges_l2_group, self.nodes_l2_map = (
            self.build_layer_graph(
                l2_nodes_list,
                L2_EDGES,
                2.0,
                NODE_L2_COLOR,
                EDGE_L2_COLOR,
                center=self.current_center,
                scale=self.current_scale,
            )
        )

        # Display Query Point, Plane and Graph
        self.play(
            FadeIn(self.plane_l2),
            FadeIn(self.nodes_l2_group),
            FadeIn(self.edges_l2_group),
        )
        self.play(FadeIn(self.query_pt), FadeIn(self.query_label))
        self.wait(0.5)

        # Introduce Violet Searcher at Node A (Entry Point)
        start_coord = self.get_transformed_coord(
            [COORDS["A"][0], COORDS["A"][1], 2.0],
            self.current_center,
            self.current_scale,
        )
        self.path_points.append(start_coord)

        self.searcher = Dot(point=start_coord, color=SEARCHER_COLOR, radius=0.12)
        self.searcher_ring = Circle(
            radius=0.22, color=SEARCHER_COLOR, stroke_width=2.0
        ).move_to(self.searcher)
        self.searcher_ring.set_shade_in_3d(True)

        entry_label = Tex(r"Entry Point $A$", font_size=18).next_to(
            self.searcher, DL, buff=0.15
        )
        self.play(FadeIn(self.searcher), Create(self.searcher_ring), Write(entry_label))
        self.wait(1.0)
        self.play(FadeOut(entry_label))

        # Greedy Walk steps: A -> D -> E
        self.probe_and_move(
            "A", ["D"], "D", 2.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "D", ["A", "E"], "E", 2.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "E", ["D", "X"], None, 2.0, self.current_center, self.current_scale
        )

        # Mark local minimum
        self.l2_min_label = Tex(r"Local Minimum on $L_2$", font_size=20).next_to(
            self.searcher, UP, buff=0.15
        )
        self.play(Write(self.l2_min_label))
        self.wait(1.5)

    # ==================== SCENE 2: The First Dive (Zoom to L1) ====================
    def scene_2_dive_to_l1(self):
        self.update_status("Diving to Layer 1...")
        self.play(FadeOut(self.l2_min_label))

        # Set new zoom anchor centered at E with scale=1.4
        self.current_center = [COORDS["E"][0], COORDS["E"][1], 0.0]
        self.current_scale = 1.4

        # Re-build beautiful 16:9 plane container and layer graph centered at E's coordinate
        self.plane_l1 = Rectangle(
            width=12.0,
            height=6.8,
            fill_color=PLANE_L1_COLOR,
            fill_opacity=0.1,
            stroke_color=PLANE_L1_COLOR,
            stroke_width=1.5,
        )

        l1_nodes_list = ["A", "D", "E", "X", "H", "I", "K", "Y", "Z"]
        self.nodes_l1_group, self.edges_l1_group, self.nodes_l1_map = (
            self.build_layer_graph(
                l1_nodes_list,
                L1_EDGES,
                0.0,
                NODE_L1_COLOR,
                EDGE_L1_COLOR,
                center=self.current_center,
                scale=self.current_scale,
            )
        )

        # Compute transformed coordinates under the new layout
        new_searcher_pos = self.get_transformed_coord(
            [COORDS["E"][0], COORDS["E"][1], 0.0],
            self.current_center,
            self.current_scale,
        )
        new_query_pos = self.get_transformed_coord(
            [COORD_Q[0], COORD_Q[1], 0.0], self.current_center, self.current_scale
        )

        # Completely seamless and stable cross-fade without camera jitter or title shifting!
        self.play(
            FadeOut(self.plane_l2),
            FadeOut(self.nodes_l2_group),
            FadeOut(self.edges_l2_group),
            FadeIn(self.plane_l1),
            FadeIn(self.nodes_l1_group),
            FadeIn(self.edges_l1_group),
            self.searcher.animate.move_to(new_searcher_pos),
            self.searcher_ring.animate.move_to(new_searcher_pos),
            self.query_pt.animate.move_to(new_query_pos),
            self.query_label.animate.next_to(new_query_pos, DR, buff=0.15),
            run_time=1.5,
        )
        self.wait(1.0)

    # ==================== SCENE 3: Refinement on Layer 1 ====================
    def scene_3_l1_refinement(self):
        self.update_status("Refinement on Layer 1")

        # Greedy search on Layer 1 (scale = 1.4, center = E)
        self.probe_and_move(
            "E", ["D", "X", "H"], "H", 0.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "H", ["D", "E", "I"], "I", 0.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "I", ["H", "K"], "K", 0.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "K", ["I", "Y", "Z"], None, 0.0, self.current_center, self.current_scale
        )

        self.l1_min_label = Tex(r"Local Minimum on $L_1$", font_size=20).next_to(
            self.searcher, UP, buff=0.15
        )
        self.play(Write(self.l1_min_label))
        self.wait(1.5)

    # ==================== SCENE 4: The Final Dive (Zoom to L0) ====================
    def scene_4_dive_to_l0_and_walk(self):
        self.update_status("Final Dive: Layer 0 (Dense Base Layer)")
        self.play(FadeOut(self.l1_min_label))

        # Set new zoom anchor centered at K with scale=2.2
        self.current_center = [COORDS["K"][0], COORDS["K"][1], -2.0]
        self.current_scale = 2.2

        # Re-build beautiful 16:9 plane container and dense layer graph centered at K
        self.plane_l0 = Rectangle(
            width=12.0,
            height=6.8,
            fill_color=PLANE_L0_COLOR,
            fill_opacity=0.1,
            stroke_color=PLANE_L0_COLOR,
            stroke_width=1.5,
        ).shift(OUT * -2.0)

        l0_nodes_list = list(COORDS.keys())
        self.nodes_l0_group, self.edges_l0_group, self.nodes_l0_map = (
            self.build_layer_graph(
                l0_nodes_list,
                L0_EDGES,
                -2.0,
                NODE_L0_COLOR,
                EDGE_L0_COLOR,
                center=self.current_center,
                scale=self.current_scale,
            )
        )

        new_searcher_pos = self.get_transformed_coord(
            [COORDS["K"][0], COORDS["K"][1], -2.0],
            self.current_center,
            self.current_scale,
        )
        new_query_pos = self.get_transformed_coord(
            [COORD_Q[0], COORD_Q[1], -2.0], self.current_center, self.current_scale
        )

        # Seamlessly cross-fade to Layer 0 graph
        self.play(
            FadeOut(self.plane_l1),
            FadeOut(self.nodes_l1_group),
            FadeOut(self.edges_l1_group),
            FadeIn(self.plane_l0),
            FadeIn(self.nodes_l0_group),
            FadeIn(self.edges_l0_group),
            self.searcher.animate.move_to(new_searcher_pos),
            self.searcher_ring.animate.move_to(new_searcher_pos),
            self.query_pt.animate.move_to(new_query_pos),
            self.query_label.animate.next_to(new_query_pos, DR, buff=0.15),
            run_time=1.5,
        )
        self.wait(1.0)

        # Walk on Layer 0 (scale = 2.2, center = K)
        self.update_status("Searching Layer 0...")
        self.probe_and_move(
            "K",
            ["I", "Y", "Z", "R"],
            "R",
            -2.0,
            self.current_center,
            self.current_scale,
        )
        self.probe_and_move(
            "R", ["K", "P"], "P", -2.0, self.current_center, self.current_scale
        )
        self.probe_and_move(
            "P", ["R", "C6"], None, -2.0, self.current_center, self.current_scale
        )

        # Distance line P -> Q (using transformed coordinates)
        p_trans = self.get_transformed_coord(
            [COORDS["P"][0], COORDS["P"][1], -2.0],
            self.current_center,
            self.current_scale,
        )
        self.dist_line = Line(
            start=p_trans, end=new_query_pos, color=PROBE_GREEN, stroke_width=2.5
        )

        self.p_label = Tex(r"Nearest Neighbor $P$", font_size=20).next_to(
            self.searcher, UL, buff=0.1
        )
        self.play(Create(self.dist_line), Write(self.p_label))
        self.wait(2.0)

        # Clean up flat-view temporary overlays
        self.play(FadeOut(self.query_label), FadeOut(self.p_label))

    # ==================== SCENE 5: Path Replay in 3D ====================
    def scene_5_3d_replay(self):
        self.update_status("Replaying Search Path across Layers")

        # Clean up flat-view elements
        self.play(
            FadeOut(self.dist_line),
            FadeOut(self.searcher),
            FadeOut(self.searcher_ring),
            FadeOut(self.nodes_l0_group),
            FadeOut(self.edges_l0_group),
            FadeOut(self.plane_l0),
        )

        # Reset query dot to original 3D coordinates
        self.query_pt.move_to([COORD_Q[0], COORD_Q[1], -2.0])

        # Build the Z-axis query line for the 3D replay stack
        self.query_line = DashedLine(
            start=[COORD_Q[0], COORD_Q[1], 2.0],
            end=[COORD_Q[0], COORD_Q[1], -2.0],
            color=QUERY_COLOR,
            stroke_width=1.5,
        )

        # Re-create all three flat planes at default coordinates (scale=1.0, center=[0.0, 0.0])
        # Layer 2 (z = 2.0)
        self.plane_l2 = Rectangle(
            width=8.0,
            height=6.0,
            fill_color=PLANE_L2_COLOR,
            fill_opacity=0.15,
            stroke_color=PLANE_L2_COLOR,
            stroke_width=1.5,
        ).shift(OUT * 2.0)
        l2_nodes = ["A", "D", "E", "X"]
        nodes_l2_grp, edges_l2_grp, _ = self.build_layer_graph(
            l2_nodes,
            L2_EDGES,
            2.0,
            NODE_L2_COLOR,
            EDGE_L2_COLOR,
            center=[0.0, 0.0, 2.0],
            scale=1.0,
        )

        # Layer 1 (z = 0.0)
        self.plane_l1 = Rectangle(
            width=8.0,
            height=6.0,
            fill_color=PLANE_L1_COLOR,
            fill_opacity=0.15,
            stroke_color=PLANE_L1_COLOR,
            stroke_width=1.5,
        ).shift(OUT * 0.0)
        l1_nodes = ["A", "D", "E", "X", "H", "I", "K", "Y", "Z"]
        nodes_l1_grp, edges_l1_grp, _ = self.build_layer_graph(
            l1_nodes,
            L1_EDGES,
            0.0,
            NODE_L1_COLOR,
            EDGE_L1_COLOR,
            center=[0.0, 0.0, 0.0],
            scale=1.0,
        )

        # Layer 0 (z = -2.0)
        self.plane_l0 = Rectangle(
            width=8.0,
            height=6.0,
            fill_color=PLANE_L0_COLOR,
            fill_opacity=0.15,
            stroke_color=PLANE_L0_COLOR,
            stroke_width=1.5,
        ).shift(OUT * -2.0)
        l0_nodes = list(COORDS.keys())
        nodes_l0_grp, edges_l0_grp, _ = self.build_layer_graph(
            l0_nodes,
            L0_EDGES,
            -2.0,
            NODE_L0_COLOR,
            EDGE_L0_COLOR,
            center=[0.0, 0.0, -2.0],
            scale=1.0,
        )

        # Vertical connectors for projected nodes
        vertical_connectors = VGroup(
            DashedLine(
                start=[COORDS["E"][0], COORDS["E"][1], 2.0],
                end=[COORDS["E"][0], COORDS["E"][1], -2.0],
                color=GRAY,
                stroke_width=1,
            ),
            DashedLine(
                start=[COORDS["K"][0], COORDS["K"][1], 0.0],
                end=[COORDS["K"][0], COORDS["K"][1], -2.0],
                color=GRAY,
                stroke_width=1,
            ),
            DashedLine(
                start=[COORDS["A"][0], COORDS["A"][1], 2.0],
                end=[COORDS["A"][0], COORDS["A"][1], 0.0],
                color=GRAY,
                stroke_width=1,
            ),
            DashedLine(
                start=[COORDS["D"][0], COORDS["D"][1], 2.0],
                end=[COORDS["D"][0], COORDS["D"][1], 0.0],
                color=GRAY,
                stroke_width=1,
            ),
        )

        # Now tilt the camera in 3D!
        # The title remains perfectly flat at the top of the screen because it is in the fixed frame!
        self.move_camera(
            phi=65 * DEGREES,
            theta=-60 * DEGREES,
            zoom=0.85,
            frame_center=[0.0, -0.5, 0.0],
            added_anims=[
                FadeIn(self.plane_l2),
                FadeIn(nodes_l2_grp),
                FadeIn(edges_l2_grp),
                FadeIn(self.plane_l1),
                FadeIn(nodes_l1_grp),
                FadeIn(edges_l1_grp),
                FadeIn(self.plane_l0),
                FadeIn(nodes_l0_grp),
                FadeIn(edges_l0_grp),
                Create(vertical_connectors),
                FadeIn(self.query_line),
            ],
            run_time=2.5,
        )
        self.wait(0.5)

        # 3D Layer Labels on the left (fixed in frame)
        labels = VGroup(
            Tex(r"Layer 2: Sparse Expressway", color=PLANE_L2_COLOR, font_size=20),
            Tex(r"Layer 1: Coarse Navigation", color=PLANE_L1_COLOR, font_size=20),
            Tex(r"Layer 0: Dense Base Data", color=PLANE_L0_COLOR, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        labels.to_corner(UL, buff=0.8)
        self.add_fixed_in_frame_mobjects(labels)
        self.remove(labels)
        self.play(FadeIn(labels, shift=RIGHT))

        # Draw search path hops in 3D
        hop1 = Line(
            start=[COORDS["A"][0], COORDS["A"][1], 2.0],
            end=[COORDS["D"][0], COORDS["D"][1], 2.0],
            color=PATH_L2_COLOR,
            stroke_width=4,
        )
        hop2 = Line(
            start=[COORDS["D"][0], COORDS["D"][1], 2.0],
            end=[COORDS["E"][0], COORDS["E"][1], 2.0],
            color=PATH_L2_COLOR,
            stroke_width=4,
        )
        dive1 = DashedLine(
            start=[COORDS["E"][0], COORDS["E"][1], 2.0],
            end=[COORDS["E"][0], COORDS["E"][1], 0.0],
            color=PATH_L2_COLOR,
            stroke_width=3,
        )

        hop3 = Line(
            start=[COORDS["E"][0], COORDS["E"][1], 0.0],
            end=[COORDS["H"][0], COORDS["H"][1], 0.0],
            color=PATH_L1_COLOR,
            stroke_width=4,
        )
        hop4 = Line(
            start=[COORDS["H"][0], COORDS["H"][1], 0.0],
            end=[COORDS["I"][0], COORDS["I"][1], 0.0],
            color=PATH_L1_COLOR,
            stroke_width=4,
        )
        hop5 = Line(
            start=[COORDS["I"][0], COORDS["I"][1], 0.0],
            end=[COORDS["K"][0], COORDS["K"][1], 0.0],
            color=PATH_L1_COLOR,
            stroke_width=4,
        )
        dive2 = DashedLine(
            start=[COORDS["K"][0], COORDS["K"][1], 0.0],
            end=[COORDS["K"][0], COORDS["K"][1], -2.0],
            color=PATH_L1_COLOR,
            stroke_width=3,
        )

        hop6 = Line(
            start=[COORDS["K"][0], COORDS["K"][1], -2.0],
            end=[COORDS["R"][0], COORDS["R"][1], -2.0],
            color=PATH_L0_COLOR,
            stroke_width=4,
        )
        hop7 = Line(
            start=[COORDS["R"][0], COORDS["R"][1], -2.0],
            end=[COORDS["P"][0], COORDS["P"][1], -2.0],
            color=PATH_L0_COLOR,
            stroke_width=4,
        )

        # Play the hops in sequence
        self.play(Create(hop1), run_time=0.4)
        self.play(Create(hop2), run_time=0.4)
        self.play(Create(dive1), run_time=0.6)
        self.play(Create(hop3), run_time=0.4)
        self.play(Create(hop4), run_time=0.4)
        self.play(Create(hop5), run_time=0.4)
        self.play(Create(dive2), run_time=0.6)
        self.play(Create(hop6), run_time=0.4)
        self.play(Create(hop7), run_time=0.4)

        end_dot = Dot(
            point=[COORDS["P"][0], COORDS["P"][1], -2.0], color=PROBE_GREEN, radius=0.14
        )
        p_q_dist = Line(
            start=[COORDS["P"][0], COORDS["P"][1], -2.0],
            end=[COORD_Q[0], COORD_Q[1], -2.0],
            color=PROBE_GREEN,
            stroke_width=3,
        )
        self.play(FadeIn(end_dot), Create(p_q_dist))
        self.wait(1.0)

        # Cost metrics overlay (fixed in frame)
        hop_count = Tex(
            r"Search cost: $2 + 3 + 2 = 7$ hops", font_size=24, color=SEARCHER_COLOR
        ).to_corner(UR, buff=0.9)
        self.add_fixed_in_frame_mobjects(hop_count)
        self.remove(hop_count)
        self.play(Write(hop_count))
        self.wait(1.0)

        complexity = (
            VGroup(
                Tex(
                    r"Linear scan: 1,000,000 comparisons", font_size=25, color=PROBE_RED
                ),
                Tex(
                    r"HNSW search: $\mathcal{O}(\log N)$ complexity",
                    font_size=25,
                    color=PROBE_GREEN,
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .next_to(hop_count, DOWN, buff=0.4, aligned_edge=LEFT)
        )

        self.add_fixed_in_frame_mobjects(complexity)
        self.remove(complexity)
        self.play(FadeIn(complexity[0], shift=UP), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(complexity[1], shift=UP), run_time=0.8)

        self.wait(4.0)

        # Clean up everything at the end
        self.play(
            FadeOut(self.plane_l2),
            FadeOut(nodes_l2_grp),
            FadeOut(edges_l2_grp),
            FadeOut(self.plane_l1),
            FadeOut(nodes_l1_grp),
            FadeOut(edges_l1_grp),
            FadeOut(self.plane_l0),
            FadeOut(nodes_l0_grp),
            FadeOut(edges_l0_grp),
            FadeOut(vertical_connectors),
            FadeOut(labels),
            FadeOut(hop1),
            FadeOut(hop2),
            FadeOut(dive1),
            FadeOut(hop3),
            FadeOut(hop4),
            FadeOut(hop5),
            FadeOut(dive2),
            FadeOut(hop6),
            FadeOut(hop7),
            FadeOut(end_dot),
            FadeOut(p_q_dist),
            FadeOut(self.query_line),
            FadeOut(self.query_pt),
            FadeOut(hop_count),
            FadeOut(complexity),
            FadeOut(self.status_box),
            FadeOut(self.status_text),
        )
        self.wait(1.5)
