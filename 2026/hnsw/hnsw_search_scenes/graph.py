from manim import *
import numpy as np
from .common import *


class GraphMixin:
    def get_transformed_coord(self, pt, center, scale):
        """Translates and scales a coordinate centered at the zoom anchor"""
        return np.array(
            [
                (pt[0] - center[0]) * scale,
                (pt[1] - center[1]) * scale,
                pt[2],  # keep Z coordinate constant
            ]
        )

    def build_layer_graph(
        self, nodes_list, edges_list, z, node_color, edge_color, center=None, scale=1.0
    ):
        """Creates a zoomed/shifted graph at the given Z level with uniform node size and line weights"""
        if center is None:
            center = [0.0, 0.0, z]

        nodes_mobjects = {}
        for node in nodes_list:
            raw_pt = [COORDS[node][0], COORDS[node][1], z]
            transformed_pt = self.get_transformed_coord(raw_pt, center, scale)

            dot = Dot(point=transformed_pt, color=node_color, radius=0.08)

            # Label search path nodes using MathTex (perfect alignment)
            if node in ["A", "D", "E", "H", "I", "K", "R", "P"]:
                label = MathTex(node, font_size=20, color=node_color)
                label.next_to(dot, UP, buff=0.12)
                nodes_mobjects[node] = VGroup(dot, label)
            else:
                nodes_mobjects[node] = VGroup(dot)

        edges_mobjects = VGroup()
        for u, v in edges_list:
            if u in nodes_list and v in nodes_list:
                start_raw = [COORDS[u][0], COORDS[u][1], z]
                end_raw = [COORDS[v][0], COORDS[v][1], z]

                start_transformed = self.get_transformed_coord(start_raw, center, scale)
                end_transformed = self.get_transformed_coord(end_raw, center, scale)

                line = Line(
                    start=start_transformed,
                    end=end_transformed,
                    color=edge_color,
                    stroke_width=2.0,
                )
                edges_mobjects.add(line)

        nodes_group = VGroup(*nodes_mobjects.values())
        return nodes_group, edges_mobjects, nodes_mobjects

    def probe_and_move(self, curr_name, neighbors, next_name, z, center, scale):
        """Greedy walk step: shoots probe lines and moves searcher"""
        curr_coord = self.get_transformed_coord(
            [COORDS[curr_name][0], COORDS[curr_name][1], z], center, scale
        )
        curr_dist = np.linalg.norm(COORDS[curr_name] - COORD_Q)

        probe_lines = VGroup()
        probe_anims = []

        for nbr in neighbors:
            nbr_coord = self.get_transformed_coord(
                [COORDS[nbr][0], COORDS[nbr][1], z], center, scale
            )
            nbr_dist = np.linalg.norm(COORDS[nbr] - COORD_Q)

            color = PROBE_GREEN if nbr_dist < curr_dist else PROBE_RED
            line = Line(start=curr_coord, end=nbr_coord, color=color, stroke_width=3.0)
            probe_lines.add(line)
            probe_anims.append(Create(line))

        self.play(AnimationGroup(*probe_anims, run_time=0.4))
        self.wait(0.4)

        if next_name:
            next_coord = self.get_transformed_coord(
                [COORDS[next_name][0], COORDS[next_name][1], z], center, scale
            )
            self.path_points.append(next_coord)

            fade_anims = []
            for line in probe_lines:
                if np.allclose(line.end, next_coord):
                    fade_anims.append(FadeOut(line))
                else:
                    fade_anims.append(line.animate.set_stroke(opacity=0.15))

            self.play(
                self.searcher.animate.move_to(next_coord),
                self.searcher_ring.animate.move_to(next_coord),
                *fade_anims,
                run_time=0.8
            )
            self.wait(0.2)
            self.remove(*probe_lines)
        else:
            self.play(probe_lines.animate.set_color(PROBE_RED), run_time=0.3)
            self.wait(0.4)
            self.play(FadeOut(probe_lines), run_time=0.4)
            self.remove(*probe_lines)
