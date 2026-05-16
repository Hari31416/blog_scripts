from manim import *
import numpy as np


class HNSWZoomSearch(MovingCameraScene):
    def setup(self):
        super().setup()
        self.camera.background_color = "#05070D"

    def construct(self):
        query_point = np.array([2.65, -1.38, 0.0])
        self.base_frame_width = 15

        layer2_positions = {
            "A": np.array([-5.2, 3.0, 0.0]),
            "B": np.array([-1.4, 2.2, 0.0]),
            "C": np.array([0.8, 0.6, 0.0]),
            "D": np.array([3.0, 1.8, 0.0]),
            "E": np.array([3.8, -0.2, 0.0]),
            "F": np.array([5.9, -1.9, 0.0]),
            "G": np.array([0.2, -2.8, 0.0]),
        }
        layer2_edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("B", "G"),
            ("C", "D"),
            ("C", "E"),
            ("D", "E"),
            ("E", "F"),
            ("E", "G"),
            ("F", "G"),
        ]

        layer1_positions = {
            "E": np.array([3.8, -0.2, 0.0]),
            "H": np.array([3.2, -0.35, 0.0]),
            "I": np.array([2.8, -0.9, 0.0]),
            "J": np.array([2.45, -0.45, 0.0]),
            "K": np.array([2.3, -1.1, 0.0]),
            "L": np.array([3.4, -1.25, 0.0]),
            "M": np.array([4.05, -0.95, 0.0]),
            "N": np.array([4.0, -0.55, 0.0]),
            "O": np.array([2.05, -0.15, 0.0]),
        }
        layer1_edges = [
            ("E", "H"),
            ("E", "N"),
            ("E", "M"),
            ("H", "I"),
            ("H", "J"),
            ("I", "J"),
            ("I", "K"),
            ("I", "L"),
            ("J", "K"),
            ("J", "O"),
            ("K", "L"),
            ("L", "M"),
            ("M", "N"),
            ("O", "J"),
        ]

        layer0_positions = {
            "K": np.array([2.3, -1.1, 0.0]),
            "P": np.array([2.58, -1.32, 0.0]),
            "Q": np.array([2.18, -1.45, 0.0]),
            "R": np.array([2.43, -1.22, 0.0]),
            "S": np.array([2.88, -1.08, 0.0]),
            "T": np.array([2.98, -1.45, 0.0]),
            "U": np.array([2.63, -0.94, 0.0]),
            "V": np.array([2.12, -0.88, 0.0]),
            "W": np.array([2.77, -1.62, 0.0]),
            "X": np.array([2.38, -1.68, 0.0]),
            "Y": np.array([2.04, -1.24, 0.0]),
            "Z": np.array([3.12, -1.18, 0.0]),
        }
        layer0_edges = [
            ("K", "R"),
            ("K", "V"),
            ("K", "Y"),
            ("R", "P"),
            ("R", "Q"),
            ("R", "S"),
            ("P", "S"),
            ("P", "T"),
            ("P", "W"),
            ("Q", "X"),
            ("Q", "Y"),
            ("S", "U"),
            ("S", "Z"),
            ("T", "W"),
            ("U", "V"),
            ("W", "X"),
            ("Y", "X"),
        ]

        layer2 = self.build_layer(
            layer2_positions,
            layer2_edges,
            dot_radius=0.09,
            dot_color="#C7D2FE",
            edge_color="#6B7280",
            edge_width=2.6,
            edge_opacity=0.55,
        )
        layer1 = self.build_layer(
            layer1_positions,
            layer1_edges,
            dot_radius=0.075,
            dot_color="#E5E7EB",
            edge_color="#64748B",
            edge_width=2.2,
            edge_opacity=0.48,
        )
        layer0 = self.build_layer(
            layer0_positions,
            layer0_edges,
            dot_radius=0.055,
            dot_color=WHITE,
            edge_color="#475569",
            edge_width=1.8,
            edge_opacity=0.42,
        )

        self.status_value = "Searching Layer 2 (Sparse)"
        self.complexity_value = "Hierarchical greedy search"
        self.status_overlay = always_redraw(self.build_status_bar)
        self.complexity_overlay = always_redraw(self.build_complexity_label)
        self.add(self.status_overlay, self.complexity_overlay)

        query = always_redraw(lambda: self.build_query_marker(query_point))
        query.set_z_index(10)

        searcher_position = VectorizedPoint(layer2["nodes"]["A"].get_center())
        searcher = always_redraw(
            lambda: self.build_searcher(searcher_position.get_center())
        )
        searcher.set_z_index(11)
        trace = TracedPath(
            searcher_position.get_center,
            stroke_color="#FBBF24",
            stroke_width=3.5,
            dissipating_time=0.8,
        )

        self.camera.frame.set(width=15)
        self.add(trace)
        self.play(
            LaggedStart(*[Create(edge) for edge in layer2["edges"]], lag_ratio=0.08),
            LaggedStart(
                *[FadeIn(node, scale=0.8) for node in layer2["nodes"].values()],
                lag_ratio=0.06,
            ),
            FadeIn(query, scale=0.9),
            FadeIn(searcher, scale=0.7),
            run_time=2.4,
        )
        self.play(
            query.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=1.1,
        )

        self.greedy_step(
            layer2, searcher_position, query_point, "A", ["B", "D"], "D", run_time=1.8
        )
        self.greedy_step(
            layer2, searcher_position, query_point, "D", ["C", "E"], "E", run_time=1.8
        )
        self.wait(0.5)

        self.transition_to_layer(
            source_layer=layer2["group"],
            target_layer=layer1["group"],
            focus_point=layer1["nodes"]["E"].get_center(),
            new_status="Zooming to Layer 1",
            new_complexity="Refine inside a denser neighborhood",
            target_width=6.2,
            run_time=2.2,
        )
        self.update_status("Searching Layer 1 (Refined)")
        self.greedy_step(
            layer1,
            searcher_position,
            query_point,
            "E",
            ["H", "N", "M"],
            "H",
            run_time=1.5,
        )
        self.greedy_step(
            layer1, searcher_position, query_point, "H", ["I", "J"], "I", run_time=1.5
        )
        self.greedy_step(
            layer1,
            searcher_position,
            query_point,
            "I",
            ["K", "L", "J"],
            "K",
            run_time=1.7,
        )
        self.wait(0.4)

        self.transition_to_layer(
            source_layer=layer1["group"],
            target_layer=layer0["group"],
            focus_point=layer0["nodes"]["K"].get_center(),
            new_status="Final Zoom: Layer 0 (Dense)",
            new_complexity="Base layer: exact nearest-neighbor walk",
            target_width=2.8,
            run_time=2.4,
        )
        self.greedy_step(
            layer0,
            searcher_position,
            query_point,
            "K",
            ["R", "V", "Y"],
            "R",
            run_time=1.6,
        )
        self.greedy_step(
            layer0,
            searcher_position,
            query_point,
            "R",
            ["P", "Q", "S"],
            "P",
            run_time=1.8,
        )

        nearest = layer0["nodes"]["P"]
        glow = Circle(radius=0.22, stroke_color="#FDE68A", stroke_width=3.5).move_to(
            nearest
        )
        glow.set_z_index(12)

        self.update_status("Nearest Neighbor Found")
        self.update_complexity("O(log N) Search Complexity")
        self.play(
            searcher_position.animate.move_to(nearest.get_center()),
            nearest.animate.set_color("#FDE68A"),
            FadeIn(glow),
            run_time=1.2,
        )
        self.play(
            Flash(nearest, color="#FDE68A", line_length=0.2, num_lines=10),
            Indicate(query, color="#FF5A5F", scale_factor=1.05),
            run_time=1.2,
        )
        self.wait(1.5)

    def build_layer(
        self,
        positions,
        edges,
        dot_radius,
        dot_color,
        edge_color,
        edge_width,
        edge_opacity,
    ):
        nodes = {}
        frame = self.camera.frame
        base_frame_width = self.base_frame_width
        for name, point in positions.items():
            node = Dot(point, radius=dot_radius, color=dot_color)
            node.base_radius = dot_radius
            node.add_updater(
                lambda mob, frame=frame, base_frame_width=base_frame_width: mob.set_radius(
                    mob.base_radius * (frame.width / base_frame_width)
                )
            )
            node.set_z_index(4)
            nodes[name] = node

        edge_mobjects = []
        for start_name, end_name in edges:
            line = Line(
                positions[start_name],
                positions[end_name],
                stroke_color=edge_color,
                stroke_width=edge_width,
                stroke_opacity=edge_opacity,
            )
            line.set_z_index(1)
            edge_mobjects.append(line)

        edge_group = VGroup(*edge_mobjects)
        node_group = VGroup(*nodes.values())
        return {
            "group": VGroup(edge_group, node_group),
            "nodes": nodes,
            "edges": edge_mobjects,
        }

    def build_searcher(self, position):
        scale = self.camera.frame.width / self.base_frame_width
        ring = Circle(
            radius=0.18 * scale,
            stroke_color="#FBBF24",
            stroke_width=max(1.6, 3 * scale),
        )
        core = Dot(radius=0.06 * scale, color="#FDE68A")
        searcher = VGroup(ring, core).move_to(position)
        return searcher

    def build_query_marker(self, position):
        scale = self.camera.frame.width / self.base_frame_width
        halo = Dot(
            position,
            radius=0.24 * scale,
            color="#FF5A5F",
            fill_opacity=0.15,
            stroke_width=0,
        )
        core = Dot(position, radius=0.12 * scale, color="#FF5A5F")
        group = VGroup(halo, core)
        return group

    def build_status_bar(self):
        scale = self.camera.frame.width / self.base_frame_width
        label = self.build_ui_text(self.status_value, font_size=24, color=WHITE)
        box = RoundedRectangle(
            corner_radius=0.12,
            width=max(6.1, label.width + 0.7),
            height=0.62,
            fill_color="#111827",
            fill_opacity=0.9,
            stroke_color="#334155",
            stroke_width=1.5,
        )
        label.move_to(box)
        group = VGroup(box, label).scale(scale)
        group.move_to(
            self.camera.frame.get_center()
            + UP * (self.camera.frame.height / 2 - group.height / 2 - 0.18 * scale)
        )
        group.set_z_index(20)
        return group

    def build_complexity_label(self):
        scale = self.camera.frame.width / self.base_frame_width
        label = self.build_ui_text(self.complexity_value, font_size=21, color="#CBD5E1")
        box = RoundedRectangle(
            corner_radius=0.12,
            width=max(4.9, label.width + 0.7),
            height=0.58,
            fill_color="#0F172A",
            fill_opacity=0.86,
            stroke_color="#334155",
            stroke_width=1.4,
        )
        label.move_to(box)
        group = VGroup(box, label).scale(scale)
        group.move_to(
            self.camera.frame.get_center()
            + RIGHT * (self.camera.frame.width / 2 - group.width / 2 - 0.2 * scale)
            + DOWN * (self.camera.frame.height / 2 - group.height / 2 - 0.18 * scale)
        )
        group.set_z_index(20)
        return group

    def build_ui_text(self, text, font_size, color):
        return Tex(
            rf"\textsf{{{self.escape_tex(text)}}}",
            font_size=font_size,
            color=color,
        )

    def escape_tex(self, text):
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
        }
        return "".join(replacements.get(char, char) for char in text)

    def update_status(self, text, run_time=0.45):
        self.status_value = text
        if run_time:
            self.wait(run_time)

    def update_complexity(self, text, run_time=0.45):
        self.complexity_value = text
        if run_time:
            self.wait(run_time)

    def transition_to_layer(
        self,
        source_layer,
        target_layer,
        focus_point,
        new_status,
        new_complexity,
        target_width,
        run_time,
    ):
        self.add(target_layer)
        target_layer.save_state()
        target_layer.set_opacity(0)
        self.play(
            self.camera.frame.animate.move_to(focus_point).set(width=target_width),
            FadeOut(source_layer, shift=0.08 * UP),
            Restore(target_layer),
            run_time=run_time,
            rate_func=smooth,
        )
        self.update_status(new_status, run_time=0.5)
        self.update_complexity(new_complexity, run_time=0.5)

    def greedy_step(
        self,
        layer,
        searcher_position,
        query_point,
        current_name,
        candidate_names,
        next_name,
        run_time,
    ):
        current_node = layer["nodes"][current_name]
        current_distance = np.linalg.norm(current_node.get_center() - query_point)

        probes = []
        for name in candidate_names:
            node = layer["nodes"][name]
            candidate_distance = np.linalg.norm(node.get_center() - query_point)
            better = candidate_distance < current_distance
            line = Line(
                current_node.get_center(),
                node.get_center(),
                stroke_color="#22C55E" if better else "#EF4444",
                stroke_width=4,
                stroke_opacity=0.92,
            )
            line.set_z_index(8)
            probes.append(line)

        probe_group = VGroup(*probes)
        self.play(
            LaggedStart(*[Create(line) for line in probes], lag_ratio=0.15),
            run_time=0.7,
        )

        next_node = layer["nodes"][next_name]
        self.play(
            Indicate(next_node, color="#22C55E", scale_factor=1.2),
            run_time=0.55,
        )
        self.play(
            searcher_position.animate.move_to(next_node.get_center()),
            run_time=run_time * 0.55,
            rate_func=smooth,
        )
        self.play(FadeOut(probe_group), run_time=0.35)
