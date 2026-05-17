from manim import *
from .common import *


class MParamMixin:
    def get_side_coord(self, pt, side_center, scale):
        return np.array(
            [side_center[0] + pt[0] * scale, side_center[1] + pt[1] * scale, 0.0]
        )

    def build_side_graph(self, side_center, scale, edges_list, node_color, edge_color):
        nodes_mobjects = {}
        for name, coord in COORDS_M.items():
            trans_coord = self.get_side_coord(coord, side_center, scale)
            dot = Dot(point=trans_coord, color=node_color, radius=0.07)

            # Show labels only for search nodes to keep visual clean
            if name in ["N0", "N6", "N8", "N14"]:
                # Short names for presentation
                lbl_text = "Entry" if name == "N0" else name
                lbl = MathTex(lbl_text, font_size=14, color=node_color)
                lbl.next_to(dot, UP, buff=0.1)
                nodes_mobjects[name] = VGroup(dot, lbl)
            else:
                nodes_mobjects[name] = VGroup(dot)

        edges_mobjects = VGroup()
        for u, v in edges_list:
            if u in COORDS_M and v in COORDS_M:
                start = self.get_side_coord(COORDS_M[u], side_center, scale)
                end = self.get_side_coord(COORDS_M[v], side_center, scale)
                line = Line(start=start, end=end, color=edge_color, stroke_width=1.5)
                edges_mobjects.add(line)

        nodes_group = VGroup(*nodes_mobjects.values())
        return nodes_group, edges_mobjects, nodes_mobjects

    def run_m_parameter_scene(self):
        # 1. Setup split screen divider and titles
        divider = Line(
            start=[0.0, 3.8, 0.0],
            end=[0.0, -3.8, 0.0],
            color=DARK_SLATE,
            stroke_width=2,
        )

        left_title = (
            Tex("Low M (M = 2)", font_size=28, color=WHITE)
            .to_corner(UL, buff=0.4)
            .shift(RIGHT * 0.5)
        )
        right_title = (
            Tex("High M (M = 6)", font_size=28, color=WHITE)
            .to_corner(UR, buff=0.4)
            .shift(LEFT * 0.5)
        )

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title))
        self.wait(0.4)

        # Centers and scale for left/right graphs
        left_center = [-3.4, 0.0, 0.0]
        right_center = [3.4, 0.0, 0.0]
        scale = 0.85

        # 2. Build left and right graphs
        left_nodes, left_edges, left_nodes_map = self.build_side_graph(
            left_center, scale, LOW_M_EDGES, SLATE_COLOR, DARK_SLATE
        )
        right_nodes, right_edges, right_nodes_map = self.build_side_graph(
            right_center, scale, HIGH_M_EDGES, SLATE_COLOR, DARK_SLATE
        )

        # 3. Create query points on both sides
        q_coord_l = self.get_side_coord(COORD_Q_M, left_center, scale)
        q_coord_r = self.get_side_coord(COORD_Q_M, right_center, scale)

        q_dot_l = Dot(point=q_coord_l, color=QUERY_COLOR, radius=0.12)
        q_dot_r = Dot(point=q_coord_r, color=QUERY_COLOR, radius=0.12)

        q_label_l = Tex(r"Query $Q$", font_size=18, color=QUERY_COLOR).next_to(
            q_dot_l, DR, buff=0.1
        )
        q_label_r = Tex(r"Query $Q$", font_size=18, color=QUERY_COLOR).next_to(
            q_dot_r, DR, buff=0.1
        )

        self.play(
            FadeIn(left_nodes),
            FadeIn(left_edges),
            FadeIn(right_nodes),
            FadeIn(right_edges),
            FadeIn(q_dot_l),
            FadeIn(q_label_l),
            FadeIn(q_dot_r),
            FadeIn(q_label_r),
        )
        self.wait(0.5)

        # 4. Searchers starting at N0 (Entry Node)
        n0_coord_l = self.get_side_coord(COORDS_M["N0"], left_center, scale)
        n0_coord_r = self.get_side_coord(COORDS_M["N0"], right_center, scale)

        searcher_l = Dot(point=n0_coord_l, color=SEARCHER_COLOR, radius=0.1)
        searcher_r = Dot(point=n0_coord_r, color=SEARCHER_COLOR, radius=0.1)

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

        # Define step coordinate helper to clean up walk loops
        def get_pt_l(name):
            return self.get_side_coord(COORDS_M[name], left_center, scale)

        def get_pt_r(name):
            return self.get_side_coord(COORDS_M[name], right_center, scale)

        # Simultaneously animate hops
        # --- Step 1 ---
        # Left: N0 -> N1 (probes N1)
        # Right: N0 -> N8 (probes N1, N8)
        probe_l1 = Line(
            start=n0_coord_l, end=get_pt_l("N1"), color=EMERALD_COLOR, stroke_width=2.5
        )
        probe_r1_1 = Line(
            start=n0_coord_r, end=get_pt_r("N1"), color=EMERALD_COLOR, stroke_width=2.5
        )
        probe_r1_8 = Line(
            start=n0_coord_r, end=get_pt_r("N8"), color=EMERALD_COLOR, stroke_width=2.5
        )

        self.play(
            Create(probe_l1), Create(probe_r1_1), Create(probe_r1_8), run_time=0.4
        )
        self.wait(0.2)

        self.play(
            searcher_l.animate.move_to(get_pt_l("N1")),
            ring_l.animate.move_to(get_pt_l("N1")),
            searcher_r.animate.move_to(get_pt_r("N8")),
            ring_r.animate.move_to(get_pt_r("N8")),
            FadeOut(probe_l1),
            FadeOut(probe_r1_1),
            FadeOut(probe_r1_8),
            run_time=0.7,
        )
        self.wait(0.3)

        # --- Step 2 ---
        # Left: N1 -> N2 (probes N0-red, N2-green)
        # Right: N8 -> N14 (probes N0-red, N12-red, N14-green)
        probe_l2_0 = Line(
            start=get_pt_l("N1"), end=get_pt_l("N0"), color=ROSE_COLOR, stroke_width=2.5
        )
        probe_l2_2 = Line(
            start=get_pt_l("N1"),
            end=get_pt_l("N2"),
            color=EMERALD_COLOR,
            stroke_width=2.5,
        )

        probe_r2_0 = Line(
            start=get_pt_r("N8"), end=get_pt_r("N0"), color=ROSE_COLOR, stroke_width=2.5
        )
        probe_r2_12 = Line(
            start=get_pt_r("N8"),
            end=get_pt_r("N12"),
            color=ROSE_COLOR,
            stroke_width=2.5,
        )
        probe_r2_14 = Line(
            start=get_pt_r("N8"),
            end=get_pt_r("N14"),
            color=EMERALD_COLOR,
            stroke_width=2.5,
        )

        self.play(
            Create(probe_l2_0),
            Create(probe_l2_2),
            Create(probe_r2_0),
            Create(probe_r2_12),
            Create(probe_r2_14),
            run_time=0.4,
        )
        self.wait(0.2)

        success_text = Tex(
            "Success — 2 hops", font_size=20, color=EMERALD_COLOR
        ).next_to(searcher_r, UR, buff=0.15)
        success_ring = Circle(
            radius=0.25, color=EMERALD_COLOR, stroke_width=2.0
        ).move_to(get_pt_r("N14"))

        self.play(
            searcher_l.animate.move_to(get_pt_l("N2")),
            ring_l.animate.move_to(get_pt_l("N2")),
            searcher_r.animate.move_to(get_pt_r("N14")),
            ring_r.animate.move_to(get_pt_r("N14")),
            FadeOut(probe_l2_0),
            FadeOut(probe_l2_2),
            FadeOut(probe_r2_0),
            FadeOut(probe_r2_12),
            FadeOut(probe_r2_14),
            run_time=0.7,
        )

        # Right lands on true NN! Display Emerald success feedback
        self.play(
            Create(success_ring),
            Write(success_text),
            searcher_r.animate.set_color(EMERALD_COLOR),
            ring_r.animate.set_color(EMERALD_COLOR),
        )
        self.wait(0.4)

        # --- Steps 3 to 6: Left continues walking, Right remains idle in success ---
        path_l = ["N2", "N3", "N4", "N5", "N6"]
        for i in range(len(path_l) - 1):
            curr = path_l[i]
            nxt = path_l[i + 1]
            # Probe from curr to nxt
            probe_ok = Line(
                start=get_pt_l(curr),
                end=get_pt_l(nxt),
                color=EMERALD_COLOR,
                stroke_width=2.5,
            )
            self.play(Create(probe_ok), run_time=0.3)
            self.play(
                searcher_l.animate.move_to(get_pt_l(nxt)),
                ring_l.animate.move_to(get_pt_l(nxt)),
                FadeOut(probe_ok),
                run_time=0.5,
            )
            self.wait(0.1)

        # Left gets trapped at N6!
        # Probe neighbor N5 (red)
        probe_fail = Line(
            start=get_pt_l("N6"), end=get_pt_l("N5"), color=ROSE_COLOR, stroke_width=2.5
        )
        self.play(Create(probe_fail), run_time=0.3)
        self.wait(0.2)
        self.play(FadeOut(probe_fail), run_time=0.3)

        trapped_text = Tex(
            "Trapped — Recall Failure", font_size=20, color=ROSE_COLOR
        ).next_to(searcher_l, DL, buff=0.15)
        trapped_ring = Circle(radius=0.25, color=ROSE_COLOR, stroke_width=2.0).move_to(
            get_pt_l("N6")
        )

        self.play(
            Create(trapped_ring),
            Write(trapped_text),
            searcher_l.animate.set_color(ROSE_COLOR),
            ring_l.animate.set_color(ROSE_COLOR),
        )
        self.wait(1.5)

        # 5. Fade in the punchline text
        comparison_label = Tex(
            "Same data. Same query. Different graph.", font_size=24, color=WHITE
        ).to_edge(DOWN, buff=0.4)

        # Glow effect
        comparison_bg = RoundedRectangle(
            corner_radius=0.1,
            width=8.0,
            height=0.6,
            fill_color="#0D1117",
            fill_opacity=0.9,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.0,
        ).move_to(comparison_label)

        self.play(FadeIn(comparison_bg), Write(comparison_label))
        self.wait(2.2)

        # 6. Dissolve Scene 2
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
            FadeOut(success_ring),
            FadeOut(success_text),
            FadeOut(trapped_ring),
            FadeOut(trapped_text),
            FadeOut(comparison_bg),
            FadeOut(comparison_label),
            run_time=0.8,
        )
        self.wait(0.5)
