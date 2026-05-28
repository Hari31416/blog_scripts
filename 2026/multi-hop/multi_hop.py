from manim import *
import numpy as np

# Color Palette
BG_COLOR = ManimColor("#0F172A")       # Slate Dark Blue
SEQ_COLOR = ManimColor("#F43F5E")      # Rose Red
PAR_COLOR = ManimColor("#10B981")      # Emerald Green
TEXT_COLOR = ManimColor("#F8FAFC")     # Off-white
HL_COLOR = ManimColor("#3B82F6")       # Electric Blue
GREY_COLOR = ManimColor("#64748B")     # Slate Muted Grey
CARD_BG = ManimColor("#1E293B")        # Slate Darker Grey
AGENT_COLOR = ManimColor("#8B5CF6")     # Violet

class BaseMultiHopScene(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def create_title(self, title_text):
        title = Text(title_text, font_size=32, weight=BOLD, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.4)
        underline = Line(LEFT, RIGHT, color=HL_COLOR).scale(5.5).next_to(title, DOWN, buff=0.15)
        self.add(title, underline)
        return VGroup(title, underline)

    def create_card(self, text_str, title_str=None, border_color=GREY_COLOR, width=4.5, height=2.0, font_size=14):
        bg = RoundedRectangle(corner_radius=0.15, width=width, height=height)
        bg.set_fill(CARD_BG, opacity=0.9)
        bg.set_stroke(border_color, width=2.5)
        
        content = VGroup()
        if title_str:
            title = Text(title_str, font_size=font_size+2, weight=BOLD, color=HL_COLOR)
            content.add(title)
            
        lines = text_str.split("\n")
        body_group = VGroup()
        for line in lines:
            if line.strip():
                body_group.add(Text(line, font_size=font_size, color=TEXT_COLOR))
        body_group.arrange(DOWN, buff=0.1)
        
        if title_str:
            content.add(body_group)
            content.arrange(DOWN, buff=0.2)
        else:
            content = body_group
            
        content.move_to(bg.get_center())
        card = VGroup(bg, content)
        return card

    def create_agent(self, label, radius=0.6):
        circle = Circle(radius=radius, color=AGENT_COLOR, fill_color=CARD_BG, fill_opacity=0.9, stroke_width=3)
        text = Text(label, font_size=12, weight=BOLD, color=TEXT_COLOR)
        text.move_to(circle.get_center())
        return VGroup(circle, text)


class Scene1SimpleRAGFailure(BaseMultiHopScene):
    def construct(self):
        self.create_title("Standard RAG: Single-Hop Search")
        
        # User query card
        query_card = self.create_card(
            "Compare the scientific contributions\nof Marie Curie and Albert Einstein.",
            title_str="User Query",
            border_color=HL_COLOR,
            width=5.8,
            height=1.8
        ).shift(LEFT * 3.4 + UP * 1.6)
        
        # Vector Database card
        db_card = self.create_card(
            "",
            border_color=GREY_COLOR,
            width=4.2,
            height=2.8
        ).shift(RIGHT * 3.4 + UP * 1.0)
        
        # Add database title on top to avoid overlapping with dots
        db_title = Text("Vector Database", font_size=16, weight=BOLD, color=HL_COLOR).next_to(db_card[0].get_top(), DOWN, buff=0.25)
        
        # Add scattered vector dots in DB (lower half of the card)
        dots = VGroup()
        np.random.seed(42)
        db_center = db_card[0].get_center()
        for _ in range(16):
            pt = db_center + np.array([
                np.random.uniform(-1.6, 1.6),
                np.random.uniform(-1.0, 0.2),
                0
            ])
            dot = Dot(point=pt, color=interpolate_color(HL_COLOR, GREY_COLOR, np.random.uniform(0.5, 0.8)), radius=0.08)
            dots.add(dot)
            
        self.play(FadeIn(query_card), FadeIn(db_card), FadeIn(db_title), FadeIn(dots))
        self.wait(0.5)
        
        # Query vector travel (representing standard search)
        search_arrow = Arrow(query_card.get_right(), db_card.get_left(), color=HL_COLOR)
        self.play(GrowArrow(search_arrow))
        self.wait(0.5)
        
        # Highlight two biography docs (they match Curie/Einstein but not GDP)
        bio_dot1 = dots[4]
        bio_dot2 = dots[11]
        self.play(
            bio_dot1.animate.set_color(HL_COLOR).scale(2.5),
            bio_dot2.animate.set_color(HL_COLOR).scale(2.5)
        )
        self.wait(0.5)
        
        # Retrieve broad biographies
        doc1 = self.create_card(
            "Marie Curie Biography:\nBorn in Warsaw, Poland. Nobel prize\nwinner in Physics and Chemistry.",
            title_str="Retrieved Bio 1",
            border_color=GREY_COLOR,
            width=4.8,
            height=1.8,
            font_size=11
        )
        doc2 = self.create_card(
            "Albert Einstein Biography:\nBorn in Ulm, Germany. Formulated the\ntheory of relativity.",
            title_str="Retrieved Bio 2",
            border_color=GREY_COLOR,
            width=4.8,
            height=1.8,
            font_size=11
        )
        docs_group = VGroup(doc1, doc2).arrange(DOWN, buff=0.2).shift(LEFT * 3.4 + DOWN * 1.2)
        
        retrieval_arrow = Arrow(db_card.get_left() + DOWN * 0.5, docs_group.get_right(), color=HL_COLOR)
        self.play(GrowArrow(retrieval_arrow), FadeIn(docs_group))
        self.wait(0.5)
        
        # LLM tries to generate but fails
        llm_card = self.create_card(
            "Synthesizing answer from retrieved bios...",
            title_str="LLM Generator",
            border_color=GREY_COLOR,
            width=4.2,
            height=1.6,
            font_size=12
        ).shift(RIGHT * 3.4 + DOWN * 1.2)
        
        doc_to_llm = Arrow(docs_group.get_right(), llm_card.get_left(), color=HL_COLOR)
        self.play(GrowArrow(doc_to_llm), FadeIn(llm_card))
        self.wait(1.0)
        
        # Highlight lack of detail in red
        red_rect = SurroundingRectangle(docs_group, color=SEQ_COLOR, stroke_width=3, corner_radius=0.15)
        red_label = Text("Missing detailed breakthroughs!", font_size=12, color=SEQ_COLOR).next_to(red_rect, DOWN, buff=0.1)
        
        llm_error = self.create_card(
            "Error: Insufficient details\nto compare scientific contributions.",
            title_str="LLM Output",
            border_color=SEQ_COLOR,
            width=4.2,
            height=1.6,
            font_size=12
        ).move_to(llm_card)
        
        self.play(Create(red_rect), Write(red_label))
        self.play(ReplacementTransform(llm_card, llm_error))
        self.wait(2.0)
        
        # Fade out everything
        self.play(
            FadeOut(query_card),
            FadeOut(db_card),
            FadeOut(db_title),
            FadeOut(dots),
            FadeOut(search_arrow),
            FadeOut(retrieval_arrow),
            FadeOut(docs_group),
            FadeOut(doc_to_llm),
            FadeOut(red_rect),
            FadeOut(red_label),
            FadeOut(llm_error)
        )
        self.wait(0.5)


class Scene2ParallelDecomposition(BaseMultiHopScene):
    def construct(self):
        self.create_title("Parallel Multi-Hop: Query Decomposition")
        
        # Main Query Card
        query_card = self.create_card(
            "Compare the scientific\ncontributions of Marie Curie\nand Albert Einstein.",
            title_str="User Query",
            border_color=HL_COLOR,
            width=4.4,
            height=1.6,
            font_size=11
        ).shift(LEFT * 4.6 + UP * 1.5)
        
        # Decomposition Agent
        decomp_agent = self.create_agent("Decompiler").shift(LEFT * 2.0 + UP * 1.5)
        arrow_to_decomp = Arrow(query_card.get_right(), decomp_agent.get_left(), color=HL_COLOR)
        
        self.play(FadeIn(query_card))
        self.play(FadeIn(decomp_agent), GrowArrow(arrow_to_decomp))
        self.wait(0.5)
        
        # Decomposed Parallel Sub-Queries
        sub1 = self.create_card("Scientific contributions\nof Marie Curie", border_color=PAR_COLOR, width=3.4, height=1.1, font_size=12).shift(RIGHT * 0.4 + UP * 2.3)
        sub2 = self.create_card("Scientific contributions\nof Albert Einstein", border_color=PAR_COLOR, width=3.4, height=1.1, font_size=12).shift(RIGHT * 0.4 + UP * 0.7)
        
        arrow_s1 = Arrow(decomp_agent.get_right(), sub1.get_left(), color=PAR_COLOR)
        arrow_s2 = Arrow(decomp_agent.get_right(), sub2.get_left(), color=PAR_COLOR)
        
        self.play(
            FadeIn(sub1), FadeIn(sub2),
            GrowArrow(arrow_s1), GrowArrow(arrow_s2)
        )
        self.wait(0.5)
        
        # Database Card
        db_card = self.create_card(
            "Searching concurrently...",
            title_str="Vector Database",
            border_color=GREY_COLOR,
            width=3.6,
            height=2.7
        ).shift(RIGHT * 4.4 + UP * 1.5)
        
        arrow_db1 = Arrow(sub1.get_right(), db_card.get_left() + UP * 0.6, color=PAR_COLOR)
        arrow_db2 = Arrow(sub2.get_right(), db_card.get_left() + DOWN * 0.6, color=PAR_COLOR)
        
        self.play(
            FadeIn(db_card),
            GrowArrow(arrow_db1), GrowArrow(arrow_db2)
        )
        self.wait(0.5)
        
        # Retrieved documents returned in parallel
        doc1 = self.create_card(
            "Marie Curie discovered radium\nand polonium, pioneering\nradioactivity research.",
            title_str="Retrieved Context 1",
            border_color=PAR_COLOR,
            width=3.8,
            height=1.4,
            font_size=11
        ).shift(RIGHT * 0.4 + DOWN * 1.2)
        
        doc2 = self.create_card(
            "Albert Einstein formulated relativity\nand explained the photoelectric\neffect.",
            title_str="Retrieved Context 2",
            border_color=PAR_COLOR,
            width=3.8,
            height=1.4,
            font_size=11
        ).shift(RIGHT * 0.4 + DOWN * 2.8)
        
        arrow_ret1 = Arrow(db_card.get_left() + DOWN * 1.0, doc1.get_right(), color=PAR_COLOR)
        arrow_ret2 = Arrow(db_card.get_left() + DOWN * 1.0, doc2.get_right(), color=PAR_COLOR)
        
        self.play(
            FadeIn(doc1), FadeIn(doc2),
            GrowArrow(arrow_ret1), GrowArrow(arrow_ret2)
        )
        self.wait(0.5)
        
        # Composition Agent
        comp_agent = self.create_agent("Compiler").shift(LEFT * 2.0 + DOWN * 2.0)
        
        arrow_c1 = Arrow(doc1.get_left(), comp_agent.get_right() + UP * 0.4, color=PAR_COLOR)
        arrow_c2 = Arrow(doc2.get_left(), comp_agent.get_right() + DOWN * 0.4, color=PAR_COLOR)
        
        self.play(
            FadeIn(comp_agent),
            GrowArrow(arrow_c1), GrowArrow(arrow_c2)
        )
        self.wait(0.5)
        
        # Final output synthesis card
        output_card = self.create_card(
            "Marie Curie discovered radioactive\nelements, while Albert Einstein\ndeveloped relativity.",
            title_str="Synthesized Summary",
            border_color=HL_COLOR,
            width=4.4,
            height=1.6,
            font_size=11
        ).shift(LEFT * 4.6 + DOWN * 2.0)
        
        arrow_out = Arrow(comp_agent.get_left(), output_card.get_right(), color=HL_COLOR)
        self.play(
            FadeIn(output_card),
            GrowArrow(arrow_out)
        )
        self.wait(2.5)
        
        # Fade out all elements
        self.play(
            FadeOut(query_card),
            FadeOut(decomp_agent),
            FadeOut(arrow_to_decomp),
            FadeOut(sub1),
            FadeOut(sub2),
            FadeOut(arrow_s1),
            FadeOut(arrow_s2),
            FadeOut(db_card),
            FadeOut(arrow_db1),
            FadeOut(arrow_db2),
            FadeOut(doc1),
            FadeOut(doc2),
            FadeOut(arrow_ret1),
            FadeOut(arrow_ret2),
            FadeOut(comp_agent),
            FadeOut(arrow_c1),
            FadeOut(arrow_c2),
            FadeOut(output_card),
            FadeOut(arrow_out)
        )
        self.wait(0.5)


class Scene3ParallelDecompositionFailure(BaseMultiHopScene):
    def construct(self):
        self.create_title("Where Query Decomposition Fails")
        
        # Re-introduce nested query
        query_card = self.create_card(
            "Is the GDP of Marie Curie's\nbirth country higher than\nthat of Albert Einstein's?",
            title_str="Nested Query",
            border_color=HL_COLOR,
            width=4.4,
            height=1.6,
            font_size=11
        ).shift(LEFT * 4.6 + UP * 1.5)
        
        decomp_agent = self.create_agent("Decompiler").shift(LEFT * 2.0 + UP * 1.5)
        arrow_to_decomp = Arrow(query_card.get_right(), decomp_agent.get_left(), color=HL_COLOR)
        
        self.play(FadeIn(query_card))
        self.play(FadeIn(decomp_agent), GrowArrow(arrow_to_decomp))
        self.wait(0.5)
        
        # Attempted decomposition split (but has unresolved variables in brackets)
        sub1 = self.create_card("What is the GDP of\n[Curie's birth country]?", border_color=SEQ_COLOR, width=3.4, height=1.2, font_size=11).shift(RIGHT * 0.4 + UP * 2.3)
        sub2 = self.create_card("What is the GDP of\n[Einstein's birth country]?", border_color=SEQ_COLOR, width=3.4, height=1.2, font_size=11).shift(RIGHT * 0.4 + UP * 0.7)
        
        arrow_s1 = Arrow(decomp_agent.get_right(), sub1.get_left(), color=SEQ_COLOR)
        arrow_s2 = Arrow(decomp_agent.get_right(), sub2.get_left(), color=SEQ_COLOR)
        
        self.play(
            FadeIn(sub1), FadeIn(sub2),
            GrowArrow(arrow_s1), GrowArrow(arrow_s2)
        )
        self.wait(0.5)
        
        # Show flashing red question marks or warnings on the unresolved country text
        warning1 = Text("?", font_size=32, weight=BOLD, color=SEQ_COLOR).next_to(sub1, RIGHT, buff=0.1)
        warning2 = Text("?", font_size=32, weight=BOLD, color=SEQ_COLOR).next_to(sub2, RIGHT, buff=0.1)
        
        self.play(
            Indicate(sub1[1]),
            Indicate(sub2[1]),
            FadeIn(warning1),
            FadeIn(warning2)
        )
        self.wait(0.5)
        
        # Database Card
        db_card = self.create_card(
            "Searching database...",
            title_str="Vector Database",
            border_color=GREY_COLOR,
            width=3.6,
            height=2.2
        ).shift(RIGHT * 4.4 + UP * 1.5)
        
        arrow_db1 = Arrow(sub1.get_right(), db_card.get_left() + UP * 0.4, color=SEQ_COLOR)
        arrow_db2 = Arrow(sub2.get_right(), db_card.get_left() + DOWN * 0.4, color=SEQ_COLOR)
        
        self.play(
            FadeIn(db_card),
            GrowArrow(arrow_db1), GrowArrow(arrow_db2)
        )
        self.wait(0.5)
        
        # Flash a red cross / failure on Database
        cross1 = Line(LEFT, RIGHT, color=SEQ_COLOR, stroke_width=4).scale(0.5).move_to(db_card.get_center())
        cross2 = Line(UP, DOWN, color=SEQ_COLOR, stroke_width=4).scale(0.5).rotate(45*DEGREES).move_to(db_card.get_center())
        cross1.rotate(45*DEGREES)
        cross_group = VGroup(cross1, cross2)
        
        fail_message = Text("Unresolved Dependency!", font_size=14, color=SEQ_COLOR).next_to(db_card, DOWN, buff=0.2)
        
        self.play(
            Create(cross_group),
            Write(fail_message)
        )
        self.wait(2.0)
        
        # Fade out
        self.play(
            FadeOut(query_card),
            FadeOut(decomp_agent),
            FadeOut(arrow_to_decomp),
            FadeOut(sub1),
            FadeOut(sub2),
            FadeOut(arrow_s1),
            FadeOut(arrow_s2),
            FadeOut(warning1),
            FadeOut(warning2),
            FadeOut(db_card),
            FadeOut(arrow_db1),
            FadeOut(arrow_db2),
            FadeOut(cross_group),
            FadeOut(fail_message)
        )
        self.wait(0.5)


class Scene4SequentialMultiHop(BaseMultiHopScene):
    def construct(self):
        self.create_title("Sequential Multi-Hop: Resolving Dependencies")
        
        # Re-introduce nested query
        query_card = self.create_card(
            "Is the GDP of Marie Curie's birth country\nhigher than that of Albert Einstein's?",
            title_str="Nested Query",
            border_color=HL_COLOR,
            width=5.8,
            height=1.6,
            font_size=12
        ).shift(UP * 2.2)
        
        self.play(FadeIn(query_card))
        self.wait(0.5)
        
        # -- HOP 1: Entity Resolution --
        hop1_label = Text("Hop 1: Entity Resolution (Birth Countries)", font_size=16, weight=BOLD, color=HL_COLOR).shift(LEFT * 3.2 + UP * 0.8)
        self.play(Write(hop1_label))
        
        q_hop1_1 = self.create_card("Marie Curie\nbirth country", border_color=GREY_COLOR, width=2.8, height=0.9, font_size=11).shift(LEFT * 4.8 + UP * 0.0)
        q_hop1_2 = self.create_card("Albert Einstein\nbirth country", border_color=GREY_COLOR, width=2.8, height=0.9, font_size=11).shift(LEFT * 1.6 + UP * 0.0)
        
        self.play(FadeIn(q_hop1_1), FadeIn(q_hop1_2))
        self.wait(0.5)
        
        # Retrieve results for Hop 1
        ans_hop1_1 = self.create_card("Poland", border_color=PAR_COLOR, width=2.8, height=0.8, font_size=12).shift(LEFT * 4.8 + DOWN * 1.2)
        ans_hop1_2 = self.create_card("Germany", border_color=PAR_COLOR, width=2.8, height=0.8, font_size=12).shift(LEFT * 1.6 + DOWN * 1.2)
        
        arrow_hop1_1 = Arrow(q_hop1_1.get_bottom(), ans_hop1_1.get_top(), color=PAR_COLOR)
        arrow_hop1_2 = Arrow(q_hop1_2.get_bottom(), ans_hop1_2.get_top(), color=PAR_COLOR)
        
        self.play(
            GrowArrow(arrow_hop1_1), GrowArrow(arrow_hop1_2),
            FadeIn(ans_hop1_1), FadeIn(ans_hop1_2)
        )
        self.wait(1.0)
        
        # -- Context Propagation & Morphing --
        hop2_label = Text("Hop 2: Attribute Retrieval (GDPs)", font_size=16, weight=BOLD, color=HL_COLOR).shift(RIGHT * 3.2 + UP * 0.8)
        self.play(Write(hop2_label))
        
        # Templates
        q_hop2_1 = self.create_card("GDP of [Country 1]", border_color=GREY_COLOR, width=2.8, height=0.9, font_size=11).shift(RIGHT * 1.6 + UP * 0.0)
        q_hop2_2 = self.create_card("GDP of [Country 2]", border_color=GREY_COLOR, width=2.8, height=0.9, font_size=11).shift(RIGHT * 4.8 + UP * 0.0)
        
        self.play(FadeIn(q_hop2_1), FadeIn(q_hop2_2))
        self.wait(1.0)
        
        # Context morphing animation
        q_hop2_1_resolved = self.create_card("GDP of Poland", border_color=HL_COLOR, width=2.8, height=0.9, font_size=11).move_to(q_hop2_1)
        q_hop2_2_resolved = self.create_card("GDP of Germany", border_color=HL_COLOR, width=2.8, height=0.9, font_size=11).move_to(q_hop2_2)
        
        self.play(
            ReplacementTransform(q_hop2_1, q_hop2_1_resolved),
            ReplacementTransform(q_hop2_2, q_hop2_2_resolved),
            ans_hop1_1.animate.set_color(HL_COLOR),
            ans_hop1_2.animate.set_color(HL_COLOR)
        )
        self.wait(1.0)
        
        # Retrieve results for Hop 2
        ans_hop2_1 = self.create_card("$800 Billion", border_color=PAR_COLOR, width=2.8, height=0.8, font_size=12).shift(RIGHT * 1.6 + DOWN * 1.2)
        ans_hop2_2 = self.create_card("$4.5 Trillion", border_color=PAR_COLOR, width=2.8, height=0.8, font_size=12).shift(RIGHT * 4.8 + DOWN * 1.2)
        
        arrow_hop2_1 = Arrow(q_hop2_1_resolved.get_bottom(), ans_hop2_1.get_top(), color=PAR_COLOR)
        arrow_hop2_2 = Arrow(q_hop2_2_resolved.get_bottom(), ans_hop2_2.get_top(), color=PAR_COLOR)
        
        self.play(
            GrowArrow(arrow_hop2_1), GrowArrow(arrow_hop2_2),
            FadeIn(ans_hop2_1), FadeIn(ans_hop2_2)
        )
        self.wait(1.0)
        
        # Synthesis & Final LLM output comparison
        synthesis_card = self.create_card(
            "Comparing GDP of Poland ($800B) vs. Germany ($4.5T):\nOutput: No, Germany's GDP is higher.",
            title_str="Final Synthesis",
            border_color=HL_COLOR,
            width=8.0,
            height=1.2,
            font_size=12
        ).shift(DOWN * 2.4)
        
        arrow_synth1 = Arrow(ans_hop2_1.get_bottom(), synthesis_card.get_top() + LEFT * 1.5, color=HL_COLOR)
        arrow_synth2 = Arrow(ans_hop2_2.get_bottom(), synthesis_card.get_top() + RIGHT * 1.5, color=HL_COLOR)
        
        self.play(
            GrowArrow(arrow_synth1), GrowArrow(arrow_synth2),
            FadeIn(synthesis_card)
        )
        self.wait(3.0)
        
        # Fade out
        self.play(
            FadeOut(query_card),
            FadeOut(hop1_label),
            FadeOut(q_hop1_1),
            FadeOut(q_hop1_2),
            FadeOut(ans_hop1_1),
            FadeOut(ans_hop1_2),
            FadeOut(arrow_hop1_1),
            FadeOut(arrow_hop1_2),
            FadeOut(hop2_label),
            FadeOut(q_hop2_1_resolved),
            FadeOut(q_hop2_2_resolved),
            FadeOut(ans_hop2_1),
            FadeOut(ans_hop2_2),
            FadeOut(arrow_hop2_1),
            FadeOut(arrow_hop2_2),
            FadeOut(synthesis_card),
            FadeOut(arrow_synth1),
            FadeOut(arrow_synth2)
        )
        self.wait(0.5)


class Scene5Tradeoffs(BaseMultiHopScene):
    def construct(self):
        self.create_title("Tradeoffs: Speed vs. Reasoning Depth")
        
        # Setup comparative Table using Table mobject
        rows = [
            [
                Text("Query Latency", font_size=16, color=TEXT_COLOR),
                Text("Low (O(1) round-trips)", font_size=16, color=PAR_COLOR),
                Text("High (O(N) sequential steps)", font_size=16, color=SEQ_COLOR),
            ],
            [
                Text("Dependencies", font_size=16, color=TEXT_COLOR),
                Text("Poor (Requires independent facts)", font_size=16, color=SEQ_COLOR),
                Text("Excellent (Resolves variables)", font_size=16, color=PAR_COLOR),
            ],
            [
                Text("Best Used For", font_size=16, color=TEXT_COLOR),
                Text("Comparative queries", font_size=16, color=TEXT_COLOR),
                Text("Nested / Chain-of-thought", font_size=16, color=TEXT_COLOR),
            ],
        ]
        
        table = Table(
            rows,
            col_labels=[
                Text("Metric", font_size=18, weight=BOLD, color=HL_COLOR),
                Text("Parallel Decomposition", font_size=18, weight=BOLD, color=PAR_COLOR),
                Text("Sequential Chain", font_size=18, weight=BOLD, color=SEQ_COLOR),
            ],
            element_to_mobject=lambda x: x,
            include_outer_lines=True,
            line_config={"color": GREY_COLOR, "stroke_width": 1.5}
        ).scale(0.85).shift(UP * 0.6)
        
        # Highlight Table Header boundary
        table.get_horizontal_lines()[0].set_stroke(color=TEXT_COLOR, width=2.5)
        table.get_horizontal_lines()[1].set_stroke(color=TEXT_COLOR, width=2.5)
        
        self.play(table.create(), run_time=2.0)
        self.wait(1.5)
        
        # Visual Latency Bars below the table
        latency_title = Text("Round-Trip Time (RTT) Comparison", font_size=16, weight=BOLD, color=TEXT_COLOR).shift(DOWN * 1.5)
        
        # Parallel bar
        bar_par_bg = Rectangle(height=0.4, width=6.0, color=CARD_BG, fill_opacity=0.5, stroke_width=1).shift(LEFT * 0.5 + DOWN * 2.1)
        bar_par = Rectangle(height=0.4, width=2.0, color=PAR_COLOR, fill_color=PAR_COLOR, fill_opacity=0.8)
        bar_par.move_to(bar_par_bg.get_center())
        bar_par.align_to(bar_par_bg, LEFT)
        label_par = Text("Parallel Flow: 1 RTT", font_size=11, color=PAR_COLOR).next_to(bar_par_bg, RIGHT, buff=0.2)
        
        # Sequential bar
        bar_seq_bg = Rectangle(height=0.4, width=6.0, color=CARD_BG, fill_opacity=0.5, stroke_width=1).shift(LEFT * 0.5 + DOWN * 2.7)
        bar_seq = Rectangle(height=0.4, width=5.0, color=SEQ_COLOR, fill_color=SEQ_COLOR, fill_opacity=0.8)
        bar_seq.move_to(bar_seq_bg.get_center())
        bar_seq.align_to(bar_seq_bg, LEFT)
        label_seq = Text("Sequential Flow: 2.5 RTT", font_size=11, color=SEQ_COLOR).next_to(bar_seq_bg, RIGHT, buff=0.2)
        
        self.play(
            FadeIn(latency_title),
            FadeIn(bar_par_bg), FadeIn(bar_seq_bg),
            FadeIn(label_par), FadeIn(label_seq)
        )
        
        self.play(
            GrowFromEdge(bar_par, LEFT),
            GrowFromEdge(bar_seq, LEFT),
            run_time=1.5
        )
        self.wait(3.0)
        
        # Fade out
        self.play(
            FadeOut(table),
            FadeOut(latency_title),
            FadeOut(bar_par_bg),
            FadeOut(bar_par),
            FadeOut(label_par),
            FadeOut(bar_seq_bg),
            FadeOut(bar_seq),
            FadeOut(label_seq)
        )
        self.wait(0.5)
