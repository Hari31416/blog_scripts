from manim import *

# Define colors from the original comparison script
BI_ENCODER_COLOR = "#58C4DD"
CROSS_ENCODER_COLOR = "#FC6255"
COLBERT_COLOR = "#9650D9"


class RetrievalHero(Scene):
    def construct(self):
        # Title for the hero image
        title = Text("Retrieval Architectures", font_size=44, weight=BOLD).to_edge(
            UP, buff=0.5
        )
        underline = (
            Line(LEFT, RIGHT, color=BLUE_B).scale(4.5).next_to(title, DOWN, buff=0.2)
        )

        # Comparison Table Data
        rows = [
            [
                Text("Architecture", font_size=24, weight=BOLD),
                Text("1 vector / text", font_size=22, color=BI_ENCODER_COLOR),
                Text("1 vector / token", font_size=22, color=COLBERT_COLOR),
                Text("Joint encoding", font_size=22, color=CROSS_ENCODER_COLOR),
            ],
            [
                Text("Comparison", font_size=24, weight=BOLD),
                Text("Dot product", font_size=22, color=BI_ENCODER_COLOR),
                Text("MaxSim (Tokens)", font_size=22, color=COLBERT_COLOR),
                Text("Cross-attention", font_size=22, color=CROSS_ENCODER_COLOR),
            ],
            [
                Text("Use Case", font_size=24, weight=BOLD),
                Text("1st-stage search", font_size=22),
                Text("Precision search", font_size=22),
                Text("Final reranking", font_size=22),
            ],
            [
                Text("Speed", font_size=24, weight=BOLD),
                Tex(r"Fast $O(1)$", font_size=30, color=GREEN),
                Text("Moderate", font_size=22, color=YELLOW),
                Tex(r"Slow $O(N)$", font_size=30, color=RED),
            ],
        ]

        # Create the table with professional styling
        table = (
            Table(
                rows,
                col_labels=[
                    Text("Feature", font_size=28, weight=BOLD),
                    Text(
                        "Bi-Encoder", font_size=28, weight=BOLD, color=BI_ENCODER_COLOR
                    ),
                    Text("ColBERT", font_size=28, weight=BOLD, color=COLBERT_COLOR),
                    Text(
                        "Cross-Encoder",
                        font_size=28,
                        weight=BOLD,
                        color=CROSS_ENCODER_COLOR,
                    ),
                ],
                element_to_mobject=lambda x: x,
                include_outer_lines=True,
                line_config={"color": GRAY_B, "stroke_width": 1.5},
            )
            .scale(0.7)
            .shift(DOWN * 0.4)
        )

        # Highlight the headers
        table.get_horizontal_lines()[0].set_stroke(color=WHITE, width=3)
        table.get_horizontal_lines()[1].set_stroke(color=WHITE, width=3)

        # Add everything to the scene
        self.add(title, underline, table)
