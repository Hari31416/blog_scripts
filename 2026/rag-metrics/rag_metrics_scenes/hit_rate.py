from manim import *
from .common import (
    BG_COLOR,
    RELEVANT_COLOR,
    IRRELEVANT_COLOR,
    HIGHLIGHT_COLOR,
    DocumentCard,
    create_stack,
)


class HitRateMixin:
    def hit_rate_scene(self):
        # Scene 3: Hit Rate@K (The Needle in the Haystack)
        # Title
        title = Text(
            "Hit Rate@K (Needle in the Haystack)", font="sans-serif", weight=BOLD
        ).scale(0.7)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Create three scaled-down stacks
        s1 = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "relevant",
                "irrelevant",
                "irrelevant",
                "irrelevant",
                "irrelevant",
            ],
            width=2.5,
            height=0.45,
            buff=0.08,
            text_scale=0.7,
        ).shift(LEFT * 4 + UP * 0.5)

        s2 = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "irrelevant",
                "relevant",
                "irrelevant",
                "relevant",
                "relevant",
            ],
            width=2.5,
            height=0.45,
            buff=0.08,
            text_scale=0.7,
        ).shift(UP * 0.5)

        s3 = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "irrelevant",
                "irrelevant",
                "irrelevant",
                "irrelevant",
                "irrelevant",
            ],
            width=2.5,
            height=0.45,
            buff=0.08,
            text_scale=0.7,
        ).shift(RIGHT * 4 + UP * 0.5)

        lbl1 = Text(
            "Query 1: Hit = 1", font="sans-serif", weight=SEMIBOLD, color=RELEVANT_COLOR
        ).scale(0.4)
        lbl1.next_to(s1, DOWN, buff=0.25)

        lbl2 = Text(
            "Query 2: Hit = 1", font="sans-serif", weight=SEMIBOLD, color=RELEVANT_COLOR
        ).scale(0.4)
        lbl2.next_to(s2, DOWN, buff=0.25)

        lbl3 = Text(
            "Query 3: Hit = 0",
            font="sans-serif",
            weight=SEMIBOLD,
            color=IRRELEVANT_COLOR,
        ).scale(0.4)
        lbl3.next_to(s3, DOWN, buff=0.25)

        self.play(
            FadeIn(s1),
            FadeIn(lbl1),
            FadeIn(s2),
            FadeIn(lbl2),
            FadeIn(s3),
            FadeIn(lbl3),
            run_time=2.0,
        )
        self.wait(1.0)

        # Highlight first green cards in s1 and s2 to show success
        self.play(
            Indicate(s1[0], color=RELEVANT_COLOR),
            Indicate(s2[1], color=RELEVANT_COLOR),
            run_time=1.5,
        )
        self.wait(0.5)

        # Formula
        formula_text = Text(
            "Average Hit Rate@5:", font="sans-serif", weight=MEDIUM
        ).scale(0.4)
        formula_text.shift(DOWN * 2.0 + LEFT * 2.5)

        formula = MathTex(
            r"\text{Hit Rate@5} = \frac{1 + 1 + 0}{3} = 0.67\ (67\%)", color=WHITE
        ).scale(0.7)
        formula.next_to(formula_text, RIGHT, buff=0.3)

        self.play(Write(formula_text), Write(formula))
        self.wait(2.5)

        # Fade out everything from Scene 3
        self.play(
            FadeOut(title),
            FadeOut(s1),
            FadeOut(lbl1),
            FadeOut(s2),
            FadeOut(lbl2),
            FadeOut(s3),
            FadeOut(lbl3),
            FadeOut(formula_text),
            FadeOut(formula),
        )
        self.wait(0.5)
