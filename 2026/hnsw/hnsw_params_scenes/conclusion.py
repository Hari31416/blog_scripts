from manim import *
from .common import *


class ConclusionMixin:
    def make_cell(self, check_items, cross_items, x_pos, y_pos):
        cell = VGroup()
        curr_y = y_pos
        for text in check_items:
            chk = MathTex(r"\checkmark", color=EMERALD_COLOR, font_size=18)
            txt = Tex(text, color=WHITE, font_size=15)
            chk.move_to([x_pos - 1.8, curr_y, 0.0])
            txt.next_to(chk, RIGHT, buff=0.12)
            cell.add(VGroup(chk, txt))
            curr_y -= 0.28
            
        for text in cross_items:
            crs = MathTex(r"\times", color=ROSE_COLOR, font_size=20)
            txt = Tex(text, color=WHITE, font_size=15)
            crs.move_to([x_pos - 1.8, curr_y, 0.0])
            txt.next_to(crs, RIGHT, buff=0.12)
            cell.add(VGroup(crs, txt))
            curr_y -= 0.28
            
        return cell

    def run_conclusion_scene(self):
        # 1. Title at top
        title = Tex("Hyperparameter Trade-offs", font_size=32, color=WHITE).to_edge(
            UP, buff=0.6
        )
 
        # 2. Table background card
        table_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.0,
            height=5.2,
            fill_color="#0D1117",
            fill_opacity=0.85,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.5,
        ).shift(DOWN * 0.25)
 
        self.play(Write(title), FadeIn(table_bg))
        self.wait(0.3)
 
        # 3. Column Headers
        header_y = 1.7
        h_param = Tex("Parameter", font_size=20, color=SLATE_COLOR).move_to(
            [-4.4, header_y, 0.0]
        )
        h_inc = Tex("Increase ↑", font_size=20, color=EMERALD_COLOR).move_to(
            [-0.5, header_y, 0.0]
        )
        h_dec = Tex("Decrease ↓", font_size=20, color=ROSE_COLOR).move_to(
            [4.1, header_y, 0.0]
        )
 
        headers_grp = VGroup(h_param, h_inc, h_dec)
 
        # 4. Dividers
        header_div = Line(
            start=[-5.7, 1.45, 0.0],
            end=[5.7, 1.45, 0.0],
            color=DARK_SLATE,
            stroke_width=1.5,
        )
        div_row1 = Line(
            start=[-5.7, 0.1, 0.0],
            end=[5.7, 0.1, 0.0],
            color=DARK_SLATE,
            stroke_width=1.0,
        )
        div_row2 = Line(
            start=[-5.7, -0.85, 0.0],
            end=[5.7, -0.85, 0.0],
            color=DARK_SLATE,
            stroke_width=1.0,
        )
 
        dividers_grp = VGroup(header_div, div_row1, div_row2)
 
        self.play(FadeIn(headers_grp), Create(dividers_grp))
        self.wait(0.4)
 
        # 5. Row 1: M
        lbl_m = MathTex(r"M", font_size=26, color=SEARCHER_COLOR).move_to(
            [-4.4, 0.72, 0.0]
        )
        lbl_m_desc = Tex("Max connections", font_size=12, color=SLATE_COLOR).next_to(
            lbl_m, DOWN, buff=0.08
        )
        cell_m_inc = self.make_cell(
            ["Higher Recall", "Faster Search"], ["More Memory"], x_pos=-0.5, y_pos=1.0
        )
        cell_m_dec = self.make_cell(
            ["Less Memory"], ["Lower Recall", "Trapped Searches"], x_pos=4.1, y_pos=1.0
        )
        row1_grp = VGroup(lbl_m, lbl_m_desc, cell_m_inc, cell_m_dec)
 
        # Row 2: ef_construction
        lbl_efc = MathTex(
            r"ef_{\text{construction}}", font_size=22, color=SEARCHER_COLOR
        ).move_to([-4.4, -0.38, 0.0])
        lbl_efc_desc = Tex(
            "Index build effort", font_size=12, color=SLATE_COLOR
        ).next_to(lbl_efc, DOWN, buff=0.08)
        cell_efc_inc = self.make_cell(
            ["Better Graph Quality"], ["Slower Build Time"], x_pos=-0.5, y_pos=-0.25
        )
        cell_efc_dec = self.make_cell(
            ["Faster Indexing"], ["Weaker Graph Structure"], x_pos=4.1, y_pos=-0.25
        )
        row2_grp = VGroup(lbl_efc, lbl_efc_desc, cell_efc_inc, cell_efc_dec)
 
        # Row 3: ef_search
        lbl_efs = MathTex(
            r"ef_{\text{search}}", font_size=22, color=SEARCHER_COLOR
        ).move_to([-4.4, -1.38, 0.0])
        lbl_efs_desc = Tex(
            "Query search effort", font_size=12, color=SLATE_COLOR
        ).next_to(lbl_efs, DOWN, buff=0.08)
        cell_efs_inc = self.make_cell(
            ["Higher Recall"], ["Higher Latency"], x_pos=-0.5, y_pos=-1.15
        )
        cell_efs_dec = self.make_cell(
            ["Faster Latency"], ["Lower Recall", "Local Minima"], x_pos=4.1, y_pos=-1.15
        )
        row3_grp = VGroup(lbl_efs, lbl_efs_desc, cell_efs_inc, cell_efs_dec)
 
        # Initially display all rows dim
        row1_grp.set_opacity(0.25)
        row2_grp.set_opacity(0.25)
        row3_grp.set_opacity(0.25)
 
        self.play(FadeIn(row1_grp), FadeIn(row2_grp), FadeIn(row3_grp))
        self.wait(0.6)
 
        # Glowing Highlight Box for active row
        highlight_box = RoundedRectangle(
            corner_radius=0.08,
            width=11.6,
            height=1.1,
            fill_color=SEARCHER_COLOR,
            fill_opacity=0.05,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.5,
        )
 
        # --- Highlight Row 1 ---
        highlight_box.move_to([0.0, 0.78, 0.0])
        self.play(
            row1_grp.animate.set_opacity(1.0), Create(highlight_box), run_time=0.6
        )
        self.wait(2.5)
 
        # --- Highlight Row 2 ---
        self.play(
            row1_grp.animate.set_opacity(0.25),
            row2_grp.animate.set_opacity(1.0),
            highlight_box.animate.move_to([0.0, -0.38, 0.0]),
            run_time=0.6,
        )
        self.wait(2.5)
 
        # --- Highlight Row 3 ---
        self.play(
            row2_grp.animate.set_opacity(0.25),
            row3_grp.animate.set_opacity(1.0),
            highlight_box.animate.move_to([0.0, -1.43, 0.0]),
            run_time=0.6,
        )
        self.wait(2.5)
 
        # --- Show All Bright ---
        self.play(
            row1_grp.animate.set_opacity(1.0),
            row2_grp.animate.set_opacity(1.0),
            FadeOut(highlight_box),
            run_time=0.6,
        )
        self.wait(0.5)

        # Concluding warm subtitle text
        closing_label = Tex(
            "HNSW's genius is that these trade-offs are tunable — not fixed.",
            font_size=20,
            color=GOLD_COLOR,
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(closing_label))
        self.wait(3.5)

        # Final dissolve
        self.play(
            FadeOut(title),
            FadeOut(table_bg),
            FadeOut(headers_grp),
            FadeOut(dividers_grp),
            FadeOut(row1_grp),
            FadeOut(row2_grp),
            FadeOut(row3_grp),
            FadeOut(closing_label),
            run_time=0.8,
        )
        self.wait(1.0)
