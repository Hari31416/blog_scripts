from manim import *
import random

# Define colors from plan
BI_ENCODER_COLOR = "#58C4DD"
CROSS_ENCODER_COLOR = "#FC6255"
COLBERT_COLOR = "#9650D9"


class RetrievalComparison(Scene):
    def construct(self):
        self.intro_scene()
        self.bi_encoder_scene()
        self.cross_encoder_scene()
        self.colbert_scene()
        self.summary_table()

    def intro_scene(self):
        title = Text("Retrieval Architectures", font_size=48)
        subtitle = Text(
            "Bi-Encoders vs. Cross-Encoders vs. ColBERT", font_size=32, color=GRAY
        )
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

    def bi_encoder_scene(self):
        # Header
        header = Text("Bi-Encoders", color=BI_ENCODER_COLOR).to_edge(UP)
        self.play(Write(header))

        # Query and Doc Boxes
        q_box = RoundedRectangle(
            corner_radius=0.1, height=1.5, width=3, color=BI_ENCODER_COLOR
        )
        d_box = RoundedRectangle(
            corner_radius=0.1, height=1.5, width=3, color=BI_ENCODER_COLOR
        )

        q_box.shift(LEFT * 2 + UP * 1)
        d_box.shift(LEFT * 2 + DOWN * 1)

        q_label = Text("Query Encoder", font_size=24).move_to(q_box)
        d_label = Text("Doc Encoder", font_size=24).move_to(d_box)

        q_text = Text('"How to bake bread"', font_size=20).next_to(q_box, LEFT)
        d_text = Text("Document content...", font_size=20).next_to(d_box, LEFT)

        self.play(Create(q_box), Create(d_box), Write(q_label), Write(d_label))
        self.play(Write(q_text), Write(d_text))

        # Output Vectors
        q_vec = Arrow(
            start=q_box.get_right(),
            end=q_box.get_right() + RIGHT * 1.5,
            color=BI_ENCODER_COLOR,
            stroke_width=8,
        )
        d_vec = Arrow(
            start=d_box.get_right(),
            end=d_box.get_right() + RIGHT * 1.5,
            color=BI_ENCODER_COLOR,
            stroke_width=8,
        )

        q_vec_label = MathTex(r"V_q", color=BI_ENCODER_COLOR).next_to(q_vec, UP)
        d_vec_label = MathTex(r"V_d", color=BI_ENCODER_COLOR).next_to(d_vec, DOWN)

        self.play(
            GrowArrow(q_vec), GrowArrow(d_vec), FadeIn(q_vec_label), FadeIn(d_vec_label)
        )
        self.wait(1)

        # Interaction
        dot_product = MathTex(r"V_q \cdot V_d", font_size=48).shift(RIGHT * 4)
        self.play(
            q_vec.animate.move_to(RIGHT * 3.5 + UP * 0.5),
            d_vec.animate.move_to(RIGHT * 3.5 + DOWN * 0.5),
            q_vec_label.animate.move_to(RIGHT * 3.5 + UP * 1),
            d_vec_label.animate.move_to(RIGHT * 3.5 + DOWN * 1),
            FadeOut(q_box),
            FadeOut(d_box),
            FadeOut(q_label),
            FadeOut(d_label),
            FadeOut(q_text),
            FadeOut(d_text),
        )
        self.play(Write(dot_product))

        pros = (
            VGroup(
                Text("✔ Scalable: Pre-compute V_d", font_size=24, color=GREEN),
                Text("✔ Fast: Simple dot product", font_size=24, color=GREEN),
                Text("✘ Loses token nuance", font_size=24, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .to_edge(DOWN, buff=0.5)
        )

        self.play(Write(pros))
        self.wait(2)
        self.play(
            FadeOut(
                VGroup(
                    header, q_vec, d_vec, q_vec_label, d_vec_label, dot_product, pros
                )
            )
        )

    def cross_encoder_scene(self):
        header = Text("Cross-Encoders", color=CROSS_ENCODER_COLOR).to_edge(UP)
        self.play(Write(header))

        # Concatenation
        input_box = RoundedRectangle(
            corner_radius=0.1, height=1, width=8, color=CROSS_ENCODER_COLOR
        )
        input_text = Text("[CLS] Query [SEP] Document", font_size=24).move_to(input_box)

        self.play(Create(input_box), Write(input_text))
        self.wait(1)

        # Transformer Block
        transformer = Rectangle(height=3, width=6, color=WHITE, fill_opacity=0.1)
        transformer_label = Text("Transformer (Full Attention)", font_size=32).move_to(
            transformer
        )

        self.play(
            input_box.animate.shift(UP * 2.5),
            input_text.animate.shift(UP * 2.5),
            Create(transformer),
            Write(transformer_label),
        )
        transformer.shift(UP * 0.5)
        transformer_label.move_to(transformer)

        # Attention Lines (simplified)
        lines = VGroup()
        for i in range(5):
            for j in range(5):
                line = Line(
                    transformer.get_left() + RIGHT * 1 + UP * (1 - i * 0.5),
                    transformer.get_right() - RIGHT * 1 + UP * (1 - j * 0.5),
                    stroke_width=1,
                    stroke_opacity=0.3,
                    color=CROSS_ENCODER_COLOR,
                )
                lines.add(line)

        self.play(Create(lines, lag_ratio=0.01, run_time=2))
        self.wait(1)

        score = Text("Score: 0.98", color=YELLOW, font_size=32)

        cons = (
            VGroup(
                score,
                Line(LEFT, RIGHT, color=GRAY).scale(2),
                Tex(r"\checkmark Extremely Precise", font_size=34, color=GREEN),
                Tex(r"$\times$ Slow: $O(N)$ docs", font_size=34, color=RED),
                Tex(r"$\times$ Cannot pre-compute", font_size=34, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .to_edge(DOWN, buff=0.4)
        )

        self.play(Write(cons))
        self.wait(2)
        self.play(
            FadeOut(
                VGroup(
                    header,
                    input_box,
                    input_text,
                    transformer,
                    transformer_label,
                    lines,
                    score,
                    cons,
                )
            )
        )

    def colbert_scene(self):
        header = Text("ColBERT (Late Interaction)", color=COLBERT_COLOR).to_edge(UP)
        self.play(Write(header))

        # Multi-vector output
        q_vectors = VGroup(
            *[Arrow(UP * 0.5, DOWN * 0.5, color=COLBERT_COLOR) for _ in range(5)]
        ).arrange(RIGHT, buff=0.2)
        d_vectors = VGroup(
            *[Arrow(UP * 0.5, DOWN * 0.5, color=COLBERT_COLOR) for _ in range(5)]
        ).arrange(RIGHT, buff=0.2)

        q_vectors.shift(LEFT * 3 + UP * 1)
        d_vectors.shift(LEFT * 3 + DOWN * 1)

        q_label = Text("Query Tokens", font_size=20).next_to(q_vectors, LEFT)
        d_label = Text("Doc Tokens", font_size=20).next_to(d_vectors, LEFT)

        self.play(FadeIn(q_vectors), FadeIn(d_vectors), Write(q_label), Write(d_label))
        self.wait(1)

        # MaxSim Matrix
        matrix = Square(side_length=3).shift(RIGHT * 3)
        grid = VGroup(
            *[
                Line(
                    matrix.get_left() + RIGHT * (i * 0.6),
                    matrix.get_left() + RIGHT * (i * 0.6) + UP * 1.5 + DOWN * 1.5,
                )
                for i in range(6)
            ]
        )
        grid.add(
            *[
                Line(
                    matrix.get_top() + DOWN * (i * 0.6),
                    matrix.get_top() + DOWN * (i * 0.6) + LEFT * 1.5 + RIGHT * 1.5,
                )
                for i in range(6)
            ]
        )
        grid.set_stroke(opacity=0.2)

        matrix_label = Text("MaxSim Interaction", font_size=24).next_to(matrix, UP)

        formula = MathTex(
            r"S(Q, D) = \sum_{i=1}^{n} \max_{j=1}^{m} (q_i \cdot d_j)",
            font_size=36,
            color=COLBERT_COLOR,
        ).next_to(matrix, DOWN, buff=0.8)

        self.play(Create(matrix), Create(grid), Write(matrix_label))
        self.play(Write(formula))
        self.wait(1)

        # Detailed breakdown text
        step_text = (
            Text(
                "1. For each query token, find best doc match",
                font_size=24,
                color=YELLOW,
            )
            .to_edge(LEFT, buff=1)
            .shift(UP * 2.5)
        )
        self.play(Write(step_text))

        # MaxSim Logic: for each query token, find max in doc
        highlights = VGroup()
        matching_lines = VGroup()
        individual_scores = VGroup()

        for i in range(5):
            # Show a "scan" effect for each query token
            scan_line = Line(
                matrix.get_left() + UP * (1.2 - i * 0.6),
                matrix.get_right() + UP * (1.2 - i * 0.6),
                color=YELLOW,
                stroke_width=2,
            )

            # Highlight query vector being processed
            q_vectors[i].set_color(YELLOW)

            self.play(Create(scan_line, run_time=0.3 if i == 0 else 0.1))

            col = random.randint(0, 4)
            highlight = Square(side_length=0.6, color=YELLOW, fill_opacity=0.5).move_to(
                matrix.get_top()
                + LEFT * 1.2
                + DOWN * (0.3 + i * 0.6)
                + RIGHT * (col * 0.6)
            )

            # Score for this row
            row_score = DecimalNumber(
                random.uniform(0.7, 0.95), num_decimal_places=2, font_size=20
            ).move_to(highlight)

            # Line from token to match
            m_line = Line(
                q_vectors[i].get_center(),
                d_vectors[col].get_center(),
                color=YELLOW,
                stroke_width=2,
                stroke_opacity=0.7,
            )

            self.play(
                FadeIn(highlight),
                FadeIn(row_score),
                FadeIn(m_line),
                FadeOut(scan_line),
                run_time=0.4 if i == 0 else 0.2,
            )

            highlights.add(highlight)
            matching_lines.add(m_line)
            individual_scores.add(row_score)

            # Reset query vector color
            q_vectors[i].set_color(COLBERT_COLOR)

        self.wait(1)

        step_text_2 = Text(
            "2. Sum the maximum similarities", font_size=24, color=YELLOW
        ).move_to(step_text)
        self.play(Transform(step_text, step_text_2))

        total_score_label = MathTex(r"Total \approx", font_size=32)
        total_score_val = DecimalNumber(4.21, num_decimal_places=2, font_size=32)

        score_group = (
            VGroup(formula, total_score_label, total_score_val)
            .arrange(RIGHT, buff=0.3)
            .next_to(matrix, DOWN, buff=0.8)
        )

        self.play(
            LaggedStart(
                *[
                    s.animate.move_to(total_score_val).fade(1)
                    for s in individual_scores
                ],
                lag_ratio=0.1
            ),
            FadeIn(total_score_label),
            Write(total_score_val),
            run_time=1.5,
        )
        self.wait(2)

        pros = (
            VGroup(
                Tex(
                    r"$\checkmark$ Scalable: Pre-compute tokens",
                    font_size=34,
                    color=GREEN,
                ),
                Tex(
                    r"$\checkmark$ Precise: Token-level alignment",
                    font_size=34,
                    color=GREEN,
                ),
                Tex(r"$\times$ Storage: Multiple vectors/doc", font_size=34, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .to_edge(DOWN, buff=0.4)
        )

        self.play(
            FadeOut(score_group),
            FadeOut(step_text),
        )
        self.play(Write(pros))
        self.wait(2)
        self.play(
            FadeOut(
                VGroup(
                    header,
                    q_vectors,
                    d_vectors,
                    q_label,
                    d_label,
                    matrix,
                    grid,
                    matrix_label,
                    highlights,
                    matching_lines,
                    individual_scores,
                    pros,
                )
            )
        )

    def summary_table(self):
        title = Text("Direct Comparison", font_size=40).to_edge(UP)

        # Define table content based on user's image (simplified)
        rows = [
            [
                Text("Architecture"),
                Text("1 vector / text"),
                Text("1 vector / token"),
                Text("Joint encoding"),
            ],
            [
                Text("Comparison"),
                Text("Dot product"),
                Text("MaxSim (Tokens)"),
                Text("Cross-attention"),
            ],
            [
                Text("Use Case"),
                Text("1st-stage search"),
                Text("Precision search"),
                Text("Final reranking"),
            ],
            [Text("Speed"), Tex(r"Fast $O(1)$"), Text("Moderate"), Tex(r"Slow $O(N)$")],
        ]

        table = (
            Table(
                rows,
                col_labels=[
                    Text("Feature"),
                    Text("Bi-Encoder"),
                    Text("ColBERT"),
                    Text("Cross-Encoder"),
                ],
                element_to_mobject=lambda x: x,
                include_outer_lines=True,
            )
            .scale(0.5)
            .shift(DOWN * 0.5)
        )

        # Color the header
        table.get_vertical_lines().set_color(GRAY)
        table.get_horizontal_lines().set_color(GRAY)

        self.play(Write(title))
        self.play(table.create())
        self.wait(5)
        self.play(FadeOut(table), FadeOut(title))
