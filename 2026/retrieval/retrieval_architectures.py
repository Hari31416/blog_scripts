from manim import *
import random

# Define colors
BI_ENCODER_COLOR = "#58C4DD"
CROSS_ENCODER_COLOR = "#FC6255"
COLBERT_COLOR = "#9650D9"

class BiEncoderFrame(Scene):
    def construct(self):
        header = Text("Bi-Encoder Architecture", color=BI_ENCODER_COLOR, font_size=40).to_edge(UP, buff=0.5)
        
        # Query and Doc Boxes
        q_box = RoundedRectangle(corner_radius=0.1, height=1.2, width=2.5, color=BI_ENCODER_COLOR)
        d_box = RoundedRectangle(corner_radius=0.1, height=1.2, width=2.5, color=BI_ENCODER_COLOR)
        q_box.shift(LEFT * 3.5 + UP * 1)
        d_box.shift(LEFT * 3.5 + DOWN * 1)
        
        q_label = Text("Query Encoder", font_size=20).move_to(q_box)
        d_label = Text("Doc Encoder", font_size=20).move_to(d_box)
        
        q_text = Text('"How to bake bread"', font_size=16, color=GRAY).next_to(q_box, LEFT)
        d_text = Text("Document content...", font_size=16, color=GRAY).next_to(d_box, LEFT)
        
        # Vectors
        q_vec = Arrow(start=q_box.get_right(), end=q_box.get_right() + RIGHT * 1.5, color=BI_ENCODER_COLOR, stroke_width=6)
        d_vec = Arrow(start=d_box.get_right(), end=d_box.get_right() + RIGHT * 1.5, color=BI_ENCODER_COLOR, stroke_width=6)
        
        q_vec_label = MathTex(r"V_q", color=BI_ENCODER_COLOR).next_to(q_vec, UP, buff=0.1)
        d_vec_label = MathTex(r"V_d", color=BI_ENCODER_COLOR).next_to(d_vec, DOWN, buff=0.1)
        
        # Interaction
        interaction_label = Text("Similarity", font_size=24).shift(RIGHT * 2.5 + UP * 1.5)
        dot_product = MathTex(r"Score = V_q \cdot V_d", font_size=48).shift(RIGHT * 2.5)
        
        # Details
        details = VGroup(
            Text("✔ Pre-compute Doc Vectors", font_size=22, color=GREEN),
            Text("✔ Sub-millisecond search (ANN)", font_size=22, color=GREEN),
            Text("✘ Loses token-level interaction", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        
        self.add(header, q_box, d_box, q_label, d_label, q_text, d_text, q_vec, d_vec, q_vec_label, d_vec_label, dot_product, interaction_label, details)

class CrossEncoderFrame(Scene):
    def construct(self):
        header = Text("Cross-Encoder Architecture", color=CROSS_ENCODER_COLOR, font_size=40).to_edge(UP, buff=0.5)
        
        # Input
        input_box = RoundedRectangle(corner_radius=0.1, height=0.8, width=7, color=CROSS_ENCODER_COLOR)
        input_text = Text("[CLS] Query [SEP] Document", font_size=24).move_to(input_box)
        input_box.shift(UP * 2)
        input_text.move_to(input_box)
        
        # Transformer
        transformer = Rectangle(height=2.5, width=5, color=WHITE, fill_opacity=0.1)
        transformer_label = Text("Transformer\n(Full Self-Attention)", font_size=28, line_spacing=1).move_to(transformer)
        transformer.shift(UP * 0.2)
        transformer_label.move_to(transformer)
        
        # Attention Lines
        lines = VGroup()
        for i in range(6):
            for j in range(6):
                line = Line(
                    transformer.get_left() + RIGHT * 0.8 + UP * (0.8 - i * 0.3),
                    transformer.get_right() - RIGHT * 0.8 + UP * (0.8 - j * 0.3),
                    stroke_width=1, stroke_opacity=0.2, color=CROSS_ENCODER_COLOR
                )
                lines.add(line)
        
        # Score
        score = Text("Score: 0.98", color=YELLOW, font_size=36).next_to(transformer, DOWN, buff=0.4)
        
        # Details
        details = VGroup(
            Text("✔ Maximum Precision", font_size=22, color=GREEN),
            Text("✘ Cannot pre-compute vectors", font_size=22, color=RED),
            Text("✘ Extremely slow: O(N) inference", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        
        self.add(header, input_box, input_text, transformer, transformer_label, lines, score, details)

class LateInteractionFrame(Scene):
    def construct(self):
        header = Text("Late Interaction (ColBERT)", color=COLBERT_COLOR, font_size=40).to_edge(UP, buff=0.5)
        
        # Multi-vector output
        q_vectors = VGroup(*[Arrow(UP*0.4, DOWN*0.4, color=COLBERT_COLOR, stroke_width=4) for _ in range(5)]).arrange(RIGHT, buff=0.2)
        d_vectors = VGroup(*[Arrow(UP*0.4, DOWN*0.4, color=COLBERT_COLOR, stroke_width=4) for _ in range(5)]).arrange(RIGHT, buff=0.2)
        
        q_vectors.shift(LEFT * 4 + UP * 0.8)
        d_vectors.shift(LEFT * 4 + DOWN * 0.8)
        
        q_label = Text("Query Tokens", font_size=18).next_to(q_vectors, LEFT)
        d_label = Text("Doc Tokens", font_size=18).next_to(d_vectors, LEFT)
        
        # Interaction Matrix
        matrix = Square(side_length=2.5, color=WHITE, stroke_opacity=0.5).shift(RIGHT * 0.5)
        grid = VGroup(*[Line(matrix.get_left() + RIGHT*(i*0.5), matrix.get_left() + RIGHT*(i*0.5) + UP*1.25 + DOWN*1.25, stroke_opacity=0.2) for i in range(6)])
        grid.add(*[Line(matrix.get_top() + DOWN*(i*0.5), matrix.get_top() + DOWN*(i*0.5) + LEFT*1.25 + RIGHT*1.25, stroke_opacity=0.2) for i in range(6)])
        
        # Highlights (MaxSim)
        highlights = VGroup()
        for i in range(5):
            col = random.randint(0, 4)
            h = Square(side_length=0.5, color=YELLOW, fill_opacity=0.4, stroke_width=0).move_to(
                matrix.get_top() + LEFT*1 + DOWN*(0.25 + i*0.5) + RIGHT*(col*0.5)
            )
            highlights.add(h)
            # Line from token to match
            m_line = Line(q_vectors[i].get_center(), d_vectors[col].get_center(), color=YELLOW, stroke_width=1, stroke_opacity=0.3)
            self.add(m_line)

        matrix_label = Text("MaxSim Interaction", font_size=20).next_to(matrix, UP)
        
        # Formula
        formula = MathTex(
            r"S(Q, D) = \sum_{i=1}^{n} \max_{j=1}^{m} (q_i \cdot d_j)",
            font_size=32, color=COLBERT_COLOR
        ).next_to(matrix, RIGHT, buff=0.5)
        
        # Details
        details = VGroup(
            Text("✔ Token-level precision", font_size=22, color=GREEN),
            Text("✔ Pre-computable vectors", font_size=22, color=GREEN),
            Text("✘ High storage: multiple vectors/doc", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        
        self.add(header, q_vectors, d_vectors, q_label, d_label, matrix, grid, highlights, matrix_label, formula, details)
