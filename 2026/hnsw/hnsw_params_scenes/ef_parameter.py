from manim import *
from .common import *


class EfParamMixin:
    def get_ef_coord(self, pt, center, scale):
        return np.array([center[0] + pt[0] * scale, center[1] + pt[1] * scale, 0.0])

    def build_ef_graph(self, center, scale, node_color, edge_color):
        nodes_mobjects = {}
        for name, coord in COORDS_EF.items():
            trans_coord = self.get_ef_coord(coord, center, scale)
            dot = Dot(point=trans_coord, color=node_color, radius=0.08)

            # Show labels for structural nodes
            if name in ["E", "B3", "B2", "C1", "C2", "TrueNN"]:
                lbl_text = (
                    "Entry" if name == "E" else ("NN" if name == "TrueNN" else name)
                )
                lbl = MathTex(lbl_text, font_size=16, color=node_color)
                lbl.next_to(dot, UP, buff=0.1)
                nodes_mobjects[name] = VGroup(dot, lbl)
            else:
                nodes_mobjects[name] = VGroup(dot)

        edges_mobjects = VGroup()
        for u, v in EF_EDGES:
            if u in COORDS_EF and v in COORDS_EF:
                start = self.get_ef_coord(COORDS_EF[u], center, scale)
                end = self.get_ef_coord(COORDS_EF[v], center, scale)
                line = Line(start=start, end=end, color=edge_color, stroke_width=1.8)
                edges_mobjects.add(line)

        nodes_group = VGroup(*nodes_mobjects.values())
        return nodes_group, edges_mobjects, nodes_mobjects

    def make_queue_panel(self, center):
        # 1. Glassmorphic Queue panel background card
        panel_bg = RoundedRectangle(
            corner_radius=0.1,
            width=3.2,
            height=4.6,
            fill_color="#0D1117",
            fill_opacity=0.85,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.5,
        ).move_to(center)

        panel_title = Tex("Candidate Queue", font_size=18, color=WHITE).next_to(
            panel_bg.get_top(), DOWN, buff=0.25
        )
        panel_subtitle = Tex(
            "(sorted by dist to Q)", font_size=12, color=SLATE_COLOR
        ).next_to(panel_title, DOWN, buff=0.08)

        panel_group = VGroup(panel_bg, panel_title, panel_subtitle)
        return panel_group

    def render_queue_items(self, queue_data, center_y_start, x_pos):
        items_group = VGroup()
        curr_y = center_y_start - 0.4

        for i, (name, dist) in enumerate(queue_data):
            # Select color based on ordering
            box_color = (
                EMERALD_COLOR if i == 0 else (DARK_SLATE if i < 3 else SLATE_COLOR)
            )
            text_color = WHITE

            box = RoundedRectangle(
                corner_radius=0.05,
                width=2.8,
                height=0.45,
                fill_color="#0F172A",
                fill_opacity=0.8,
                stroke_color=box_color,
                stroke_width=1.2,
            ).move_to([x_pos, curr_y, 0.0])

            lbl_name = "Entry" if name == "E" else ("NN" if name == "TrueNN" else name)
            lbl = Tex(f"{lbl_name}", font_size=15, color=text_color).move_to(
                [x_pos - 0.7, curr_y, 0.0]
            )
            dist_lbl = MathTex(f"d={dist:.2f}", font_size=14, color=box_color).move_to(
                [x_pos + 0.6, curr_y, 0.0]
            )

            # If closest candidate, show the play pointer marker
            if i == 0:
                pointer = (
                    Triangle(
                        color=EMERALD_COLOR, fill_color=EMERALD_COLOR, fill_opacity=1.0
                    )
                    .scale(0.06)
                    .rotate(-90 * DEGREES)
                    .move_to([x_pos - 1.2, curr_y, 0.0])
                )
                item = VGroup(box, lbl, dist_lbl, pointer)
            else:
                item = VGroup(box, lbl, dist_lbl)

            items_group.add(item)
            curr_y -= 0.6

        return items_group

    def run_ef_parameter_scene(self):
        # 1. Setup split screen divider and titles
        divider = Line(
            start=[0.0, 3.8, 0.0],
            end=[0.0, -3.8, 0.0],
            color=DARK_SLATE,
            stroke_width=2,
        )

        left_title = (
            Tex("Greedy Search (efSearch = 1)", font_size=24, color=WHITE)
            .to_corner(UL, buff=0.4)
            .shift(RIGHT * 0.2)
        )
        right_title = (
            Tex("Beam Search (efSearch = 4)", font_size=24, color=WHITE)
            .to_corner(UR, buff=0.4)
            .shift(LEFT * 3.0)
        )

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title))
        self.wait(0.4)

        left_center = [-3.5, 0.0, 0.0]
        right_center = [2.2, 0.0, 0.0]
        queue_center = [5.6, 0.0, 0.0]
        scale = 0.85

        # 2. Build left and right graphs
        left_nodes, left_edges, left_nodes_map = self.build_ef_graph(
            left_center, scale, SLATE_COLOR, DARK_SLATE
        )
        right_nodes, right_edges, right_nodes_map = self.build_ef_graph(
            right_center, scale, SLATE_COLOR, DARK_SLATE
        )

        # 3. Create query points
        q_coord_l = self.get_ef_coord(COORD_Q_EF, left_center, scale)
        q_coord_r = self.get_ef_coord(COORD_Q_EF, right_center, scale)

        q_dot_l = Dot(point=q_coord_l, color=QUERY_COLOR, radius=0.12)
        q_dot_r = Dot(point=q_coord_r, color=QUERY_COLOR, radius=0.12)

        q_label_l = Tex(r"Query $Q$", font_size=18, color=QUERY_COLOR).next_to(
            q_dot_l, DR, buff=0.1
        )
        q_label_r = Tex(r"Query $Q$", font_size=18, color=QUERY_COLOR).next_to(
            q_dot_r, DR, buff=0.1
        )

        # 4. Render Queue UI Background
        queue_ui_bg = self.make_queue_panel(queue_center)

        self.play(
            FadeIn(left_nodes),
            FadeIn(left_edges),
            FadeIn(right_nodes),
            FadeIn(right_edges),
            FadeIn(q_dot_l),
            FadeIn(q_label_l),
            FadeIn(q_dot_r),
            FadeIn(q_label_r),
            FadeIn(queue_ui_bg),
        )
        self.wait(0.5)

        # Helpers for side-specific coordinates
        def get_pt_l(name):
            return self.get_ef_coord(COORDS_EF[name], left_center, scale)

        def get_pt_r(name):
            return self.get_ef_coord(COORDS_EF[name], right_center, scale)

        # 5. Searcher dots
        searcher_l = Dot(point=get_pt_l("E"), color=SEARCHER_COLOR, radius=0.1)
        searcher_r = Dot(point=get_pt_r("E"), color=SEARCHER_COLOR, radius=0.1)

        ring_l = Circle(radius=0.18, color=SEARCHER_COLOR, stroke_width=1.5).move_to(
            searcher_l
        )
        ring_r = Circle(radius=0.18, color=SEARCHER_COLOR, stroke_width=1.5).move_to(
            searcher_r
        )

        self.play(
            FadeIn(searcher_l), Create(ring_l), FadeIn(searcher_r), Create(ring_r)
        )
        self.wait(0.8)

        # Queue panel top position
        queue_start_y = queue_ui_bg[0].get_top()[1] - 0.4
        queue_x = queue_center[0]

        # Live Queue tracker
        current_queue = []
        queue_mobjects = VGroup()

        # --- Step 1 ---
        # Both sides probe crescent nodes from E
        probes_l = VGroup(
            *[
                Line(
                    get_pt_l("E"), get_pt_l(nbr), color=EMERALD_COLOR, stroke_width=2.2
                )
                for nbr in ["B1", "B2", "B3", "B4", "B5"]
            ]
        )
        probes_r = VGroup(
            *[
                Line(
                    get_pt_r("E"), get_pt_r(nbr), color=EMERALD_COLOR, stroke_width=2.2
                )
                for nbr in ["B1", "B2", "B3", "B4", "B5"]
            ]
        )

        self.play(Create(probes_l), Create(probes_r), run_time=0.4)
        self.wait(0.2)

        # Populate Queue for Right Side:
        # Distances to Q (2.0, 0.0):
        # B3 (-0.1, 0.0) -> d=2.1
        # B2 (-0.3, 0.6), B4 (-0.3, -0.6) -> d=2.4
        # B1 (-0.9, 1.2), B5 (-0.9, -1.2) -> d=3.2
        current_queue = [
            ("B3", 2.1),
            ("B2", 2.4),
            ("B4", 2.4),
            ("B1", 3.2),
            ("B5", 3.2),
        ]
        new_queue_mobs = self.render_queue_items(
            current_queue[:4], queue_start_y, queue_x
        )

        self.play(
            searcher_l.animate.move_to(get_pt_l("B3")),
            ring_l.animate.move_to(get_pt_l("B3")),
            searcher_r.animate.move_to(get_pt_r("B3")),
            ring_r.animate.move_to(get_pt_r("B3")),
            FadeIn(new_queue_mobs, shift=LEFT),
            FadeOut(probes_l),
            FadeOut(probes_r),
            run_time=0.8,
        )
        queue_mobjects = new_queue_mobs
        self.wait(0.6)

        # --- Step 2 ---
        # Greedy vs Beam split behavior:
        # Left (Greedy): probes B2 and B4 from B3. Both are red (further).
        probe_l_b2 = Line(
            get_pt_l("B3"), get_pt_l("B2"), color=ROSE_COLOR, stroke_width=2.2
        )
        probe_l_b4 = Line(
            get_pt_l("B3"), get_pt_l("B4"), color=ROSE_COLOR, stroke_width=2.2
        )

        # Right (Beam): also probes B2 and B4 from B3 (red), but Pops B3 and Backtracks to next best candidate: B2!
        probe_r_b2 = Line(
            get_pt_r("B3"), get_pt_r("B2"), color=ROSE_COLOR, stroke_width=2.2
        )
        probe_r_b4 = Line(
            get_pt_r("B3"), get_pt_r("B4"), color=ROSE_COLOR, stroke_width=2.2
        )

        self.play(
            Create(probe_l_b2),
            Create(probe_l_b4),
            Create(probe_r_b2),
            Create(probe_r_b4),
            run_time=0.4,
        )
        self.wait(0.3)

        # Greedy stuck ring and label
        stuck_ring = Circle(radius=0.25, color=ROSE_COLOR, stroke_width=2.0).move_to(
            get_pt_l("B3")
        )
        stuck_lbl = Tex("Stuck — Local Min", font_size=18, color=ROSE_COLOR).next_to(
            searcher_l, DOWN, buff=0.1
        )

        # Animate backtrack on Right (pop B3, new queue starts with B2, searcher moves to B2)
        current_queue = [("B2", 2.4), ("B4", 2.4), ("B1", 3.2), ("B5", 3.2)]
        next_queue_mobs = self.render_queue_items(
            current_queue[:4], queue_start_y, queue_x
        )

        # Animate backtracking movement: draw a dotted line indicating backtracking jump from B3 to B2
        backtrack_line = DashedLine(
            get_pt_r("B3"), get_pt_r("B2"), color=SEARCHER_COLOR, stroke_width=1.5
        )

        self.play(
            Create(stuck_ring),
            Write(stuck_lbl),
            searcher_l.animate.set_color(ROSE_COLOR),
            ring_l.animate.set_color(ROSE_COLOR),
            FadeOut(probe_l_b2),
            FadeOut(probe_l_b4),
            FadeOut(probe_r_b2),
            FadeOut(probe_r_b4),
            Create(backtrack_line),
            Transform(queue_mobjects, next_queue_mobs),
            run_time=0.7,
        )
        self.wait(0.2)

        # Move searcher to B2
        self.play(
            searcher_r.animate.move_to(get_pt_r("B2")),
            ring_r.animate.move_to(get_pt_r("B2")),
            FadeOut(backtrack_line),
            run_time=0.6,
        )
        self.wait(0.4)

        # --- Step 3 ---
        # Right (Beam) is at B2. Probes B1 (red) and C1 (green!)
        probe_r_b1 = Line(
            get_pt_r("B2"), get_pt_r("B1"), color=ROSE_COLOR, stroke_width=2.2
        )
        probe_r_c1 = Line(
            get_pt_r("B2"), get_pt_r("C1"), color=EMERALD_COLOR, stroke_width=2.2
        )

        self.play(Create(probe_r_b1), Create(probe_r_c1), run_time=0.4)
        self.wait(0.2)

        # Pop B2, Push C1 (dist to Q = 2.1)
        # Queue: C1 (2.1), B4 (2.4), B1 (3.2), B5 (3.2)
        current_queue = [("C1", 2.1), ("B4", 2.4), ("B1", 3.2), ("B5", 3.2)]
        next_queue_mobs = self.render_queue_items(
            current_queue[:4], queue_start_y, queue_x
        )

        self.play(
            searcher_r.animate.move_to(get_pt_r("C1")),
            ring_r.animate.move_to(get_pt_r("C1")),
            FadeOut(probe_r_b1),
            FadeOut(probe_r_c1),
            Transform(queue_mobjects, next_queue_mobs),
            run_time=0.7,
        )
        self.wait(0.4)

        # --- Step 4 ---
        # Right (Beam) is at C1. Probes C2 (green!)
        probe_r_c2 = Line(
            get_pt_r("C1"), get_pt_r("C2"), color=EMERALD_COLOR, stroke_width=2.2
        )
        self.play(Create(probe_r_c2), run_time=0.4)

        # Pop C1, Push C2 (dist = 1.1)
        # Queue: C2 (1.1), B4 (2.4), B1 (3.2), B5 (3.2)
        current_queue = [("C2", 1.1), ("B4", 2.4), ("B1", 3.2), ("B5", 3.2)]
        next_queue_mobs = self.render_queue_items(
            current_queue[:4], queue_start_y, queue_x
        )

        self.play(
            searcher_r.animate.move_to(get_pt_r("C2")),
            ring_r.animate.move_to(get_pt_r("C2")),
            FadeOut(probe_r_c2),
            Transform(queue_mobjects, next_queue_mobs),
            run_time=0.7,
        )
        self.wait(0.4)

        # --- Step 5 ---
        # Right (Beam) is at C2. Probes TrueNN (green!)
        probe_r_nn = Line(
            get_pt_r("C2"), get_pt_r("TrueNN"), color=EMERALD_COLOR, stroke_width=2.2
        )
        self.play(Create(probe_r_nn), run_time=0.4)

        # Pop C2, Push TrueNN (dist = 0.3)
        # Queue: TrueNN (0.3), B4 (2.4), B1 (3.2), B5 (3.2)
        current_queue = [("TrueNN", 0.3), ("B4", 2.4), ("B1", 3.2), ("B5", 3.2)]
        next_queue_mobs = self.render_queue_items(
            current_queue[:4], queue_start_y, queue_x
        )

        # Emerald success markers for Right
        found_ring = Circle(radius=0.25, color=EMERALD_COLOR, stroke_width=2.0).move_to(
            get_pt_r("TrueNN")
        )
        found_lbl = Tex("NN Found", font_size=18, color=EMERALD_COLOR).next_to(
            searcher_r, DOWN, buff=0.1
        )

        self.play(
            searcher_r.animate.move_to(get_pt_r("TrueNN")),
            ring_r.animate.move_to(get_pt_r("TrueNN")),
            searcher_r.animate.set_color(EMERALD_COLOR),
            ring_r.animate.set_color(EMERALD_COLOR),
            FadeOut(probe_r_nn),
            Transform(queue_mobjects, next_queue_mobs),
            Create(found_ring),
            Write(found_lbl),
            run_time=0.7,
        )
        self.wait(2.2)

        # 6. Dissolve Scene 3
        self.play(
            FadeOut(divider),
            FadeOut(left_title),
            FadeOut(right_title),
            FadeOut(left_nodes),
            FadeOut(left_edges),
            FadeOut(right_nodes),
            FadeOut(right_edges),
            FadeOut(q_dot_l),
            FadeOut(q_label_l),
            FadeOut(q_dot_r),
            FadeOut(q_label_r),
            FadeOut(searcher_l),
            FadeOut(ring_l),
            FadeOut(searcher_r),
            FadeOut(ring_r),
            FadeOut(stuck_ring),
            FadeOut(stuck_lbl),
            FadeOut(found_ring),
            FadeOut(found_lbl),
            FadeOut(queue_ui_bg),
            FadeOut(queue_mobjects),
            run_time=0.8,
        )
        self.wait(0.5)
