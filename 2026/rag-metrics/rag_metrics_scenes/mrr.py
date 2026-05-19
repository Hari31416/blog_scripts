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


class MRRMixin:
    def mrr_scene(self):
        # Scene 4: Mean Reciprocal Rank (MRR)
        # Title
        title = Text(
            "Mean Reciprocal Rank (MRR)", font="sans-serif", weight=BOLD
        ).scale(0.7)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Query A Stack (First hit at Rank 3, second hit at Rank 4 ignored)
        sa = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "irrelevant",
                "irrelevant",
                "relevant",
                "relevant",
                "irrelevant",
            ],
            width=2.4,
            height=0.55,
            buff=0.1,
            text_scale=0.85,
        ).shift(LEFT * 4.6 + DOWN * 0.2)

        la = Text("Query A", font="sans-serif", weight=SEMIBOLD).scale(0.4)
        la.next_to(sa, UP, buff=0.2)

        # Query B Stack (First hit at Rank 1, second hit at Rank 2 ignored)
        sb = create_stack(
            ranks=[1, 2, 3, 4, 5],
            relevance_types=[
                "relevant",
                "relevant",
                "irrelevant",
                "irrelevant",
                "irrelevant",
            ],
            width=2.4,
            height=0.55,
            buff=0.1,
            text_scale=0.85,
        ).shift(LEFT * 1.2 + DOWN * 0.2)

        lb = Text("Query B", font="sans-serif", weight=SEMIBOLD).scale(0.4)
        lb.next_to(sb, UP, buff=0.2)

        self.play(FadeIn(sa), FadeIn(la), FadeIn(sb), FadeIn(lb))
        self.wait(0.5)

        # --- Query A Highlight ---
        # Show first relevant at Rank 3
        self.play(Indicate(sa[2], color=RELEVANT_COLOR))

        # Draw arrow pointing left to Rank 3 from further left
        arrow_a = Arrow(
            start=sa[2].get_left() + LEFT * 0.7,
            end=sa[2].get_left() + LEFT * 0.1,
            color=HIGHLIGHT_COLOR,
            stroke_width=3,
        )
        val_a = MathTex(r"RR_A = \frac{1}{3}", color=HIGHLIGHT_COLOR).scale(0.65)
        val_a.next_to(sa.get_bottom(), DOWN, buff=0.1)

        self.play(Create(arrow_a), Write(val_a))
        self.wait(0.5)

        # Subsequent relevant cards are ignored
        self.play(sa[3].animate.set_opacity(0.25))
        self.wait(0.5)

        # --- Query B Highlight ---
        # Show first relevant at Rank 1
        self.play(Indicate(sb[0], color=RELEVANT_COLOR))

        # Draw arrow pointing left to Rank 1 from the right
        arrow_b = Arrow(
            start=sb[0].get_right() + RIGHT * 0.7,
            end=sb[0].get_right() + RIGHT * 0.1,
            color=HIGHLIGHT_COLOR,
            stroke_width=3,
        )
        val_b = MathTex(r"RR_B = \frac{1}{1}", color=HIGHLIGHT_COLOR).scale(0.65)
        val_b.next_to(sb.get_bottom(), DOWN, buff=0.1)

        self.play(Create(arrow_b), Write(val_b))
        self.wait(0.5)

        # Subsequent relevant cards are ignored
        self.play(sb[1].animate.set_opacity(0.25))
        self.wait(0.5)

        # --- Formula and MRR Calculation (Right Side) ---
        mrr_formula = MathTex(
            r"\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} RR_i", color=WHITE
        ).scale(0.7)

        mrr_calc = MathTex(
            r"\text{MRR} = \frac{1/3 + 1.0}{2} = 0.67", color=WHITE
        ).scale(0.7)

        calc_group = VGroup(mrr_formula, mrr_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4
        )
        calc_group.shift(RIGHT * 3.4 + DOWN * 0.2)

        self.play(Write(mrr_formula))
        self.wait(0.8)

        # Link calculations to formula
        self.play(
            Indicate(val_a, color=HIGHLIGHT_COLOR),
            Indicate(val_b, color=HIGHLIGHT_COLOR),
            Write(mrr_calc),
        )
        self.wait(2.5)

        # Fade out everything from Scene 4
        self.play(
            FadeOut(title),
            FadeOut(sa),
            FadeOut(la),
            FadeOut(sb),
            FadeOut(lb),
            FadeOut(arrow_a),
            FadeOut(val_a),
            FadeOut(arrow_b),
            FadeOut(val_b),
            FadeOut(calc_group),
        )
        self.wait(0.5)
