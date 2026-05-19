from manim import *
from .common import (
    BG_COLOR,
    RELEVANT_COLOR,
    IRRELEVANT_COLOR,
    HIGHLIGHT_COLOR,
    DocumentCard,
    create_stack,
)


class IntroMixin:
    def intro_scene(self):
        # Scene 1: Introduction (The Ranked List)
        # Title of the video
        title = Text(
            "Evaluating Retrieval Metrics", font="sans-serif", weight=BOLD
        ).scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Create Query Box
        query_box = RoundedRectangle(
            corner_radius=0.1,
            width=5.0,
            height=0.8,
            stroke_color=HIGHLIGHT_COLOR,
            stroke_width=2,
            fill_color="#111827",  # Dark Slate
            fill_opacity=0.9,
        )
        query_box.next_to(title, DOWN, buff=0.4)

        query_label = MathTex(r"\text{Query } Q", color=WHITE).scale(0.8)
        query_label.move_to(query_box.get_center())

        self.play(FadeIn(query_box, shift=DOWN * 0.3), Write(query_label))
        self.wait(0.5)

        # Down arrow from Query Box
        arrow = Arrow(
            start=query_box.get_bottom(),
            end=query_box.get_bottom() + DOWN * 0.8,
            color=HIGHLIGHT_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        )
        self.play(Create(arrow))
        self.wait(0.5)

        # Create and drop 5 generic cards one by one
        generic_cards = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=["generic"] * 5,
            width=4.0,
            height=0.6,
            buff=0.12,
        )
        generic_cards.next_to(arrow, DOWN, buff=0.2)

        # Animate cards descending and entering the stack
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=DOWN * 0.4) for card in generic_cards],
                lag_ratio=0.15
            ),
            run_time=1.5,
        )
        self.wait(1.0)

        # Now they evaluate one by one to show relevance
        evaluated_cards = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "relevant",
                "irrelevant",
                "relevant",
                "irrelevant",
                "relevant",
            ],
            width=4.0,
            height=0.6,
            buff=0.12,
        )
        evaluated_cards.move_to(generic_cards.get_center())

        # Transform generic to evaluated
        self.play(
            LaggedStart(
                *[
                    ReplacementTransform(generic_cards[i], evaluated_cards[i])
                    for i in range(5)
                ],
                lag_ratio=0.25
            ),
            run_time=2.0,
        )
        self.wait(2.0)

        # Fade out everything from intro
        self.play(
            FadeOut(title),
            FadeOut(query_box),
            FadeOut(query_label),
            FadeOut(arrow),
            FadeOut(evaluated_cards),
        )
        self.wait(0.5)
