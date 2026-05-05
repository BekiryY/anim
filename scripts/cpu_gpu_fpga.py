from manim import *

config.pixel_height = 720
config.pixel_width = 960
config.frame_rate = 50
config.preview = True

class HardwareConvolution(Scene):
    def construct(self):
        # --- 1. SETUP THE 24x16 GRIDS ---
        def create_arch(title_text, core_text, color):
            grid = VGroup(*[Square(side_length=0.2, stroke_color=color, stroke_width=1, fill_opacity=0.1) for _ in range(384)])
            grid.arrange_in_grid(rows=24, cols=16, buff=0)
            title = Text(title_text, font_size=20).next_to(grid, UP, buff=0.15)
            subtitle = Text(core_text, font_size=14, color=color).next_to(title, UP, buff=0.05)
            return VGroup(subtitle, title, grid), grid

        cpu_ui, cpu_grid = create_arch("CPU (Sequential)", "8 cores", BLUE_E)
        gpu_ui, gpu_grid = create_arch("GPU (Batches)", "64×16 cores", GREEN_E)
        fpga_ui, fpga_grid = create_arch("FPGA (Spatial)", "6×4×8 DSP slices", ORANGE)

        VGroup(cpu_ui, gpu_ui, fpga_ui).arrange(RIGHT, buff=0.4)

        main_title = Text("Average Convolution Performance Comparison", font_size=32, weight=BOLD)
        main_title.to_edge(UP, buff=0.3)

        # Shift the grid group down so it sits below the title with some breathing room
        VGroup(cpu_ui, gpu_ui, fpga_ui).next_to(main_title, DOWN, buff=0.4)

        self.play(
            FadeIn(main_title),
            FadeIn(cpu_ui), FadeIn(gpu_ui), FadeIn(fpga_ui),
            run_time=1
        )

        # --- 2. READY THE FILTERS ---

        # CPU: 1x1 Rectangle
        cpu_filter = Rectangle(width=0.2, height=0.2, stroke_color=RED, stroke_width=4)
        cpu_filter.move_to(cpu_grid[0].get_center())

        # GPU: 64 distributed Cores (every 3 rows, every 2 cols → 8×8)
        gpu_filter = VGroup()
        for r in range(0, 24, 3):
            for c in range(0, 16, 2):
                rect = Rectangle(width=0.2, height=0.2, stroke_color=YELLOW, stroke_width=4)
                rect.move_to(gpu_grid[r * 16 + c].get_center())
                gpu_filter.add(rect)

        # FPGA: 6-row x 4-col Spatial Array
        fpga_filter = Rectangle(width=0.8, height=1.2, stroke_color=ORANGE, stroke_width=6)
        fpga_filter.move_to(fpga_grid[0].get_corner(UL) + RIGHT*0.4 + DOWN*0.6)

        self.play(Create(cpu_filter), Create(gpu_filter), Create(fpga_filter))
        self.wait(0.5)

        # --- 3. PRECOMPUTE ALL TARGET POSITIONS ---

        # CPU: full 24x16 snake scan (row-by-row, alternating direction)
        cpu_positions = []
        for r in range(24):
            row_indices = range(r * 16, (r + 1) * 16)
            if r % 2 != 0:
                row_indices = reversed(row_indices)
            for i in row_indices:
                cpu_positions.append(cpu_grid[i].get_center())

        # GPU: 4-step local snake (row gap=2 so only 2 DOWN steps needed)
        # RIGHT covers col gaps, DOWN×2 covers the 2 row gaps
        gpu_start = gpu_filter.get_center().copy()
        gpu_deltas = [RIGHT*0.2, DOWN*0.2, LEFT*0.2, DOWN*0.2]
        gpu_positions = [gpu_start]
        for d in gpu_deltas:
            gpu_positions.append(gpu_positions[-1] + d)

        # FPGA: 4x4 grid of 6-row x 4-col kernel positions, snake order
        fpga_positions = []
        for r in range(4):
            for c in range(4):
                actual_c = c if r % 2 == 0 else 3 - c
                idx = (r * 6) * 16 + (actual_c * 4)
                fpga_positions.append(fpga_grid[idx].get_corner(UL) + RIGHT*0.4 + DOWN*0.6)

        # --- 4. CONCURRENT UPDATER ANIMATION ---
        # Each filter has its own dt accumulator and step index.
        # When accumulated time crosses the step threshold, it moves to the next position.

        #for making speed differencec more obvious to technical people:
        #
        CPU_STEP  = 0.04   # 60x speed 
        GPU_STEP  = 0.10   # 12x speed
        FPGA_STEP = 0.30   # 4x speed
        # CPU_STEP  = 0.04   # 40x speed
        # GPU_STEP  = 0.10   # 15x speed
        # FPGA_STEP = 0.32   # 5x speed

        # Pre-calculate total time for each device and show below their grids
        cpu_total = len(cpu_positions) * CPU_STEP
        gpu_total = (len(gpu_positions) - 1) * GPU_STEP
        fpga_total = (len(fpga_positions) - 1) * FPGA_STEP

        cpu_time_label  = Text(f"Total: {cpu_total:.2f}s",  font_size=14, color=BLUE_E ).next_to(cpu_grid,  DOWN, buff=0.1)
        gpu_time_label  = Text(f"Total: {gpu_total:.2f}s",  font_size=14, color=GREEN_E).next_to(gpu_grid,  DOWN, buff=0.1)
        fpga_time_label = Text(f"Total: {fpga_total:.2f}s", font_size=14, color=ORANGE ).next_to(fpga_grid, DOWN, buff=0.1)
        self.play(FadeIn(cpu_time_label), FadeIn(gpu_time_label), FadeIn(fpga_time_label), run_time=0.5)

        state = {
            "cpu_acc": 0.0, "cpu_idx": 0,
            "gpu_acc": 0.0, "gpu_idx": 0,
            "fpga_acc": 0.0, "fpga_idx": 0,
        }

        def cpu_updater(mob, dt):
            state["cpu_acc"] += dt
            new_idx = int(state["cpu_acc"] / CPU_STEP)
            if new_idx > state["cpu_idx"]:
                state["cpu_idx"] = min(new_idx, len(cpu_positions) - 1)
                mob.move_to(cpu_positions[state["cpu_idx"]])
                # Flash: alternate color each step
                mob.set_stroke(color=(GREEN if state["cpu_idx"] % 2 == 0 else RED))

        def gpu_updater(mob, dt):
            state["gpu_acc"] += dt
            new_idx = int(state["gpu_acc"] / GPU_STEP)
            if new_idx > state["gpu_idx"]:
                state["gpu_idx"] = min(new_idx, len(gpu_positions) - 1)
                mob.move_to(gpu_positions[state["gpu_idx"]])
                mob.set_stroke(color=(WHITE if state["gpu_idx"] % 2 == 0 else YELLOW))

        def fpga_updater(mob, dt):
            state["fpga_acc"] += dt
            new_idx = int(state["fpga_acc"] / FPGA_STEP)
            if new_idx > state["fpga_idx"]:
                state["fpga_idx"] = min(new_idx, len(fpga_positions) - 1)
                mob.move_to(fpga_positions[state["fpga_idx"]])

        cpu_filter.add_updater(cpu_updater)
        gpu_filter.add_updater(gpu_updater)
        fpga_filter.add_updater(fpga_updater)

        # Run until CPU finishes its full snake (384 cells * 0.02s each)
        total_time = len(cpu_positions) * CPU_STEP
        self.wait(total_time)

        cpu_filter.remove_updater(cpu_updater)
        gpu_filter.remove_updater(gpu_updater)
        fpga_filter.remove_updater(fpga_updater)
        self.wait(1)

if __name__ == "__main__":
    scene = HardwareConvolution()
    scene.render()