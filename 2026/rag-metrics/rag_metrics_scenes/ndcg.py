from manim import *
from .common import (
    BG_COLOR,
    RELEVANT_COLOR,
    PARTIAL_COLOR,
    IRRELEVANT_COLOR,
    HIGHLIGHT_COLOR,
    VARIABLE_COLOR,
    DocumentCard,
    create_stack,
)


class NDCGMixin:
    def ndcg_scene(self):
        # Scene 6: Normalized Discounted Cumulative Gain (NDCG)
        # Title
        title = Text(
            "Normalized Discounted Cumulative Gain (NDCG)",
            font="sans-serif",
            weight=BOLD,
        ).scale(0.65)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Left Stack (3 Graded Cards)
        stack = create_stack(
            ranks=[1, 2, 3],
            relevance_types=["relevant", "irrelevant", "partial"],
            scores=[3, 0, 1],
            width=3.4,
            height=0.7,
            buff=0.15,
        ).shift(LEFT * 3.5 + UP * 0.5)

        stack_label = Text(
            "Graded Relevance Stack", font="sans-serif", weight=SEMIBOLD
        ).scale(0.4)
        stack_label.next_to(stack, UP, buff=0.2)

        self.play(FadeIn(stack), FadeIn(stack_label))
        self.wait(0.5)

        # 2. Cumulative Gain (CG) - Active Working Area
        cg_title = Text(
            "1. Cumulative Gain (CG)", font="sans-serif", weight=BOLD, color=WHITE
        ).scale(0.4)
        cg_formula = MathTex(r"\text{CG} = \sum_{i=1}^{K} rel_i", color=WHITE).scale(
            0.65
        )
        cg_calc = MathTex(r"\text{CG} = 3 + 0 + 1 = 4", color=WHITE).scale(0.65)

        cg_group = VGroup(cg_title, cg_formula, cg_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        cg_group.shift(RIGHT * 2.5 + UP * 0.2)

        self.play(FadeIn(cg_title), Write(cg_formula))
        self.wait(0.5)
        self.play(
            *[Indicate(card, color=HIGHLIGHT_COLOR) for card in stack], Write(cg_calc)
        )
        self.wait(1.0)

        # Morph CG into a compact summary at top right
        cg_summary = (
            MathTex(r"\text{CG} = 4", color=WHITE)
            .scale(0.65)
            .move_to(RIGHT * 3.5 + UP * 2.2)
        )
        self.play(ReplacementTransform(cg_group, cg_summary))
        self.wait(0.5)

        # 3. Discounted Cumulative Gain (DCG) - Active Working Area
        dcg_title = Text(
            "2. Discounted Cumulative Gain (DCG)",
            font="sans-serif",
            weight=BOLD,
            color=WHITE,
        ).scale(0.4)
        dcg_formula = MathTex(
            r"\text{DCG} = \sum_{i=1}^{K} \frac{rel_i}{\log_2(i + 1)}", color=WHITE
        ).scale(0.65)
        dcg_calc = MathTex(
            r"\text{DCG} = \frac{3}{\log_2(2)} + \frac{0}{\log_2(3)} + \frac{1}{\log_2(4)}",
            color=WHITE,
        ).scale(0.65)
        dcg_sum = MathTex(r"= 3.0 + 0.0 + 0.5 = 3.5", color=WHITE).scale(0.65)

        dcg_group = VGroup(dcg_title, dcg_formula, dcg_calc, dcg_sum).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        dcg_group.shift(RIGHT * 2.5 + UP * 0.0)

        self.play(FadeIn(dcg_title), Write(dcg_formula))
        self.wait(0.5)
        self.play(Write(dcg_calc))
        self.wait(0.5)
        self.play(Write(dcg_sum))
        self.wait(1.5)

        # Morph DCG into compact summary at top right (below CG)
        dcg_summary = (
            MathTex(r"\text{DCG} = 3.5", color=WHITE)
            .scale(0.65)
            .move_to(RIGHT * 3.5 + UP * 1.5)
        )
        self.play(ReplacementTransform(dcg_group, dcg_summary))
        self.wait(0.5)

        # 4. Ideal DCG (IDCG) - Sort stack
        pos = [card.get_center() for card in stack]
        self.play(
            stack[1].animate.move_to(pos[2]),
            stack[2].animate.move_to(pos[1]),
            run_time=1.5,
        )
        self.wait(0.3)

        sorted_stack = create_stack(
            ranks=[1, 2, 3],
            relevance_types=["relevant", "partial", "irrelevant"],
            scores=[3, 1, 0],
            width=3.4,
            height=0.7,
            buff=0.15,
        )
        sorted_stack.move_to(stack.get_center())

        self.play(
            ReplacementTransform(stack, sorted_stack),
            Transform(
                stack_label,
                Text(
                    "Ideal Stack (Sorted)",
                    font="sans-serif",
                    weight=SEMIBOLD,
                    color=RELEVANT_COLOR,
                )
                .scale(0.4)
                .next_to(sorted_stack, UP, buff=0.2),
            ),
        )
        self.wait(0.5)

        # IDCG calculation - Active Working Area
        idcg_title = Text(
            "3. Ideal DCG (IDCG)", font="sans-serif", weight=BOLD, color=WHITE
        ).scale(0.4)
        idcg_calc = MathTex(
            r"\text{IDCG} = \frac{3}{\log_2(2)} + \frac{1}{\log_2(3)} + \frac{0}{\log_2(4)}",
            color=WHITE,
        ).scale(0.65)
        idcg_sum = MathTex(r"= 3.0 + 0.63 + 0.0 = 3.63", color=WHITE).scale(0.65)

        idcg_group = VGroup(idcg_title, idcg_calc, idcg_sum).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        idcg_group.shift(RIGHT * 2.5 + DOWN * 0.4)

        self.play(FadeIn(idcg_title), Write(idcg_calc))
        self.wait(0.5)
        self.play(Write(idcg_sum))
        self.wait(1.5)

        # Morph IDCG into compact summary at top right (below DCG)
        idcg_summary = (
            MathTex(r"\text{IDCG} = 3.63", color=WHITE)
            .scale(0.65)
            .move_to(RIGHT * 3.5 + UP * 0.8)
        )
        self.play(ReplacementTransform(idcg_group, idcg_summary))
        self.wait(0.5)

        # 5. NDCG Division - Active Working Area (Bottom)
        ndcg_title = Text(
            "4. Normalized DCG (NDCG)",
            font="sans-serif",
            weight=BOLD,
            color=VARIABLE_COLOR,
        ).scale(0.4)
        ndcg_calc = MathTex(
            r"\text{NDCG} = \frac{\text{DCG}}{\text{IDCG}} = \frac{3.5}{3.63} \approx 0.96",
            color=VARIABLE_COLOR,
        ).scale(0.7)

        ndcg_group = VGroup(ndcg_title, ndcg_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        ndcg_group.shift(RIGHT * 2.5 + DOWN * 1.0)

        self.play(FadeIn(ndcg_title), Write(ndcg_calc))
        self.wait(2.5)

        # Fade out everything from Scene 6
        self.play(
            FadeOut(title),
            FadeOut(sorted_stack),
            FadeOut(stack_label),
            FadeOut(cg_summary),
            FadeOut(dcg_summary),
            FadeOut(idcg_summary),
            FadeOut(ndcg_group),
        )
        self.wait(0.5)
