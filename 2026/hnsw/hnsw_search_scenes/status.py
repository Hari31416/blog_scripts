from manim import *
from .common import SEARCHER_COLOR


class StatusMixin:
    def init_status_bar(self):
        # 1. Create a glassmorphic status box at the top of the frame
        self.status_box = Rectangle(
            width=6.0,
            height=0.6,
            fill_color="#0D1117",
            fill_opacity=0.85,
            stroke_color=SEARCHER_COLOR,
            stroke_width=1.5,
        ).to_edge(UP, buff=0.3)

        self.status_text = Text("HNSW Hierarchical Search", font_size=16, color=WHITE)
        self.status_text.move_to(self.status_box.get_center())

        # Add as fixed-in-frame overlay: it stays perfectly flat, horizontal,
        # centered at the top of the screen at all times and never tilts in 3D!
        self.add_fixed_in_frame_mobjects(self.status_box, self.status_text)

    def update_status(self, text_str):
        """Seamlessly updates the status bar text with standard Text, preventing 3D distortion"""
        new_text = Text(text_str, font_size=16, color=WHITE)
        new_text.move_to(self.status_box.get_center())

        # 1. Add new text to fixed-in-frame immediately so it starts in 2D overlay space
        self.add_fixed_in_frame_mobjects(new_text)

        # 2. Perform a clean cross-fade between old and new overlay text
        self.play(
            FadeOut(self.status_text, run_time=0.3), FadeIn(new_text, run_time=0.4)
        )

        # 3. Clean up the old text completely from the scene and fixed-in-frame systems
        self.remove_fixed_in_frame_mobjects(self.status_text)
        self.remove(self.status_text)

        # 4. Keep the reference updated
        self.status_text = new_text
        self.wait(0.2)
