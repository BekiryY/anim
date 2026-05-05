from manim import *

class HardwareEffects(Scene):
    def construct(self):
        # Create a single MAC unit
        mac_core = Square(side_length=1, stroke_color=BLUE, fill_opacity=0.2)
        self.play(DrawBorderThenFill(mac_core)) # Mechanical creation effect

        # Simulate the core executing an intense operation
        self.play(
            Indicate(mac_core, color=RED, scale_factor=1.5),
            Flash(mac_core, color=YELLOW, line_length=0.5, flash_radius=0.8),
            run_time=1
        )

        # Highlight the core smoothly after processing
        self.play(Circumscribe(mac_core, color=GREEN, time_width=1.5))
        self.wait()


if __name__ == "__main__":
    scene = HardwareEffects()
    scene.render()