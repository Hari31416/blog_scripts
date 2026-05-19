from manim import *

# Premium Color Palette
BG_COLOR = "#05070D"  # Premium Dark Navy
RELEVANT_COLOR = "#10B981"  # Emerald Green
PARTIAL_COLOR = "#34D399"  # Light Emerald
IRRELEVANT_COLOR = "#64748B"  # Slate Gray
HIGHLIGHT_COLOR = "#FF5A5F"  # Rose Red
VARIABLE_COLOR = "#A78BFA"  # Violet


class DocumentCard(VGroup):
    def __init__(
        self,
        rank,
        relevance_type,
        score=None,
        text_scale=1.0,
        width=3.6,
        height=0.7,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.rank = rank
        self.relevance_type = (
            relevance_type  # "relevant", "partial", "irrelevant", "generic"
        )
        self.score = score

        # Color resolution
        if relevance_type == "relevant":
            fill_color = RELEVANT_COLOR
            stroke_color = RELEVANT_COLOR
            fill_opacity = 0.2
        elif relevance_type == "partial":
            fill_color = PARTIAL_COLOR
            stroke_color = PARTIAL_COLOR
            fill_opacity = 0.2
        elif relevance_type == "irrelevant":
            fill_color = IRRELEVANT_COLOR
            stroke_color = IRRELEVANT_COLOR
            fill_opacity = 0.1
        else:  # generic / unevaluated
            fill_color = "#1E293B"  # Slate 800
            stroke_color = "#334155"  # Slate 700
            fill_opacity = 0.15

        self.rect = RoundedRectangle(
            corner_radius=0.1,
            width=width,
            height=height,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=2,
        )
        self.add(self.rect)

        # Label components: Rank and Relevance
        rank_text = Text(f"Rank {rank}", font="sans-serif", weight=MEDIUM).scale(
            0.35 * text_scale
        )
        rank_text.align_to(self.rect.get_left(), LEFT).shift(RIGHT * 0.25)
        self.add(rank_text)

        if relevance_type in ["relevant", "partial", "irrelevant"]:
            if relevance_type == "relevant":
                symbol = MathTex(r"\checkmark", color=RELEVANT_COLOR).scale(
                    0.9 * text_scale
                )
            elif relevance_type == "partial":
                symbol = MathTex(r"\sim", color=PARTIAL_COLOR).scale(0.9 * text_scale)
            elif relevance_type == "irrelevant":
                symbol = MathTex(r"\times", color=IRRELEVANT_COLOR).scale(
                    0.9 * text_scale
                )

            symbol.align_to(self.rect.get_right(), RIGHT).shift(LEFT * 0.35)
            self.add(symbol)

        # Add score if specified, otherwise draw generic ID label
        if score is not None:
            score_text = Text(f"Score: {score}", font="sans-serif", weight=BOLD).scale(
                0.35 * text_scale
            )
            score_text.move_to(self.rect.get_center())
            self.add(score_text)
        else:
            doc_label = Text(f"Doc D{rank}", font="sans-serif").scale(0.35 * text_scale)
            doc_label.move_to(self.rect.get_center())
            self.add(doc_label)


def create_stack(
    ranks,
    relevance_types,
    scores=None,
    text_scale=1.0,
    width=3.6,
    height=0.7,
    buff=0.15,
):
    cards = []
    for i, rank in enumerate(ranks):
        rel = relevance_types[i]
        score = scores[i] if scores is not None else None
        card = DocumentCard(
            rank, rel, score=score, text_scale=text_scale, width=width, height=height
        )
        cards.append(card)
    return VGroup(*cards).arrange(DOWN, buff=buff)
