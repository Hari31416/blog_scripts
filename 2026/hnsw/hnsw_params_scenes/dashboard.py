from manim import *
from .common import *


class DashboardMixin:
    def run_dashboard_scene(self):
        # 1. Title at the top
        title = Tex("HNSW Hyperparameters", font_size=36, color=WHITE).to_edge(
            UP, buff=0.6
        )

        # 2. Modern glassmorphic control card
        dashboard_card = RoundedRectangle(
            corner_radius=0.15,
            width=9.5,
            height=4.6,
            fill_color="#0D1117",
            fill_opacity=0.85,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.5,
        ).shift(DOWN * 0.2)

        self.play(Write(title), FadeIn(dashboard_card))
        self.wait(0.4)

        # 3. M Slider elements
        # Position M track at y = 1.0, labels around it
        m_label = MathTex(
            r"M \text{ (Max Connections per Node)}", font_size=22, color=WHITE
        )
        m_label.move_to([-1.5, 1.4, 0.0])

        m_value_display = MathTex(r"M = 16", font_size=22, color=EMERALD_COLOR)
        m_value_display.move_to([3.0, 1.4, 0.0])

        m_track = Line(
            start=[-3.5, 0.9, 0.0],
            end=[3.5, 0.9, 0.0],
            color=DARK_SLATE,
            stroke_width=4.0,
        )

        # Ticks for M track
        m_tick_left = Line(
            [-3.5, 0.75, 0], [-3.5, 1.05, 0], color=SLATE_COLOR, stroke_width=2
        )
        m_tick_right = Line(
            [3.5, 0.75, 0], [3.5, 1.05, 0], color=SLATE_COLOR, stroke_width=2
        )
        m_val_left = MathTex("2", font_size=16, color=SLATE_COLOR).next_to(
            m_tick_left, DOWN, buff=0.1
        )
        m_val_right = MathTex("64", font_size=16, color=SLATE_COLOR).next_to(
            m_tick_right, DOWN, buff=0.1
        )

        # Knob starts at 16 (let's say it's placed at x = -1.5)
        m_knob = Dot(point=[-1.5, 0.9, 0.0], color=EMERALD_COLOR, radius=0.14)

        m_definition = Tex(
            r"$\rightarrow$ controls how many connections each node can form",
            font_size=18,
            color=SLATE_COLOR,
        )
        m_definition.move_to([-0.5, 0.3, 0.0])

        # Animate M Slider
        self.play(
            FadeIn(m_label),
            Create(m_track),
            Create(m_tick_left),
            Create(m_tick_right),
            FadeIn(m_val_left),
            FadeIn(m_val_right),
        )
        self.play(FadeIn(m_knob), FadeIn(m_value_display))
        self.play(
            Flash(
                m_knob,
                color=EMERALD_COLOR,
                line_length=0.25,
                num_lines=8,
                flash_radius=0.2,
            )
        )
        self.play(FadeIn(m_definition, shift=RIGHT))
        self.wait(0.5)

        # 4. ef Slider elements
        # Position ef track at y = -0.8, labels around it
        ef_label = MathTex(
            r"ef \text{ (Candidate Queue Size)}", font_size=22, color=WHITE
        )
        ef_label.move_to([-1.5, -0.4, 0.0])

        ef_value_display = MathTex(r"ef = 10", font_size=22, color=EMERALD_COLOR)
        ef_value_display.move_to([3.0, -0.4, 0.0])

        ef_track = Line(
            start=[-3.5, -0.9, 0.0],
            end=[3.5, -0.9, 0.0],
            color=DARK_SLATE,
            stroke_width=4.0,
        )

        # Ticks for ef track
        ef_tick_left = Line(
            [-3.5, -1.05, 0], [-3.5, -0.75, 0], color=SLATE_COLOR, stroke_width=2
        )
        ef_tick_right = Line(
            [3.5, -1.05, 0], [3.5, -0.75, 0], color=SLATE_COLOR, stroke_width=2
        )
        ef_val_left = MathTex("1", font_size=16, color=SLATE_COLOR).next_to(
            ef_tick_left, DOWN, buff=0.1
        )
        ef_val_right = MathTex("500", font_size=16, color=SLATE_COLOR).next_to(
            ef_tick_right, DOWN, buff=0.1
        )

        # Knob starts at 10 (let's say it's placed at x = -2.5)
        ef_knob = Dot(point=[-2.5, -0.9, 0.0], color=EMERALD_COLOR, radius=0.14)

        ef_definition = Tex(
            r"$\rightarrow$ controls how wide the search beam is",
            font_size=18,
            color=SLATE_COLOR,
        )
        ef_definition.move_to([-0.5, -1.5, 0.0])

        ef_sublabels = (
            VGroup(
                Tex(
                    r"$ef_{\text{construction}}$ : for indexing",
                    font_size=16,
                    color=SLATE_COLOR,
                ),
                Tex(
                    r"$ef_{\text{search}}$ : for querying",
                    font_size=16,
                    color=SLATE_COLOR,
                ),
            )
            .arrange(RIGHT, buff=0.6)
            .move_to([-0.5, -2.0, 0.0])
        )

        # Animate ef Slider
        self.play(
            FadeIn(ef_label),
            Create(ef_track),
            Create(ef_tick_left),
            Create(ef_tick_right),
            FadeIn(ef_val_left),
            FadeIn(ef_val_right),
        )
        self.play(FadeIn(ef_knob), FadeIn(ef_value_display))
        self.play(
            Flash(
                ef_knob,
                color=EMERALD_COLOR,
                line_length=0.25,
                num_lines=8,
                flash_radius=0.2,
            )
        )
        self.play(FadeIn(ef_definition, shift=RIGHT), FadeIn(ef_sublabels, shift=UP))
        self.wait(1.5)

        # 5. Clean up Scene
        self.play(
            FadeOut(title),
            FadeOut(dashboard_card),
            FadeOut(m_label),
            FadeOut(m_value_display),
            FadeOut(m_track),
            FadeOut(m_tick_left),
            FadeOut(m_tick_right),
            FadeOut(m_val_left),
            FadeOut(m_val_right),
            FadeOut(m_knob),
            FadeOut(m_definition),
            FadeOut(ef_label),
            FadeOut(ef_value_display),
            FadeOut(ef_track),
            FadeOut(ef_tick_left),
            FadeOut(ef_tick_right),
            FadeOut(ef_val_left),
            FadeOut(ef_val_right),
            FadeOut(ef_knob),
            FadeOut(ef_definition),
            FadeOut(ef_sublabels),
            run_time=0.8,
        )
        self.wait(0.5)
