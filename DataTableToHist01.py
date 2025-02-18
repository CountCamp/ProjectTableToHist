import pandas as pd
from manim import (
    Scene,
    NumberPlane,
    VGroup,
    Text,
    Rectangle,
    GOLD_E,
    GOLD_A,
    RED,
    WHITE,
    UP,
    config,
    Create,
    LEFT,
    RIGHT,
    PI,
    Dot,
    BLUE,
    GREY,
    FadeIn,
    FadeOut,
    smooth,
    NumberLine,
    DOWN,
    Write,
    Transform,
    Line,
    Arrow,
)


class DataToHist01(Scene):
    def construct(self):
        # ======================================================
        # 1. SET UP THE BACKGROUND GRID
        # ======================================================
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": GREY,  # grid line color
                "stroke_width": 1,  # grid line thickness
                "stroke_opacity": 0.5,  # grid line opacity
            },
            axis_config={
                "stroke_color": GREY,  # axis color
                "stroke_width": 1,  # axis thickness
            },
        )
        self.add(grid)

        # ======================================================
        # 2. LOAD AND PREPARE THE DATA
        # ======================================================
        data = pd.read_csv("Data/geslacht_leeftijd_data.csv", index_col=False)
        if "Unnamed: 0" in data.columns:
            data = data.drop(columns=["Unnamed: 0"])
        data = data.head(100)
        print(f"Total observations in data: {len(data)}")
        data.columns = ["ID", "Geslacht", "Leeftijd"]
        data["Geslacht"] = data["Geslacht"].replace({"Female": "Vrouw", "Male": "Man"})
        print(data.head(3))
        rows = [list(data.columns)] + data.values.tolist()

        # ======================================================
        # 3. DEFINE PARAMETERS FOR THE TABLE
        # ======================================================
        column_widths = [1, 2, 2]  # widths for each column
        y_spacing = 0.75  # vertical spacing between rows
        x_positions = [
            sum(column_widths[:j]) + column_widths[j] / 2 - sum(column_widths) / 2
            for j in range(len(column_widths))
        ]

        # ======================================================
        # 4. CREATE THE FULL TABLE (ALL ROWS)
        # ======================================================
        table = VGroup()
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                cell_text = (
                    Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)
                    if i == 0
                    else Text(str(value), color=GOLD_A).scale(0.5)
                )
                cell_border = Rectangle(
                    width=column_widths[j], height=y_spacing, color=GOLD_A
                )
                cell_text.move_to([x_positions[j], -i * y_spacing, 0])
                cell_border.move_to([x_positions[j], -i * y_spacing, 0])
                table.add(VGroup(cell_border, cell_text))
        table.shift(UP * (config.frame_height / 2 - table.get_top()[1]))
        self.play(Create(table), run_time=5)
        self.wait()

        # ======================================================
        # 5. SCROLL THE FULL TABLE TO REVEAL THE BOTTOM
        # ======================================================
        table_bottom_y = table.get_bottom()[1]
        screen_bottom_y = -config.frame_height / 2
        scroll_vector = DOWN * (table_bottom_y - screen_bottom_y) + UP * (
            y_spacing * 4 / 3
        )
        self.play(table.animate.shift(scroll_vector), run_time=6, rate_func=smooth)
        self.wait()

        # ======================================================
        # 6. CREATE THE REDUCED TABLE (TOP 6, DUMMY, BOTTOM 3)
        # ======================================================
        top_rows = data.head(6)
        bottom_rows = data.tail(3)
        dummy_row = pd.DataFrame([["...", "...", "..."]], columns=data.columns)
        combined_data = pd.concat([top_rows, dummy_row, bottom_rows], ignore_index=True)
        reduced_rows = [list(combined_data.columns)] + combined_data.values.tolist()

        reduced_table = VGroup()
        for i, row in enumerate(reduced_rows):
            for j, value in enumerate(row):
                if 7 <= i < len(reduced_rows) - 3:
                    if j == 1:
                        dots = VGroup(
                            Text("...").move_to([x_positions[0], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[1], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[2], -i * y_spacing, 0]),
                        )
                        reduced_table.add(dots)
                    continue
                cell_text = (
                    Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)
                    if i == 0
                    else Text(str(value), color=GOLD_A).scale(0.5)
                )
                cell_border = Rectangle(
                    width=column_widths[j], height=y_spacing, color=GOLD_A
                )
                cell_text.move_to([x_positions[j], -i * y_spacing, 0])
                cell_border.move_to([x_positions[j], -i * y_spacing, 0])
                reduced_table.add(VGroup(cell_border, cell_text))
        reduced_table.scale(0.7)
        reduced_table.to_edge(LEFT)
        reduced_table.shift(UP * (3 - reduced_table.get_top()[1]))
        self.play(FadeOut(table), FadeIn(reduced_table), run_time=3)
        self.wait()

        # ======================================================
        # 7. SET UP STATISTICS & AXIS PARAMETERS
        # ======================================================
        leeftijden = data["Leeftijd"].tolist()
        print(f"Unique ages in dataset: {set(leeftijden)}")
        min_age = data["Leeftijd"].min()
        max_age = data["Leeftijd"].max()
        mode_age = data["Leeftijd"].mode()[0]
        max_freq = data["Leeftijd"].value_counts().max()
        print(
            f"Min Age: {min_age}, Max Age: {max_age}, Mode Age: {mode_age}, Max Frequency: {max_freq}"
        )
        horizontal_start, horizontal_end = [-1, -2.5, 0], [6, -2.5, 0]
        vertical_start, vertical_end = [-1, -2.5, 0], [-1, 3, 0]
        total_vertical_height = vertical_end[1] - vertical_start[1]
        num_ticks = max_freq + 2
        vertical_step = total_vertical_height / num_ticks

        # ======================================================
        # 8. CREATE THE HORIZONTAL NUMBER LINE (AXIS)
        # ======================================================
        number_line = NumberLine(
            x_range=[min_age - 1, max_age + 1, 1],
            length=horizontal_end[0] - horizontal_start[0],
            include_numbers=True,
            color=GOLD_E,
        )
        number_line.shift(horizontal_start - number_line.get_start())
        self.add(number_line)
        self.wait(2)

        # ======================================================
        # 9. CREATE THE VERTICAL AXIS, TICKS, & LABELS
        # ======================================================
        vertical_line = Line(start=vertical_start, end=vertical_end, color=GOLD_E)
        vertical_ticks = VGroup()
        for i in range(num_ticks + 1):
            tick = Line(start=LEFT * 0.1, end=RIGHT * 0.1, color=GOLD_E).move_to(
                vertical_start + UP * i * vertical_step
            )
            label = Text(str(i), font_size=20, color=GOLD_E).next_to(
                tick, LEFT, buff=0.2
            )
            vertical_ticks.add(tick, label)
        vertical_label = (
            Text("Frequentie", font_size=24, color=GOLD_E)
            .rotate(PI / 2)
            .next_to(vertical_line, LEFT, buff=0.8)
        )
        horizontal_label = Text(
            "Leeftijd in jaren", font_size=24, color=GOLD_E
        ).next_to(number_line, DOWN)
        self.play(
            Create(number_line),
            Create(vertical_line),
            Create(vertical_ticks),
            Write(vertical_label),
            Write(horizontal_label),
        )

        # ======================================================
        # 10. ANIMATE DOT TRANSFER & RUNNING-MEAN INDICATOR
        # ======================================================
        # Initialize running-mean data.
        animated_ages = []  # List of all ages that have been animated (for computing the mean)
        frequencies = {}  # Dictionary: age -> number of dots already placed
        mean_indicator = None  # Will hold the arrow+label for the mean

        # Helper: create a mean indicator (arrow + label) at the x-coordinate for the mean.
        def create_mean_indicator(mean_val):
            start = number_line.n2p(mean_val)
            end = start + UP * 3  # arrow length = 3 units
            arrow = Arrow(start, end, buff=0, color=RED)
            label = Text(f"x̄ = {mean_val:.1f}", font_size=40, color=RED).next_to(
                arrow, UP, buff=0.2
            )
            return VGroup(arrow, label)

        points = VGroup()  # Group to hold all animated blue dots
        processed_ages = set()  # Record which ages have been processed

        print("Ages being processed for dots:")
        for age in leeftijden:
            print(age)

        # -- Animate Top Rows (cells 1-6) --
        for i, row in enumerate(rows[1:7]):
            age = row[2]
            # Get the center of the cell from the reduced table (using an appropriate index offset)
            cell_center = reduced_table[(i + 1) * 3 + 2].get_center()
            processed_ages.add(age)
            # Highlight the cell temporarily.
            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(cell_center)
            self.play(Create(highlight_cell), run_time=0.5)
            # Create a temporary text copy for the animation.
            anim_text = Text(str(age), color=RED).scale(0.5).move_to(cell_center)
            self.play(FadeIn(anim_text), run_time=0.5)
            # Compute target position using the frequency for this age.
            target_position = (
                number_line.n2p(age)
                + UP * (frequencies.get(age, 0) + 1) * vertical_step
            )
            new_dot = Dot(color=BLUE).move_to(cell_center)
            self.play(
                Transform(new_dot, Dot(color=BLUE).move_to(target_position)),
                run_time=0.7,
            )
            self.play(FadeOut(anim_text), run_time=0.3)
            animated_ages.append(age)
            frequencies.setdefault(age, 0)
            frequencies[age] += 1
            points.add(new_dot)
            self.play(FadeOut(highlight_cell), run_time=0.2)
            # Update the running mean indicator if at least 2 dots exist.
            if len(animated_ages) >= 2:
                current_mean = sum(animated_ages) / len(animated_ages)
                new_indicator = create_mean_indicator(current_mean)
                if mean_indicator is None:
                    mean_indicator = new_indicator
                    self.play(FadeIn(mean_indicator), run_time=1)
                else:
                    self.play(Transform(mean_indicator, new_indicator), run_time=1)
                    # Bring the mean indicator to the front after updating.
                    mean_indicator.set_z_index(10)
                self.wait(0.3)

        # -- Animate Middle Rows (ages from index 6 to -3) --
        for age in leeftijden[6:-3]:
            processed_ages.add(age)
            animated_ages.append(age)
            # Use a starting position offset from the reduced table.
            start_position = reduced_table[7 * 3].get_center() + RIGHT * 1
            point = Dot(color=BLUE).move_to(start_position)
            target_position = (
                number_line.n2p(age)
                + UP * (frequencies.get(age, 0) + 1) * vertical_step
            )
            self.play(point.animate.move_to(target_position), run_time=0.1)
            frequencies.setdefault(age, 0)
            frequencies[age] += 1
            points.add(point)
            # Update mean indicator.
            current_mean = sum(animated_ages) / len(animated_ages)
            new_indicator = create_mean_indicator(current_mean)
            if mean_indicator is None:
                mean_indicator = new_indicator
                self.play(FadeIn(mean_indicator), run_time=1)
            else:
                self.play(Transform(mean_indicator, new_indicator), run_time=1)
            self.wait(0.2)

        # -- Animate Bottom Rows (last 3 cells) --
        for i, row in enumerate(reduced_rows[-3:]):
            age = row[2]
            cell_center = reduced_table[(8 * 3 + i * 3)].get_center()
            processed_ages.add(age)
            animated_ages.append(age)
            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(cell_center)
            self.play(Create(highlight_cell), run_time=0.5)
            anim_text = Text(str(age), color=RED).scale(0.5).move_to(cell_center)
            self.play(FadeIn(anim_text), run_time=0.5)
            target_position = (
                number_line.n2p(age)
                + UP * (frequencies.get(age, 0) + 1) * vertical_step
            )
            new_dot = Dot(color=BLUE).move_to(cell_center)
            self.play(
                Transform(new_dot, Dot(color=BLUE).move_to(target_position)),
                run_time=0.7,
            )
            self.play(FadeOut(anim_text), run_time=0.3)
            frequencies.setdefault(age, 0)
            frequencies[age] += 1
            points.add(new_dot)
            self.play(FadeOut(highlight_cell), run_time=0.2)
            # Update mean indicator.
            current_mean = sum(animated_ages) / len(animated_ages)
            new_indicator = create_mean_indicator(current_mean)
            if mean_indicator is None:
                mean_indicator = new_indicator
                self.play(FadeIn(mean_indicator), run_time=1)
            else:
                self.play(Transform(mean_indicator, new_indicator), run_time=1)
            self.wait(0.2)

        self.wait(2)

        # ======================================================
        # 11. BUILD THE HISTOGRAM BARS & TRANSITION FROM DOTS
        # ======================================================
        bars = VGroup()
        for age, freq in frequencies.items():
            bar = Rectangle(
                width=0.4,
                height=freq * vertical_step,
                color=BLUE,
                fill_opacity=0.7,
            ).next_to(number_line.n2p(age), UP, buff=0)
            bars.add(bar)
        print(f"Missing age: {set(leeftijden) - processed_ages}")
        print(f"Total points stored: {len(points)}")
        for i, dot in enumerate(points):
            print(f"Dot {i + 1} at position: {dot.get_center()}")
        self.play(FadeOut(points), run_time=0.5)
        self.play(FadeIn(bars))

        # ======================================================
        # 12. CREATE AND POSITION THE TITLE
        # ======================================================
        title = Text("Histogram voor Leeftijd", font_size=32, color=GOLD_E).to_edge(
            UP, buff=1
        )
        # Center the title horizontally relative to the number line and shift it upward.
        title.move_to([number_line.get_center()[0], title.get_center()[1], 0])
        title.shift(UP * 0.5)
        self.play(Write(title))
        self.wait(3)


# Specific for this script: One group, Histogram and Running Mean Indicator
# Run the scene
# manim -qm DataTableToHist01.py DataToHist01
