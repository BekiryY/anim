from manim import *

"""
This script is a Manim project that creates a simulation of a memory filling up with data packets.
It uses the Manim library to create the animation.


"""
config.quality = "low_quality"
config.preview = True
config.frame_rate = 30

class MemoryFill(Scene):
    def construct(self):
        # 1. Create Data Packet and Memory Block
        data_packet = Circle(radius=0.2, color=BLUE, fill_opacity=1).shift(LEFT * 4)
        
        memory_bank = Rectangle(height=3, width=2, color=WHITE).shift(RIGHT * 2)
        memory_label = Text("SRAM").scale(0.5).next_to(memory_bank, UP)
        
        # 2. Moving and Glowing Effect
        self.play(FadeIn(data_packet), Create(memory_bank), Write(memory_label))
        
        # Move packet and change color to simulate a "glow" or activation
        self.play(
            data_packet.animate.shift(RIGHT * 6.0).set_color(YELLOW), 
            run_time=1.5
        )
        
        # Packet fades out as it "enters" memory
        self.play(FadeOut(data_packet), run_time=0.5)

        # 3. Simulate Memory Filling Up
        # Create a tiny green fill box at the bottom of the memory
        fill_box = Rectangle(width=1.9, height=0.1, fill_color=GREEN, fill_opacity=0.8, stroke_width=0)
        fill_box.align_to(memory_bank, UR).shift(DL * 0.05)
        
        self.add(fill_box)
        
        # Animate the fill box stretching to the top
        self.play(
            fill_box.animate.stretch_to_fit_height(2.9).align_to(memory_bank, UR).shift(DL * 0.05),
            run_time=1
        )
        self.wait()

if __name__ == "__main__":
    my_scene = MemoryFill()  # Instantiate the object
    my_scene.construct()     # Call the method
    my_scene.render()
