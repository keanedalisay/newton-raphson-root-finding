from manim import *
import numpy as np

class NewtonRaphsonOscillating(MovingCameraScene):
    def construct(self):
        # Axes
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True}
        )
        labels = axes.get_axis_labels("x", "f(x)")
        self.play(Create(axes), Write(labels))

        # Function f(x) = x^3 - 2x + 2
        f = lambda x: x**3 - 2*x + 2
        df = lambda x: 3*x**2 - 2
        graph = axes.plot(f, color=BLUE)
        self.play(Create(graph))

        # Approximate root
        root_x = -1.7693  # only for visualization
        root_dot = Dot(axes.c2p(root_x, 0), color=PURPLE)
        root_label = MathTex(f"{root_x:.3f}").scale(0.7).next_to(root_dot, UP)
        self.play(FadeIn(root_dot), Write(root_label))

        # Formula box
        formula = MathTex(
            r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}"
        ).scale(0.7)
        formula.to_corner(UR)
        box = SurroundingRectangle(formula, buff=0.2)
        formula_group = VGroup(formula, box)
        formula_group.add_updater(lambda m: m.to_corner(UR))
        self.play(Write(formula), Create(box))

        # Initial guess to induce oscillation
        x_n = 0.0

        error_line = None

        for i in range(6):
            y_n = f(x_n)

            point = Dot(axes.c2p(x_n, y_n), color=RED)

            # Vertical projection
            v_line = DashedLine(
                axes.c2p(x_n, 0),
                axes.c2p(x_n, y_n),
                color=GRAY
            )

            # Tangent line
            slope = df(x_n)
            tangent = axes.plot(
                lambda x: slope * (x - x_n) + y_n,
                x_range=[x_n - 0.7, x_n + 0.7],
                color=YELLOW
            )

            # Newton update
            x_next = x_n - y_n / slope
            x_dot = Dot(axes.c2p(x_next, 0), color=GREEN)

            label = MathTex(f"x_{{{i}}}").scale(0.7)
            label.next_to(x_dot, UP)

            # Error bar to approximate root
            new_error_line = Line(
                axes.c2p(x_next, 0),
                axes.c2p(root_x, 0),
                color=RED
            )

            self.play(FadeIn(point), Create(v_line))
            self.play(Create(tangent))
            self.play(FadeIn(x_dot), Write(label))

            if error_line is None:
                error_line = new_error_line
                self.play(Create(error_line))
            else:
                self.play(Transform(error_line, new_error_line), run_time=0.6)

            self.wait(0.6)

            x_n = x_next

            # Small zoom after first iteration
            if i == 0:
                self.play(
                    self.camera.frame.animate
                    .scale(0.75)
                    .move_to(axes.c2p(-0.5, 0)),
                    run_time=1.0
                )

            self.play(
                FadeOut(point),
                FadeOut(v_line),
                FadeOut(tangent)
            )

        # Emphasize oscillation / root
        self.play(
            Indicate(root_dot, scale_factor=1.3),
            Flash(root_dot, color=PURPLE)
        )

        self.play(
            self.camera.frame.animate
            .scale(1.5) 
            .move_to(axes.c2p(0, 0)),
            run_time=1.2
        )

        self.wait(2)
