from manim import *

config.pixel_height = 720
config.pixel_width = 1280
config.frame_rate = 50
config.preview = True


class ScaleInContinuously(Scene):
    def construct(self):

        # ── Original single square ────────────────────────────────────────────
        outer = Square(
            side_length=2.5,
            stroke_color=BLUE_C,
            stroke_width=4,
            fill_color=BLUE_E,
            fill_opacity=0.25,
        )
        # Label anchored to square's upper edge — part of the same VGroup
        # so it scales and moves together with outer when we animate outer_group
        label = Text("ZOOM →", font_size=20, color=BLUE_B)
        label.next_to(outer, UP, buff=0.1)

        outer_group = VGroup(outer, label)
        outer_group.move_to(ORIGIN)

        # ── 4 inner squares (2×2 grid) — built before the first play ─────────
        inner_colors = [RED_C, GREEN_C, YELLOW_C, PURPLE_C]
        inner_labels = ["A", "B", "C", "D"]

        inner_cells = []
        for col, lbl in zip(inner_colors, inner_labels):
            sq = Square(
                side_length=0.7,
                stroke_color=col,
                stroke_width=3,
                fill_color=col,
                fill_opacity=0.25,
            )
            txt = Text(lbl, font_size=18, color=col)
            cell = VGroup(sq, txt)
            inner_cells.append(cell)

        inner_group = VGroup(*inner_cells)
        inner_group.arrange_in_grid(rows=2, cols=2, buff=0)
        inner_group.move_to(ORIGIN)
        inner_group.scale(0.06)   # 1.4 × 0.5 = 0.7 total — starts small inside outer

        # ── Both appear together from frame 1 ─────────────────────────────────
        self.play(
            DrawBorderThenFill(outer),
            FadeIn(label),
            FadeIn(inner_group),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── Zoom: outer + inner scale as one unit, both fly off screen ────────
        zoom_group = VGroup(outer_group, inner_group)
        self.play(
            zoom_group.animate.scale(30.0),
            run_time=1.0,
            rate_func=linear,
        )

        self.wait(1)




if __name__ == "__main__":
    scene = ScaleInContinuously()
    scene.render()
