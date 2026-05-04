from manim import *

config.pixel_height = 240
config.pixel_width = 320
config.frame_rate = 50
config.preview = True

class HardwareConvolution(Scene):
    def construct(self):
        # --- 1. SETUP THE 24x16 GRIDS ---
        def create_arch(title_text, color):
            grid = VGroup(*[Square(side_length=0.2, stroke_color=color, stroke_width=1, fill_opacity=0.1) for _ in range(384)])
            grid.arrange_in_grid(rows=24, cols=16, buff=0)
            title = Text(title_text, font_size=24).next_to(grid, UP, buff=0.2)
            return VGroup(title, grid), grid

        cpu_ui, cpu_grid = create_arch("CPU (Sequential)", BLUE_E)
        gpu_ui, gpu_grid = create_arch("GPU (Batches)", GREEN_E)
        fpga_ui, fpga_grid = create_arch("FPGA (Spatial)", ORANGE)

        VGroup(cpu_ui, gpu_ui, fpga_ui).arrange(RIGHT, buff=0.8)
        self.play(FadeIn(cpu_ui), FadeIn(gpu_ui), FadeIn(fpga_ui), run_time=1)

        # --- 2. READY THE FILTERS ---
        
        # CPU: 1x1 Rectangle 
        cpu_filter = Rectangle(width=0.2, height=0.2, stroke_color=RED, stroke_width=4)
        cpu_filter.move_to(cpu_grid[0].get_center())

        # GPU: 48 distributed Cores
        gpu_filter = VGroup()
        for r in range(0, 24, 4):
            for c in range(0, 16, 2):
                idx = r * 16 + c 
                rect = Rectangle(width=0.2, height=0.2, stroke_color=YELLOW, stroke_width=4)
                rect.move_to(gpu_grid[idx].get_center())
                gpu_filter.add(rect)

        # FPGA: 6x4 Spatial Array (4 cols, 6 rows)
        # 4 blocks * 0.2 width = 0.8, 6 blocks * 0.2 height = 1.2
        fpga_filter = Rectangle(width=0.8, height=1.2, stroke_color=ORANGE, stroke_width=6)
        fpga_filter.move_to(fpga_grid[0].get_corner(UL) + RIGHT*0.4 + DOWN*0.6)

        self.play(Create(cpu_filter), Create(gpu_filter), Create(fpga_filter))
        self.wait(0.5)

        # --- 3. EXECUTION ANIMATIONS ---
        
        # CPU path (using absolute positions to prevent Succession bugs)
        cpu_indices = []
        for r in range(24):
            if r % 2 == 0:
                cpu_indices.extend(range(r * 16, (r + 1) * 16))
            else:
                cpu_indices.extend(reversed(range(r * 16, (r + 1) * 16)))
        
        cpu_anims = []
        # Limiting to 30 animation cell shifts for a quicker test run
        for idx in cpu_indices[1:31]:
            target_pos = cpu_grid[idx].get_center()
            cpu_anims.append(cpu_filter.animate(run_time=0.02).set_color(GREEN))
            cpu_anims.append(cpu_filter.animate(run_time=0.02).set_color(RED))
            cpu_anims.append(cpu_filter.animate(run_time=0.02).move_to(target_pos))

        # GPU path (using absolute positions)
        gpu_snake_path = [RIGHT * 0.2, DOWN * 0.2, LEFT * 0.2, DOWN * 0.2, DOWN * 0.2, RIGHT * 0.2]
        gpu_anims = []
        gpu_curr_pos = gpu_filter.get_center()
        for direction in gpu_snake_path:
            gpu_curr_pos = gpu_curr_pos + direction
            gpu_anims.append(gpu_filter.animate(run_time=0.06).set_color(WHITE))
            gpu_anims.append(gpu_filter.animate(run_time=0.06).set_color(YELLOW))
            gpu_anims.append(gpu_filter.animate(run_time=0.06).move_to(gpu_curr_pos))

        # FPGA path (Discrete 4x4 kernels snake path using absolute positions)
        fpga_anims = []
        fpga_centers = []
        for r in range(4): # 4 kernels vertically
            for c in range(4): # 4 kernels horizontally
                actual_c = c if r % 2 == 0 else 3 - c
                # Top-left grid index of the current 6x4 kernel
                idx = (r * 6) * 16 + (actual_c * 4)
                kernel_center = fpga_grid[idx].get_corner(UL) + RIGHT*0.4 + DOWN*0.6
                fpga_centers.append(kernel_center)
        
        for target_pos in fpga_centers[1:]:
            fpga_anims.append(fpga_filter.animate(run_time=0.16, rate_func=linear).move_to(target_pos))

        # Play all three streams concurrently
        self.play(
            Succession(*cpu_anims),
            Succession(*gpu_anims),
            Succession(*fpga_anims)
        )
        self.wait(1)

if __name__ == "__main__":
    scene = HardwareConvolution()
    scene.render()