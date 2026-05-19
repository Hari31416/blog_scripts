from manim import *
from .common import (
    BG_COLOR,
    RELEVANT_COLOR,
    IRRELEVANT_COLOR,
    HIGHLIGHT_COLOR,
    VARIABLE_COLOR,
    DocumentCard,
    create_stack,
)


class MAPMixin:
    def map_scene(self):
        # Scene 5: Mean Average Precision (MAP)
        # Title
        title = Text(
            "Mean Average Precision (MAP)", font="sans-serif", weight=BOLD
        ).scale(0.7)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Left Stack A (Good Ranking) - narrow width to fit side-by-side later
        sa = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "relevant",
                "irrelevant",
                "relevant",
                "irrelevant",
                "relevant",
            ],
            width=2.4,
            height=0.55,
            buff=0.1,
            text_scale=0.8,
        ).shift(LEFT * 3.5 + DOWN * 0.2)

        la = Text("Query A (Good)", font="sans-serif", weight=SEMIBOLD).scale(0.4)
        la.next_to(sa, UP, buff=0.2)

        self.play(FadeIn(sa), FadeIn(la))
        self.wait(0.5)

        # 2. Sliding indicator arrow
        arrow = Triangle(
            color=VARIABLE_COLOR, fill_color=VARIABLE_COLOR, fill_opacity=1
        ).scale(0.12)
        arrow.rotate(-90 * DEGREES)
        arrow.next_to(sa[0], LEFT, buff=0.15)
        self.play(FadeIn(arrow))
        self.wait(0.3)

        # Right side text lines for calculations
        # Rank 1: Relevant
        self.play(Indicate(sa[0], color=RELEVANT_COLOR))
        p1 = MathTex(r"P@1 = \frac{1}{1} = 1.0", color=RELEVANT_COLOR).scale(0.65)
        p1.move_to(RIGHT * 2.5 + UP * 1.2)
        self.play(Write(p1))
        self.wait(0.5)

        # Move to Rank 2: Irrelevant
        self.play(arrow.animate.next_to(sa[1], LEFT, buff=0.15))
        self.wait(0.3)

        # Move to Rank 3: Relevant
        self.play(arrow.animate.next_to(sa[2], LEFT, buff=0.15))
        self.play(Indicate(sa[2], color=RELEVANT_COLOR))
        p3 = MathTex(r"P@3 = \frac{2}{3} \approx 0.67", color=RELEVANT_COLOR).scale(
            0.65
        )
        p3.move_to(RIGHT * 2.5 + UP * 0.4)
        self.play(Write(p3))
        self.wait(0.5)

        # Move to Rank 4: Irrelevant
        self.play(arrow.animate.next_to(sa[3], LEFT, buff=0.15))
        self.wait(0.3)

        # Move to Rank 5: Relevant
        self.play(arrow.animate.next_to(sa[4], LEFT, buff=0.15))
        self.play(Indicate(sa[4], color=RELEVANT_COLOR))
        p5 = MathTex(r"P@5 = \frac{3}{5} = 0.60", color=RELEVANT_COLOR).scale(0.65)
        p5.move_to(RIGHT * 2.5 + DOWN * 0.4)
        self.play(Write(p5))
        self.wait(0.5)

        # Fade out indicator arrow
        self.play(FadeOut(arrow))

        # AP formula for Query A
        ap_formula_a = MathTex(
            r"AP_A = \frac{1.0 + 0.67 + 0.60}{3} \approx 0.76", color=WHITE
        ).scale(0.7)
        ap_formula_a.move_to(RIGHT * 2.5 + DOWN * 1.5)
        self.play(Write(ap_formula_a))
        self.wait(1.5)

        # --- Transition to Side-by-Side Comparison ---
        # Shift Stack A and its label to the left, scale and reposition formula A
        self.play(
            sa.animate.shift(LEFT * 1.3),
            la.animate.shift(LEFT * 1.3),
            FadeOut(p1),
            FadeOut(p3),
            FadeOut(p5),
            ap_formula_a.animate.scale(0.8).move_to(LEFT * 4.8 + DOWN * 2.3),
        )
        self.wait(0.5)

        # Create Stack B (Bad Ranking, relevant pushed down)
        sb = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "irrelevant",
                "irrelevant",
                "irrelevant",
                "relevant",
                "relevant",
            ],
            width=2.4,
            height=0.55,
            buff=0.1,
            text_scale=0.8,
        ).shift(LEFT * 1.6 + DOWN * 0.2)

        lb = Text("Query B (Bad)", font="sans-serif", weight=SEMIBOLD).scale(0.4)
        lb.next_to(sb, UP, buff=0.2)

        self.play(FadeIn(sb), FadeIn(lb))
        self.wait(0.5)

        # AP formula for Query B - scaled down and placed directly below stack B
        ap_formula_b = MathTex(
            r"AP_B = \frac{0.25 + 0.40}{3} \approx 0.22", color=WHITE
        ).scale(0.56)
        ap_formula_b.move_to(LEFT * 1 + DOWN * 2.3)

        # Highlight relevant cards in Stack B (Rank 4, 5)
        self.play(
            Indicate(sb[3], color=RELEVANT_COLOR),
            Indicate(sb[4], color=RELEVANT_COLOR),
            Write(ap_formula_b),
        )
        self.wait(1.5)

        # Draw a big text comparison on the right
        map_title = Text(
            "Mean Average Precision",
            font="sans-serif",
            weight=BOLD,
            color=VARIABLE_COLOR,
        ).scale(0.45)
        map_formula = MathTex(
            r"\text{MAP} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} AP_i", color=WHITE
        ).scale(0.7)

        map_calc = MathTex(
            r"\text{MAP} = \frac{0.76 + 0.22}{2} = 0.49", color=WHITE
        ).scale(0.7)

        map_group = VGroup(map_title, map_formula, map_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        )
        map_group.shift(RIGHT * 3.4 + UP * 0.2)

        self.play(FadeIn(map_title), Write(map_formula))
        self.wait(0.8)
        self.play(
            Indicate(ap_formula_a, color=HIGHLIGHT_COLOR),
            Indicate(ap_formula_b, color=HIGHLIGHT_COLOR),
            Write(map_calc),
        )
        self.wait(2.5)

        # Fade out everything from Scene 5
        self.play(
            FadeOut(title),
            FadeOut(sa),
            FadeOut(la),
            FadeOut(sb),
            FadeOut(lb),
            FadeOut(ap_formula_a),
            FadeOut(ap_formula_b),
            FadeOut(map_group),
        )
        self.wait(0.5)
