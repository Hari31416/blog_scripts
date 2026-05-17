from manim import *
from .common import *


class GreedyWalkMixin:
    def greedy_walk_scene(self):
        header = Text(
            "Greedy Traversal to Insertion Point",
            font_size=24,
            color=VIOLET_COLOR,
        ).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(header)

        # Create Searcher at Node E on Layer 2
        searcher = Dot(
            point=[COORDS["E"][0], COORDS["E"][1], 2.0], color=VIOLET_COLOR, radius=0.12
        )
        searcher_ring = Circle(radius=0.25, color=VIOLET_COLOR, stroke_width=2).move_to(
            searcher
        )
        searcher_ring.set_shade_in_3d(True)

        self.play(FadeIn(searcher), Create(searcher_ring))
        self.wait(1)

        # Since E is the only L2 node, we project directly down to L1
        proj_line = DashedLine(
            start=[COORDS["E"][0], COORDS["E"][1], 2.0],
            end=[COORDS["E"][0], COORDS["E"][1], 0.0],
            color=VIOLET_COLOR,
            stroke_width=2,
        )
        self.play(Create(proj_line))

        # Searcher dives down to L1 Node E
        self.play(
            searcher.animate.move_to([COORDS["E"][0], COORDS["E"][1], 0.0]),
            searcher_ring.animate.move_to([COORDS["E"][0], COORDS["E"][1], 0.0]),
            run_time=1.5,
        )
        self.wait(0.5)
        self.play(FadeOut(proj_line))

        # Now on L1, greedy walk to find where N belongs
        # E probes its L1 neighbors: D and B
        probe_d = Line(
            start=[COORDS["E"][0], COORDS["E"][1], 0.0],
            end=[COORDS["D"][0], COORDS["D"][1], 0.0],
            color=VIOLET_COLOR,
            stroke_width=3,
        )
        probe_b = Line(
            start=[COORDS["E"][0], COORDS["E"][1], 0.0],
            end=[COORDS["B"][0], COORDS["B"][1], 0.0],
            color=VIOLET_COLOR,
            stroke_width=3,
        )

        # Display distance comparison
        dist_labels = (
            VGroup(
                Text("d(E, N) = 1.12  (Nearest)", font_size=18, color=GREEN),
                Text("d(D, N) = 2.83  (Farther)", font_size=18, color=ROSE_COLOR),
                Text("d(B, N) = 3.04  (Farther)", font_size=18, color=ROSE_COLOR),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .to_corner(UL)
        )

        self.add_fixed_in_frame_mobjects(dist_labels)
        self.play(Create(probe_d), Create(probe_b))
        self.wait(1.5)

        # Searcher stays at E since it is closest to N (local minimum on L1)
        self.play(
            probe_d.animate.set_stroke(opacity=0.2),
            probe_b.animate.set_stroke(opacity=0.2),
        )

        local_min_text = Text(
            "Local Minimum Found: Node E", font_size=20, color=GREEN
        ).next_to(dist_labels, DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(local_min_text)
        self.play(Write(local_min_text))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(header),
            FadeOut(probe_d),
            FadeOut(probe_b),
            FadeOut(dist_labels),
            FadeOut(local_min_text),
            FadeOut(searcher),
            FadeOut(searcher_ring),
        )
