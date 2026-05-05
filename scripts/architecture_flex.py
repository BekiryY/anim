from manim import *

config.pixel_height = 720
config.pixel_width = 960
config.frame_rate = 50
config.preview = True

class ArchitectureFlex(Scene):
    def construct(self):

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text(
            "Architecture Performance Metrics",
            font_size=34, weight=BOLD, color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.6)

        # ── Table data ────────────────────────────────────────────────────────
        # Each inner list is one row: [metric_A, value_A, metric_B, value_B]
        rows = [
            ["GOPS",  "—",  "GOPS / $", "—"],
            ["GBPS",  "—",  "MHz",      "—"],
            ["POWER", "—",  "$",        "—"],
        ]

        # Column widths (in Manim units)
        col_widths  = [1.6, 1.6, 1.6, 1.6]
        row_height  = 0.75
        font_metric = 22   # left-side metric labels
        font_value  = 20   # right-side values

        # Colour scheme
        col_colors = [BLUE_C, BLUE_B, ORANGE, "#F4A261"]  # metric A, val A, metric B, val B
        row_bg     = ["#1a1a2e", "#16213e"]                # alternating row backgrounds

        # ── Build cells ───────────────────────────────────────────────────────
        table_group = VGroup()
        total_width  = sum(col_widths)
        total_height = row_height * len(rows)

        for ri, row_data in enumerate(rows):
            y_top = -ri * row_height

            # Row background
            bg = Rectangle(
                width=total_width,
                height=row_height,
                fill_color=row_bg[ri % 2],
                fill_opacity=0.85,
                stroke_width=0,
            )
            bg.move_to([total_width / 2 - col_widths[0] / 2,
                        y_top - row_height / 2, 0])

            table_group.add(bg)

            x_cursor = 0
            for ci, cell_text in enumerate(row_data):
                # Determine styling
                is_metric_col = ci % 2 == 0
                color  = col_colors[ci]
                fsize  = font_metric if is_metric_col else font_value
                weight = BOLD if is_metric_col else NORMAL

                label = Text(cell_text, font_size=fsize, color=color, weight=weight)
                label.move_to([
                    x_cursor + col_widths[ci] / 2,
                    y_top - row_height / 2,
                    0,
                ])
                table_group.add(label)
                x_cursor += col_widths[ci]

        # ── Column separator lines ─────────────────────────────────────────────
        # Draw a vertical line between col1 and col2 (the two metric groups)
        sep_x = col_widths[0] + col_widths[1]
        sep = Line(
            start=[sep_x, 0, 0],
            end  =[sep_x, -total_height, 0],
            stroke_color=GREY_C,
            stroke_width=1.5,
        )
        table_group.add(sep)

        # ── Outer border ──────────────────────────────────────────────────────
        border = Rectangle(
            width=total_width,
            height=total_height,
            stroke_color=GREY_B,
            stroke_width=1.5,
            fill_opacity=0,
        )
        border.move_to([total_width / 2 - col_widths[0] / 2,
                        -total_height / 2, 0])
        table_group.add(border)

        # ── Row divider lines ─────────────────────────────────────────────────
        for ri in range(1, len(rows)):
            y = -ri * row_height
            divider = Line(
                start=[0, y, 0],
                end  =[total_width, y, 0],
                stroke_color=GREY_D,
                stroke_width=0.8,
            )
            table_group.add(divider)

        # ── Position the whole table centred below the title ─────────────────
        table_group.center()
        table_group.next_to(title, DOWN, buff=0.55)

        self.play(FadeIn(table_group), run_time=0.8)
        self.wait(3)


if __name__ == "__main__":
    scene = ArchitectureFlex()
    scene.render()
