from manim import *

# Set to 1:1 Square resolution for perfect LinkedIn/Twitter viewing
config.pixel_width = 480
config.pixel_height = 480
config.frame_rate = 30

class AcceleratorTeaser(Scene):
    def construct(self):
        # 1. The Hook
        title = Text("Unleashing Spatial Compute", font_size=48).shift(UP * 3.5)
        self.play(Write(title), run_time=1)

        # 2. The 160 MAC Grid (Dormant State)
        mac_grid = VGroup(*[
            Square(side_length=0.25, stroke_width=2, stroke_color=BLUE_E, fill_opacity=0.1) 
            for _ in range(160)
        ])
        mac_grid.arrange_in_grid(rows=10, cols=16, buff=0.1).shift(DOWN * 0.5)
        self.play(FadeIn(mac_grid, shift=UP*0.5), run_time=1)

        # 3. The "Power Up" Cascade (Aesthetic Glow)
        # LaggedStart triggers the glow sequentially across the grid like a wave
        self.play(
            LaggedStart(
                *[mac.animate.set_color(YELLOW).set_fill(ORANGE, opacity=0.8) for mac in mac_grid],
                lag_ratio=0.01,
                run_time=2
            )
        )

        # 4. The Flex
        gops_text = Text("20.8 GOPS", font_size=80, color=RED, weight=BOLD).move_to(mac_grid)
        subtitle = Text("Team Silicore • Coming Soon", font_size=32, color=GRAY).next_to(mac_grid, DOWN * 2)
        
        # Dim the grid and punch in the text
        self.play(
            mac_grid.animate.set_opacity(0.15),
            FadeIn(gops_text, scale=0.2),
            Write(subtitle)
        )
        self.wait(2)

if __name__ == "__main__":
    with tempconfig({"renderer": "opengl", "preview": True}):
        my_scene = AcceleratorTeaser()  # Instantiate the object
        # my_scene.construct()     # Call the method
        my_scene.render()