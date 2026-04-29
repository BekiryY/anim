from manim import *

config.quality = "low_quality"
config.preview = True
config.frame_rate = 30

CELL_SIZE = 0.5
GRID_ROWS = 10
GRID_COLS = 10
KERNEL_SIZE = 3

class Convolution(Scene):
    def construct(self):
        cell = CELL_SIZE

        # --- Build 10x10 grid ---
        grid = VGroup()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                sq = Square(side_length=cell, stroke_width=1, stroke_color=WHITE, fill_opacity=0)
                sq.move_to([c * cell, -r * cell, 0])
                grid.add(sq)

        grid.move_to(ORIGIN)

        grid_label = Text("10×10 Input", font_size=24).next_to(grid, UP)

        self.play(Create(grid), Write(grid_label))
        self.wait(0.3)

        # --- Build 3x3 kernel highlight ---
        kernel = VGroup()
        for r in range(KERNEL_SIZE):
            for c in range(KERNEL_SIZE):
                sq = Square(
                    side_length=cell,
                    stroke_width=2,
                    stroke_color=YELLOW,
                    fill_color=YELLOW,
                    fill_opacity=0.35,
                )
                sq.move_to([c * cell, -r * cell, 0])
                kernel.add(sq)

        kernel_label = Text("3×3 Kernel", font_size=24, color=YELLOW)

        # Position kernel at top-left cell of the grid
        top_left = grid[0].get_center()
        kernel.move_to(
            top_left + RIGHT * cell * (KERNEL_SIZE - 1) / 2
                      + DOWN  * cell * (KERNEL_SIZE - 1) / 2
        )
        kernel_label.next_to(kernel, UP).shift(UP * 0.1)

        self.play(FadeIn(kernel), Write(kernel_label))
        self.wait(0.3)

        # --- Slide kernel across the grid ---
        stride = 1
        steps_c = GRID_COLS - KERNEL_SIZE  # 7 steps horizontally
        steps_r = GRID_ROWS - KERNEL_SIZE  # 7 steps vertically

        run_time_per_step = 0.18

        for row in range(steps_r + 1):
            for col in range(steps_c + 1):
                if row == 0 and col == 0:
                    continue  # already placed here

                target_center = (
                    top_left
                    + RIGHT * col * cell
                    + DOWN  * row * cell
                    + RIGHT * cell * (KERNEL_SIZE - 1) / 2
                    + DOWN  * cell * (KERNEL_SIZE - 1) / 2
                )

                self.play(
                    kernel.animate.move_to(target_center),
                    kernel_label.animate.next_to(
                        target_center + UP * cell * (KERNEL_SIZE - 1) / 2,
                        UP, buff=0.05
                    ),
                    run_time=run_time_per_step,
                    rate_func=linear,
                )

        self.wait(1)


if __name__ == "__main__":
    my_scene = Convolution()  # Instantiate the object
    # my_scene.construct()     # Call the method
    my_scene.render()