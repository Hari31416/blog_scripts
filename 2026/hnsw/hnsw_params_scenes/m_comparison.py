from manim import *

from .common import *


class MComparisonMixin:
    def animate_path(self, searcher, points, shifted, color, run_time=0.6):
        trail = VGroup()
        for start_name, end_name in zip(points, points[1:]):
            segment = Line(
                shifted[start_name], shifted[end_name], color=color, stroke_width=4
            )
            trail.add(segment)
            self.play(
                Create(segment),
                searcher.animate.move_to(shifted[end_name]),
                run_time=run_time,
                rate_func=smooth,
            )
        return trail

    def m_parameter_scene(self):
        self.play(
            self.m_card.knob.animate.move_to(self.m_card.knob_positions[2]),
            self.m_card.glow.animate.move_to(self.m_card.knob_positions[2]),
            Transform(
                self.m_card.value_label,
                Text("M = 2", font_size=18, color=M_COLOR, weight=BOLD).move_to(
                    self.m_card.value_label
                ),
            ),
            run_time=0.8,
        )

        divider = Line(UP * 2.45, DOWN * 3.2, color=PANEL_STROKE, stroke_width=2)
        divider.set_glow_factor(0.25)
        left_frame, left_title = make_panel(LEFT_CENTER, "Low M  (M = 2)")
        right_frame, right_title = make_panel(RIGHT_CENTER, "High M  (M = 6)")

        left_edges, left_nodes, left_map, left_shifted = make_graph(
            M_NODES, M_LOW_EDGES, LEFT_CENTER
        )
        right_edges, right_nodes, right_map, right_shifted = make_graph(
            M_NODES, M_LOW_EDGES + M_HIGH_EXTRA_EDGES, RIGHT_CENTER
        )

        left_query = make_query(left_shifted[M_TARGET], label_dir=UR)
        right_query = make_query(right_shifted[M_TARGET], label_dir=UR)
        left_searcher = make_searcher(left_shifted[M_LOW_PATH[0]])
        right_searcher = make_searcher(right_shifted[M_HIGH_PATH[0]])

        same_note = Text(
            "Same data and same query but different graph.",
            font_size=22,
            color=SOFT_GREY,
            weight=BOLD,
        ).to_edge(DOWN, buff=0.38)

        self.play(
            FadeIn(divider),
            FadeIn(left_frame),
            FadeIn(right_frame),
            FadeIn(left_title, shift=DOWN * 0.1),
            FadeIn(right_title, shift=DOWN * 0.1),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                FadeIn(left_edges),
                FadeIn(right_edges),
                FadeIn(left_nodes),
                FadeIn(right_nodes),
                FadeIn(left_query),
                FadeIn(right_query),
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        self.play(FadeIn(left_searcher), FadeIn(right_searcher), run_time=0.5)

        left_trail = self.animate_path(
            left_searcher, M_LOW_PATH, left_shifted, SEARCHER_COLOR, 0.5
        )
        right_trail = self.animate_path(
            right_searcher, M_HIGH_PATH, right_shifted, SUCCESS_COLOR, 0.8
        )

        left_fail = make_badge("Trapped - Recall Failure", FAIL_COLOR)
        left_fail.next_to(left_frame, DOWN, buff=-0.6)
        right_ok = make_badge("Success - 2 steps", SUCCESS_COLOR)
        right_ok.next_to(right_frame, DOWN, buff=-0.6)

        left_ring = DashedVMobject(
            Circle(radius=0.34, color=FAIL_COLOR).move_to(left_shifted[M_LOW_PATH[-1]]),
            num_dashes=24,
        )
        right_ring = Circle(radius=0.34, color=SUCCESS_COLOR, stroke_width=3).move_to(
            right_shifted[M_TARGET]
        )

        self.play(
            Create(left_ring),
            Create(right_ring),
            FadeIn(left_fail, shift=UP * 0.1),
            FadeIn(right_ok, shift=UP * 0.1),
            run_time=0.8,
        )
        self.play(Write(same_note))
        self.wait(1.4)

        self.play(
            self.m_card.knob.animate.move_to(self.m_card.knob_positions[6]),
            self.m_card.glow.animate.move_to(self.m_card.knob_positions[6]),
            Transform(
                self.m_card.value_label,
                Text("M = 6", font_size=18, color=M_COLOR, weight=BOLD).move_to(
                    self.m_card.value_label
                ),
            ),
            run_time=0.8,
        )
        self.wait(0.3)
        self.play(
            FadeOut(
                VGroup(
                    divider,
                    left_frame,
                    right_frame,
                    left_title,
                    right_title,
                    left_edges,
                    right_edges,
                    left_nodes,
                    right_nodes,
                    left_query,
                    right_query,
                    left_searcher,
                    right_searcher,
                    left_trail,
                    right_trail,
                    left_fail,
                    right_ok,
                    left_ring,
                    right_ring,
                    same_note,
                )
            ),
            run_time=0.9,
        )
