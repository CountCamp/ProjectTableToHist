import numpy as np
from manim import *


class MonkeyStats1(Scene):
    def construct(self):
        # ======================================================
        # 1. TITLE AND DATASET DISPLAY
        # ======================================================
        title = Text("Berekening van Gemiddelde en Standaardafwijking", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Define the dataset for the 9 monkeys.
        # (For example, these could represent the weights or scores of 9 monkeys.)
        monkey_data = [2, 3, 4, 4, 5, 7, 8, 9, 10]
        n = len(monkey_data)

        # Display the dataset as a row of numbers.
        data_text = VGroup(*[Text(str(val), font_size=30) for val in monkey_data])
        data_text.arrange(RIGHT, buff=0.5)
        data_text.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(data_text))
        self.wait(1)

        # ======================================================
        # 2. CALCULATE THE MEAN
        # ======================================================
        # Show the formula for the mean.
        mean_formula = MathTex(r"\bar{x}=\frac{x_1+x_2+\cdots+x_n}{n}", font_size=36)
        mean_formula.next_to(data_text, DOWN, buff=1)
        self.play(Write(mean_formula))
        self.wait(1)

        # Calculate the total sum and mean.
        total = sum(monkey_data)
        mean_value = total / n

        # Display the sum.
        sum_text = Text(f"Som = {total}", font_size=30)
        sum_text.next_to(mean_formula, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(FadeIn(sum_text))
        self.wait(1)

        # Show the division leading to the mean.
        division_text = Text(
            f"Gemiddelde = {total} / {n} = {mean_value:.2f}", font_size=30
        )
        division_text.next_to(sum_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(division_text))
        self.wait(2)

        # Optionally, illustrate the mean on a number line.
        # (Here we create a dashed vertical line at the x-coordinate corresponding to the mean.)
        mean_line = DashedLine(
            start=mean_formula.get_bottom() + DOWN * 0.5,
            end=mean_formula.get_bottom() + DOWN * 3,
            color=RED,
        )
        mean_label = Text(f"x̄ = {mean_value:.2f}", font_size=30, color=RED)
        mean_label.next_to(mean_line, RIGHT, buff=0.2)
        self.play(Create(mean_line), Write(mean_label))
        self.wait(2)

        # ======================================================
        # 3. CALCULATE THE STANDAARDAFWIJKING (STANDARD DEVIATION)
        # ======================================================
        # Display the formula for standard deviation.
        std_formula = MathTex(
            r"\sigma=\sqrt{\frac{(x_1-\bar{x})^2+(x_2-\bar{x})^2+\cdots+(x_n-\bar{x})^2}{n}}",
            font_size=36,
        )
        std_formula.next_to(division_text, DOWN, buff=1)
        self.play(Write(std_formula))
        self.wait(1)

        # For each data point, compute and display the difference and its square.
        diff_texts = VGroup()
        sq_texts = VGroup()
        for i, x in enumerate(monkey_data):
            diff = x - mean_value
            sq = diff**2
            diff_item = Text(f"{x} - {mean_value:.2f} = {diff:.2f}", font_size=24)
            sq_item = Text(f"({diff:.2f})² = {sq:.2f}", font_size=24)
            diff_texts.add(diff_item)
            sq_texts.add(sq_item)
        diff_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sq_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        diff_texts.to_edge(LEFT, buff=1)
        sq_texts.next_to(diff_texts, RIGHT, buff=1)
        self.play(FadeIn(diff_texts), FadeIn(sq_texts))
        self.wait(2)

        # Sum the squared differences and calculate standard deviation.
        sum_squared = sum([(x - mean_value) ** 2 for x in monkey_data])
        std_value = np.sqrt(sum_squared / n)
        sum_sq_text = Text(f"Som kwadraten = {sum_squared:.2f}", font_size=30)
        sum_sq_text.next_to(sq_texts, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(FadeIn(sum_sq_text))
        self.wait(1)

        std_text = Text(f"σ = √({sum_squared:.2f}/{n}) = {std_value:.2f}", font_size=30)
        std_text.next_to(sum_sq_text, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(std_text))
        self.wait(3)

        # Clean up the intermediate texts (if desired) so that only the key results remain.
        self.play(
            FadeOut(diff_texts),
            FadeOut(sq_texts),
            FadeOut(sum_sq_text),
            FadeOut(std_formula),
        )
        self.wait(2)
