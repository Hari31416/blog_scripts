from manim import *
from .common import (
    BG_COLOR,
    RELEVANT_COLOR,
    IRRELEVANT_COLOR,
    HIGHLIGHT_COLOR,
    VARIABLE_COLOR,
)


class OutroMixin:
    def outro_scene(self):
        # Scene 7: Outro & Summary (The Choice Matrix)
        # Title
        title = Text("Which Metric to Use?", font="sans-serif", weight=BOLD).scale(0.8)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title))
        self.wait(0.5)

        # Custom Table Construction
        table_width = 11.0
        table_height = 4.8

        # Table background box
        table_box = RoundedRectangle(
            corner_radius=0.15,
            width=table_width,
            height=table_height,
            stroke_color=VARIABLE_COLOR,
            stroke_width=2,
            fill_color="#0b0f19",
            fill_opacity=0.95,
        ).shift(DOWN * 0.3)

        self.play(Create(table_box))
        self.wait(0.3)

        # Header dividing line
        header_y = table_box.get_top()[1] - 0.8
        header_line = Line(
            start=[table_box.get_left()[0], header_y, 0],
            end=[table_box.get_right()[0], header_y, 0],
            color=VARIABLE_COLOR,
            stroke_width=1.5,
        )

        # Column dividing line
        col_x = -2.2
        col_line = Line(
            start=[col_x, table_box.get_top()[1], 0],
            end=[col_x, table_box.get_bottom()[1], 0],
            color=VARIABLE_COLOR,
            stroke_width=1.5,
        )

        self.play(Create(header_line), Create(col_line))
        self.wait(0.3)

        # Header text
        header_metric = Text(
            "Metric", font="sans-serif", weight=BOLD, color=HIGHLIGHT_COLOR
        ).scale(0.4)
        header_metric.move_to(
            [(table_box.get_left()[0] + col_x) / 2, table_box.get_top()[1] - 0.4, 0]
        )

        header_usecase = Text(
            "Primary Use Case / Focus",
            font="sans-serif",
            weight=BOLD,
            color=HIGHLIGHT_COLOR,
        ).scale(0.4)
        header_usecase.move_to(
            [(table_box.get_right()[0] + col_x) / 2, table_box.get_top()[1] - 0.4, 0]
        )

        self.play(Write(header_metric), Write(header_usecase))
        self.wait(0.5)

        # Rows data
        rows_data = [
            ("Hit Rate / Recall", "Coverage & Needle in Haystack", RELEVANT_COLOR),
            ("Precision", "Purity of Top Results", RELEVANT_COLOR),
            ("MRR", "Navigational Search & Single Answer", RELEVANT_COLOR),
            ("MAP", "Ranked Binary Retrieval List", RELEVANT_COLOR),
            ("NDCG", "Ranked Graded List (e.g. Web Search)", VARIABLE_COLOR),
        ]

        row_y_starts = [header_y - 0.4 - i * 0.8 for i in range(5)]

        rows_group = VGroup()
        for i, (metric, usecase, col) in enumerate(rows_data):
            y = row_y_starts[i]

            metric_text = Text(metric, font="sans-serif", weight=BOLD, color=col).scale(
                0.35
            )
            # Center horizontally in the left column
            metric_text.move_to([(table_box.get_left()[0] + col_x) / 2, y, 0])

            usecase_text = Text(
                usecase, font="sans-serif", weight=MEDIUM, color=WHITE
            ).scale(0.35)
            # Left align within the right column (add buffer from divider)
            usecase_text.move_to([col_x + 0.4, y, 0], aligned_edge=LEFT)

            row_items = VGroup(metric_text, usecase_text)
            rows_group.add(row_items)

        # Fade in the rows sequentially
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=RIGHT * 0.2) for row in rows_group], lag_ratio=0.3
            ),
            run_time=2.5,
        )
        self.wait(2.0)

        # Outro text
        outro_text = Text(
            "Happy Evaluating!", font="sans-serif", weight=BOLD, color=HIGHLIGHT_COLOR
        ).scale(0.5)
        outro_text.next_to(table_box, DOWN, buff=0.25)

        self.play(Write(outro_text))
        self.wait(2.5)

        # Final fade out
        self.play(
            FadeOut(title),
            FadeOut(table_box),
            FadeOut(header_line),
            FadeOut(col_line),
            FadeOut(header_metric),
            FadeOut(header_usecase),
            FadeOut(rows_group),
            FadeOut(outro_text),
        )
        self.wait(0.5)
