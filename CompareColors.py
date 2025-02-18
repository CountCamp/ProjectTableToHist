from manim import *


class CompareColors(Scene):
    def construct(self):
        # --- Title ---
        title = Text("Extended Color Comparison", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # --- Define Colors ---
        venetian_pinks = [
            ("#E6A8D7", "Venetian Pink 1"),
            ("#C76E6E", "Venetian Pink 2"),
            ("#CC7A8B", "Venetian Pink 3"),
            ("#B36A75", "Venetian Pink 4"),
        ]

        greens = [
            ("#808000", "Olive 1"),
            ("#6B8E23", "Olive 2"),
            ("#556B2F", "Olive 3"),
            ("#9ACD32", "Lime Green"),
            ("#A2A23A", "Soft Olive"),
            ("#228B22", "Forest Green"),
            ("#32CD32", "Bright Green"),
        ]

        gold_shades = [
            ("#FFD700", "Gold (GOLD_E)"),
            ("#FFA500", "Orange (GOLD_A)"),
            ("#FFC125", "Light Gold"),
            ("#DAA520", "Dark Gold"),
            ("#FFCC33", "Classic Gold"),
            ("#D4AF37", "Rich Gold"),
            ("#E5C100", "Deep Gold"),
        ]

        def create_color_block(hex_code, label, position):
            """Helper function to create a color box with text inside."""
            box = Rectangle(width=2.5, height=1, fill_color=hex_code, fill_opacity=1)
            text_color = (
                BLACK
                if hex_code in ["#FFC125", "#FFD700", "#FFCC33", "#E5C100"]
                else WHITE
            )
            hex_text = Text(hex_code, font_size=20, color=text_color).move_to(
                box.get_center()
            )
            label_text = Text(label, font_size=24, color=WHITE).next_to(
                box, RIGHT, buff=0.3
            )
            group = VGroup(box, hex_text, label_text).arrange(RIGHT, buff=0.3)
            group.move_to(position)
            return group

        # --- Display Venetian Pinks ---
        venetian_group = VGroup(
            *[
                create_color_block(hex_code, label, LEFT * 5 + UP * (1.5 - i))
                for i, (hex_code, label) in enumerate(venetian_pinks)
            ]
        )
        self.play(FadeIn(venetian_group))

        # --- Display Greens ---
        green_group = VGroup(
            *[
                create_color_block(hex_code, label, LEFT * 1 + UP * (3 - i))
                for i, (hex_code, label) in enumerate(greens)
            ]
        )
        self.play(FadeIn(green_group))

        # --- Display Gold Shades ---
        gold_group = VGroup(
            *[
                create_color_block(hex_code, label, RIGHT * 4 + UP * (3 - i))
                for i, (hex_code, label) in enumerate(gold_shades)
            ]
        )
        self.play(FadeIn(gold_group))

        # Pause for viewing
        self.wait(10)
