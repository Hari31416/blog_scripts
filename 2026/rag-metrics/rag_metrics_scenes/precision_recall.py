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


class PrecisionRecallMixin:
    def precision_recall_scene(self):
        # Scene 2: Precision@K & Recall@K (The Binary Foundation)
        # Title
        title = Text("Precision@K & Recall@K", font="sans-serif", weight=BOLD).scale(
            0.7
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Left Stack
        stack = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "relevant",
                "irrelevant",
                "relevant",
                "irrelevant",
                "relevant",
            ],
            width=3.2,
            height=0.6,
            buff=0.12,
        )
        stack.shift(LEFT * 4.0 + DOWN * 0.2)

        stack_label = Text(
            "Retrieved Stack (K=5)", font="sans-serif", weight=MEDIUM
        ).scale(0.4)
        stack_label.next_to(stack, UP, buff=0.2)

        self.play(FadeIn(stack), FadeIn(stack_label))
        self.wait(0.5)

        # 2. Database Pool (Right Side, Top)
        db_box = RoundedRectangle(
            corner_radius=0.1,
            width=4.4,
            height=1.6,
            stroke_color=RELEVANT_COLOR,
            stroke_width=2,
            fill_color="#0F172A",
            fill_opacity=0.8,
        ).shift(RIGHT * 3.0 + UP * 1.8)

        db_label = Text(
            "All Relevant Docs in DB (N = 6)", font="sans-serif", weight=MEDIUM
        ).scale(0.35)
        db_label.next_to(db_box, UP, buff=0.15)

        # 6 mini cards inside the database pool
        db_cards = VGroup()
        for i in range(6):
            c = RoundedRectangle(
                corner_radius=0.05,
                width=1.0,
                height=0.4,
                fill_color=RELEVANT_COLOR,
                fill_opacity=0.3,
                stroke_color=RELEVANT_COLOR,
                stroke_width=1.5,
            )
            lbl = Text(f"Doc D_R{i+1}", font="sans-serif").scale(0.2)
            lbl.move_to(c.get_center())
            card_g = VGroup(c, lbl)
            db_cards.add(card_g)

        db_cards.arrange_in_grid(rows=2, cols=3, buff=0.15)
        db_cards.move_to(db_box.get_center())

        self.play(Create(db_box), FadeIn(db_label), FadeIn(db_cards))
        self.wait(0.5)

        # 3. Precision Formula (Right Side, Middle)
        precision_title = Text(
            "Precision@5", font="sans-serif", weight=BOLD, color=WHITE
        ).scale(0.4)
        precision_formula = MathTex(
            r"\text{Precision@5} = \frac{\text{Relevant in Top 5}}{5}", color=WHITE
        ).scale(0.6)

        precision_calc = MathTex(r"= \frac{3}{5} = 0.60\ (60\%)", color=WHITE).scale(
            0.6
        )

        p_group = VGroup(precision_title, precision_formula, precision_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        p_group.move_to(RIGHT * 3.0 + DOWN * 0.4)

        self.play(FadeIn(precision_title), Write(precision_formula))
        self.wait(0.5)

        # Highlight the relevant cards in stack
        self.play(
            *[Indicate(stack[i], color=RELEVANT_COLOR) for i in [0, 2, 4]], run_time=1.5
        )
        self.wait(0.5)

        self.play(Write(precision_calc))
        self.wait(1.0)

        # 4. Recall Formula (Right Side, Bottom)
        recall_title = Text(
            "Recall@5", font="sans-serif", weight=BOLD, color=WHITE
        ).scale(0.4)
        recall_formula = MathTex(
            r"\text{Recall@5} = \frac{\text{Relevant in Top 5}}{\text{Total Relevant}}",
            color=WHITE,
        ).scale(0.6)

        recall_calc = MathTex(r"= \frac{3}{6} = 0.50\ (50\%)", color=WHITE).scale(0.6)

        r_group = VGroup(recall_title, recall_formula, recall_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        r_group.move_to(RIGHT * 3.0 + DOWN * 2.1)

        self.play(FadeIn(recall_title), Write(recall_formula))
        self.wait(0.5)

        # Highlight database pool (6 cards)
        self.play(
            Indicate(db_box, color=RELEVANT_COLOR),
            Indicate(db_cards, color=RELEVANT_COLOR),
            run_time=1.5,
        )
        self.wait(0.5)

        self.play(Write(recall_calc))
        self.wait(1.5)

        # 5. Order Insensitivity Demonstration
        # Show shuffling explanation text
        shuffle_text = Text(
            "Shuffling retrieved documents...",
            font="sans-serif",
            weight=BOLD,
            color=HIGHLIGHT_COLOR,
        ).scale(0.4)
        shuffle_text.next_to(stack, DOWN, buff=0.3)
        self.play(Write(shuffle_text))
        self.wait(0.5)

        # Swap cards visually
        pos = [card.get_center() for card in stack]

        self.play(
            stack[0].animate.move_to(pos[1]),
            stack[1].animate.move_to(pos[0]),
            stack[2].animate.move_to(pos[3]),
            stack[3].animate.move_to(pos[2]),
            run_time=1.5,
        )
        self.wait(0.5)

        # Transform into a correctly ordered shuffled stack to update the labels (Rank numbers)
        correct_shuffled_stack = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "irrelevant",
                "relevant",
                "irrelevant",
                "relevant",
                "relevant",
            ],
            width=3.2,
            height=0.6,
            buff=0.12,
        )
        correct_shuffled_stack.move_to(stack.get_center())

        self.play(ReplacementTransform(stack, correct_shuffled_stack))
        self.wait(0.5)

        # Show unchanged explanation text
        unchanged_text = Text(
            "Score remains unchanged even with different order!",
            font="sans-serif",
            weight=BOLD,
            color=HIGHLIGHT_COLOR,
        ).scale(0.35)
        unchanged_text.next_to(correct_shuffled_stack, DOWN, buff=0.3)

        self.play(ReplacementTransform(shuffle_text, unchanged_text))
        self.play(
            Indicate(precision_calc, color=HIGHLIGHT_COLOR),
            Indicate(recall_calc, color=HIGHLIGHT_COLOR),
            run_time=1.5,
        )
        self.wait(2.5)

        # Fade out everything from Scene 2
        self.play(
            FadeOut(title),
            FadeOut(correct_shuffled_stack),
            FadeOut(stack_label),
            FadeOut(db_box),
            FadeOut(db_label),
            FadeOut(db_cards),
            FadeOut(p_group),
            FadeOut(r_group),
            FadeOut(unchanged_text),
        )
        self.wait(0.5)
