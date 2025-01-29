import pandas as pd
from manim import *

class DataToHist2(Scene):
    def construct(self):
        # Add a unit grid with main axes crossing at the center of the screen
        # By default, the grid lines are grey and have a resolution of 1
        # To change grid settings, use grid_color and axis_config arguments
        # To change line thickness, use grid_line_config and axis_config arguments
        # Create a unit grid with a resolution of 1
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
            # stroke_color is the color of the lines
            "stroke_color": GREY,
            # stroke_width is the thickness of the lines
            "stroke_width": 1,
            # stroke_opacity is the opacity of the lines  
            "stroke_opacity": 0.5
            },
            axis_config={
            # color of the axes
            "stroke_color": GREY,
            # stroke_width is the thickness of the lines
            "stroke_width": 1
            }
        )

        self.add(grid)


        # Load the dataset without the index column
        data = pd.read_csv("geslacht_leeftijd_data.csv", index_col=False)
        if "Unnamed: 0" in data.columns:
            data = data.drop(columns=["Unnamed: 0"])

        # Select only the first 100 rows
        data = data.head(100)

        # Rename column headers and replace gender labels
        data.columns = ["ID", "Geslacht", "Leeftijd"]
        data["Geslacht"] = data["Geslacht"].replace({"Female": "Vrouw", "Male": "Man"})

        # Convert the DataFrame to a list of rows (including header)
        rows = [list(data.columns)] + data.values.tolist()

        # Create a group to hold all table cells
        table = VGroup()

        # Define column-specific spacing
        # Narrower width for 'ID', wider for others
        column_widths = [1, 2, 2]  
        # Vertical spacing
        y_spacing = 0.75

        # Precompute x_positions for all columns
        # For the first column (j = 0): (1) + (1) / 2  - (5) / 2 = -1
        # For the second column (j = 1): (1 + 2) + (2) / 2 - (5) / 2 = 1.5
        # For the third column (j = 2): (1 + 2 + 2) + (2) / 2 - (5) / 2 = 3.5
        x_positions = [
            sum(column_widths[:j]) + column_widths[j] / 2 - sum(column_widths) / 2
            for j in range(len(column_widths))
        ]

        # Generate table cells with borders
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                # Header row styling
                if i == 0:
                    # Darker gold for header
                    cell_text = Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)  
                else:
                    # Regular gold for data
                    cell_text = Text(str(value), color=GOLD_A).scale(0.5)

                # Create a rectangle for the cell border
                cell_border = Rectangle(width=column_widths[j], height=y_spacing, color=GOLD_A)

                # Use precomputed x_position
                # for j = 0: x_positions[0] = -1, for j = 1: x_positions[1] = 1.5, for j = 2: x_positions[2] = 3.5
                x_position = x_positions[j]
                # Position the cell
                # For i = 0: y_position = 0, for i = 1: y_position = -0.75, for i = 2: y_position = -1.5, etc.
                cell_text.move_to([x_position, -i * y_spacing, 0])
                cell_border.move_to([x_position, -i * y_spacing, 0])

                # Group the text and border together
                cell = VGroup(cell_border, cell_text)
                # Add the cell to the table group
                table.add(cell)

        # Step 1: Show table with top just below the screen's top
        # Using 3D coordinates to shift the table upwards
        table_top_y =  table.get_top()[1] # 1 means the y-coordinate of the top of the table
        # Adjust this value for fine-tuning
        target_top_y = config.frame_height / 2 #  Half of the screen height
        # Shift the table up by the difference
        table.shift(UP * (target_top_y - table_top_y))
        self.play(Create(table), run_time=5)  # Slow creation for visibility, use rate function maybe for first bit slow later fast.
        self.wait()

        # Step 2: Scroll down to show the bottom of the table and move up slightly to reveal the bottom row clearly
        # Bottom of the table in 3D coordinates
        table_bottom_y = table.get_bottom()[1] # 1 means the y-coordinate of the bottom of the table
        # Bottom of the screen in 3D coordinates
        screen_bottom_y = -config.frame_height / 2  # Half of the screen height
        self.play(
            # Scrolling down to reveal the bottom row
            table.animate.shift(DOWN * (table_bottom_y - screen_bottom_y) + UP * y_spacing * 4 / 3),  # Combine both movements
            run_time=6,
            # Slow scrolling for clarity, what kind of scrolling? Linear, smooth, etc.
            rate_func = smooth
        )
        self.wait()

        # Step 3: Move the table to the left and display only key rows
        # Select first 7 rows and last 3 rows
        top_rows = data.head(7)
        bottom_rows = data.tail(3)
        combined_data = pd.concat([top_rows, bottom_rows], axis=0)

        # Convert the reduced DataFrame to a list of rows (including header)
        reduced_rows = [list(combined_data.columns)] + combined_data.values.tolist()

        # Create a reduced table
        reduced_table = VGroup()

        for i, row in enumerate(reduced_rows):
            for j, value in enumerate(row):
                # Add dots for the missing rows
                if 7 <= i < len(reduced_rows) - 3:
                    if j == 1:  # Add dots only once per row
                        dots = VGroup(
                            Text("...").move_to([x_positions[0], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[1], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[2], -i * y_spacing, 0])
                        )
                        reduced_table.add(dots)
                    continue

                # Header row styling
                if i == 0:
                    cell_text = Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)  # Donkergeel voor kolomnamen
                else:
                    cell_text = Text(str(value), color=GOLD_A).scale(0.5)  # Zacht geel voor data

                cell_border = Rectangle(width=column_widths[j], height=y_spacing, color=GOLD_A)
                x_position = x_positions[j]  # Use precomputed x_position
                cell_text.move_to([x_position, -i * y_spacing, 0])
                cell_border.move_to([x_position, -i * y_spacing, 0])

                # Group the text and border together
                cell = VGroup(cell_border, cell_text)
                reduced_table.add(cell)

        # Scale down 
        reduced_table.scale(0.7)
        # Move the table to the left edge of the screen
        reduced_table.to_edge(LEFT)
        # Adjust the y-position of the table to be centered vertically
        reduced_table_top_y = reduced_table.get_top()[1]
        final_top_y = 3
        # Shift the table up by the difference between the current top y and the desired top y
        reduced_table.shift(UP * (final_top_y - reduced_table_top_y))

        # Replace the original table with the reduced table
        self.play(FadeOut(table), FadeIn(reduced_table), run_time=3)
        self.wait()

        # Load dataset and prepare statistics
        leeftijden = data["Leeftijd"].tolist()

        # Calculate stats
        min_leeftijd = min(leeftijden)
        max_leeftijd = max(leeftijden)
        # for height of the bars
        modus = max(set(leeftijden), key=leeftijden.count)
        max_freq = leeftijden.count(modus)

        # Scaling factors
        vertical_step = 0.4  # Adjusted for better proportionality
        total_vertical_height = (max_freq + 1) * vertical_step

        # Create horizontal number line on the right
        number_line = NumberLine(
            x_range=[min_leeftijd - 1, max_leeftijd + 1, 1],
            length=7,  # Adjusted for better spacing
            include_numbers=True,
            color=GOLD_E
        ).to_edge(RIGHT).shift(DOWN * 2)

        # Add vertical axis with labels
        vertical_line = Line(
            start=number_line.get_left() + UP * 0.5,
            end=number_line.get_left() + UP * total_vertical_height,
            color=GOLD_E
        )
        vertical_ticks = VGroup()
        for i in range(0, max_freq + 2, 5):
            tick = Line(start=LEFT * 0.1, end=RIGHT * 0.1, color=GOLD_E).move_to(
                vertical_line.get_start() + UP * i * vertical_step
            )
            label = Text(str(i), font_size=20, color=GOLD_E).next_to(tick, LEFT, buff=0.2)
            vertical_ticks.add(tick, label)

        vertical_label = Text("Frequentie", font_size=24, color=GOLD_E).rotate(PI / 2).next_to(vertical_line, LEFT, buff=0.5)
        horizontal_label = Text("Leeftijd in jaren", font_size=24, color=GOLD_E).next_to(number_line, DOWN)

        self.play(Create(number_line), Create(vertical_line), Create(vertical_ticks), Write(vertical_label), Write(horizontal_label))

        # Animate first 6 values moving to number line
        points = VGroup()
        frequencies = {}

        for i, row in enumerate(rows[1:7]):
            leeftijd = row[2]
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            # Highlight cell
            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(reduced_table[(i + 1) * 3 + 2].get_center())
            self.play(Create(highlight_cell), run_time=0.5)

            # Animate value moving out of table and turning into a point
            value_text = Text(str(leeftijd), color=WHITE).move_to(reduced_table[(i + 1) * 3 + 2].get_center())
            self.play(FadeIn(value_text), run_time=0.5)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            point = Dot(color=BLUE).move_to(target_position)
            self.play(
                value_text.animate.move_to(target_position),
                Transform(value_text, point),
                run_time=0.7
            )
            frequencies[leeftijd] += 1
            points.add(point)

            # Remove highlight
            self.play(FadeOut(highlight_cell), run_time=0.2)

        # Animate values from "..."
        for leeftijd in leeftijden[7:-3]:
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            # Simulate point moving from "..."
            start_position = reduced_table[7 * 3 ].get_center() + RIGHT * 1  # Corrected start row
            point = Dot(color=BLUE).move_to(start_position)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            self.play(point.animate.move_to(target_position), run_time=0.05)
            frequencies[leeftijd] += 1
            points.add(point)

        # Animate last 3 values
        for i, row in enumerate(reduced_rows[-3:]):
            leeftijd = row[2]
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(reduced_table[(8 * 3 + i * 3)].get_center())
            self.play(Create(highlight_cell), run_time=0.5)

            value_text = Text(str(leeftijd), color=WHITE).move_to(reduced_table[(8 * 3 + i * 3)].get_center())
            self.play(FadeIn(value_text), run_time=0.5)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            point = Dot(color=BLUE).move_to(target_position)
            self.play(
                value_text.animate.move_to(target_position),
                Transform(value_text, point),
                run_time=0.7
            )
            frequencies[leeftijd] += 1
            points.add(point)

            self.play(FadeOut(highlight_cell), run_time=0.2)

        # Pause and then transform to histogram
        self.wait(2)
        bars = VGroup()

        for leeftijd, freq in frequencies.items():
            bar = Rectangle(
                width=0.4, height=freq * vertical_step, color=BLUE, fill_opacity=0.7
            ).next_to(number_line.n2p(leeftijd), UP, buff=0)
            bars.add(bar)

        # Ensure all points fade out
        self.play(FadeOut(points), run_time=0.5)

        # Transition to histogram bars
        self.play(FadeIn(bars))

        # Add title
        title = Text("Histogram van Leeftijd", font_size=32, color=GOLD_E).to_edge(UP, buff=1)
        self.play(Write(title))
        self.wait(3)

############################################################################################

class DataToHist3(Scene):
    def construct(self):
        # Add a unit grid with main axes crossing at the center of the screen
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            },
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1
            }
        )
        self.add(grid)

        # Load the dataset without the index column
        data = pd.read_csv("geslacht_leeftijd_data.csv", index_col=False)
        if "Unnamed: 0" in data.columns:
            data = data.drop(columns=["Unnamed: 0"])

        # Select only the first 100 rows
        data = data.head(100)

        # Rename column headers and replace gender labels
        data.columns = ["ID", "Geslacht", "Leeftijd"]
        data["Geslacht"] = data["Geslacht"].replace({"Female": "Vrouw", "Male": "Man"})

        # Convert the DataFrame to a list of rows (including header)
        rows = [list(data.columns)] + data.values.tolist()

        # Create a group to hold all table cells
        table = VGroup()

        # Define column-specific spacing
        column_widths = [1, 2, 2]
        y_spacing = 0.75

        # Precompute x_positions for all columns
        x_positions = [
            sum(column_widths[:j]) + column_widths[j] / 2 - sum(column_widths) / 2
            for j in range(len(column_widths))
        ]

        # Generate table cells with borders
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if i == 0:
                    cell_text = Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)
                else:
                    cell_text = Text(str(value), color=GOLD_A).scale(0.5)

                cell_border = Rectangle(width=column_widths[j], height=y_spacing, color=GOLD_A)
                x_position = x_positions[j]
                cell_text.move_to([x_position, -i * y_spacing, 0])
                cell_border.move_to([x_position, -i * y_spacing, 0])

                cell = VGroup(cell_border, cell_text)
                table.add(cell)

        table_top_y = table.get_top()[1]
        target_top_y = config.frame_height / 2
        table.shift(UP * (target_top_y - table_top_y))
        self.play(Create(table), run_time=5)
        self.wait()

        table_bottom_y = table.get_bottom()[1]
        screen_bottom_y = -config.frame_height / 2
        self.play(
            table.animate.shift(DOWN * (table_bottom_y - screen_bottom_y) + UP * y_spacing * 4 / 3),
            run_time=6,
            rate_func=smooth
        )
        self.wait()

        top_rows = data.head(7)
        bottom_rows = data.tail(3)
        combined_data = pd.concat([top_rows, bottom_rows], axis=0)
        reduced_rows = [list(combined_data.columns)] + combined_data.values.tolist()

        reduced_table = VGroup()

        for i, row in enumerate(reduced_rows):
            for j, value in enumerate(row):
                if 7 <= i < len(reduced_rows) - 3:
                    if j == 1:
                        dots = VGroup(
                            Text("...").move_to([x_positions[0], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[1], -i * y_spacing, 0]),
                            Text("...").move_to([x_positions[2], -i * y_spacing, 0])
                        )
                        reduced_table.add(dots)
                    continue

                if i == 0:
                    cell_text = Text(str(value), weight="BOLD", color=GOLD_E).scale(0.6)
                else:
                    cell_text = Text(str(value), color=GOLD_A).scale(0.5)

                cell_border = Rectangle(width=column_widths[j], height=y_spacing, color=GOLD_A)
                x_position = x_positions[j]
                cell_text.move_to([x_position, -i * y_spacing, 0])
                cell_border.move_to([x_position, -i * y_spacing, 0])

                cell = VGroup(cell_border, cell_text)
                reduced_table.add(cell)

        reduced_table.scale(0.7)
        reduced_table.to_edge(LEFT)
        reduced_table_top_y = reduced_table.get_top()[1]
        final_top_y = 3
        reduced_table.shift(UP * (final_top_y - reduced_table_top_y))

        self.play(FadeOut(table), FadeIn(reduced_table), run_time=3)
        self.wait()

        leeftijden = data["Leeftijd"].tolist()
        min_leeftijd = min(leeftijden)
        max_leeftijd = max(leeftijden)
        modus = max(set(leeftijden), key=leeftijden.count)
        max_freq = leeftijden.count(modus)

        # Define the start and end points for the axes
        horizontal_start = [-1, -3, 0]
        horizontal_end = [5, -3, 0]
        vertical_start = [-1, -3, 0]
        vertical_end = [-1, 3, 0]  # Predefined end point for the vertical axis

        # Calculate the total vertical height based on the predefined vertical axis length
        total_vertical_height = vertical_end[1] - vertical_start[1]

        # Calculate the number of ticks and the spacing between them
        num_ticks = max_freq + 2
        vertical_step = total_vertical_height / num_ticks

        # Create horizontal number line based on the range of leeftijden
        number_line = NumberLine(
            # x_range is the range of the number line   
            x_range=[min_leeftijd - 1, max_leeftijd + 1, 1],
            length=horizontal_end[0] - horizontal_start[0],
            include_numbers=True,
            color=GOLD_E
        ).move_to(horizontal_start)

        # Create vertical axis
        vertical_line = Line(
            start=vertical_start,
            end=vertical_end,
            color=GOLD_E
        )

        # Add vertical ticks and labels
        vertical_ticks = VGroup()
        # Add vertical ticks and labels
        for i in range(num_ticks + 1):
            # Create a tick mark
            tick = Line(start=LEFT * 0.1, end=RIGHT * 0.1, color=GOLD_E).move_to(
                vertical_start + UP * i * vertical_step
            )
            label = Text(str(i), font_size=20, color=GOLD_E).next_to(tick, LEFT, buff=0.2)
            vertical_ticks.add(tick, label)

        vertical_label = Text("Frequentie", font_size=24, color=GOLD_E).rotate(PI / 2).next_to(vertical_line, LEFT, buff=0.5)
        horizontal_label = Text("Leeftijd in jaren", font_size=24, color=GOLD_E).next_to(number_line, DOWN)

        self.play(Create(number_line), Create(vertical_line), Create(vertical_ticks), Write(vertical_label), Write(horizontal_label))

        points = VGroup()
        frequencies = {}

        for i, row in enumerate(rows[1:7]):
            leeftijd = row[2]
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(reduced_table[(i + 1) * 3 + 2].get_center())
            self.play(Create(highlight_cell), run_time=0.5)

            value_text = Text(str(leeftijd), color=WHITE).move_to(reduced_table[(i + 1) * 3 + 2].get_center())
            self.play(FadeIn(value_text), run_time=0.5)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            point = Dot(color=BLUE).move_to(target_position)
            self.play(
                value_text.animate.move_to(target_position),
                Transform(value_text, point),
                run_time=0.7
            )
            frequencies[leeftijd] += 1
            points.add(point)

            self.play(FadeOut(highlight_cell), run_time=0.2)

        for leeftijd in leeftijden[7:-3]:
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            start_position = reduced_table[7 * 3].get_center() + RIGHT * 1
            point = Dot(color=BLUE).move_to(start_position)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            self.play(point.animate.move_to(target_position), run_time=0.05)
            frequencies[leeftijd] += 1
            points.add(point)

        for i, row in enumerate(reduced_rows[-3:]):
            leeftijd = row[2]
            if leeftijd not in frequencies:
                frequencies[leeftijd] = 0

            highlight_cell = Rectangle(
                width=column_widths[2], height=y_spacing, color=RED
            ).move_to(reduced_table[(8 * 3 + i * 3)].get_center())
            self.play(Create(highlight_cell), run_time=0.5)

            value_text = Text(str(leeftijd), color=WHITE).move_to(reduced_table[(8 * 3 + i * 3)].get_center())
            self.play(FadeIn(value_text), run_time=0.5)
            target_position = number_line.n2p(leeftijd) + UP * frequencies[leeftijd] * vertical_step
            point = Dot(color=BLUE).move_to(target_position)
            self.play(
                value_text.animate.move_to(target_position),
                Transform(value_text, point),
                run_time=0.7
            )
            frequencies[leeftijd] += 1
            points.add(point)

            self.play(FadeOut(highlight_cell), run_time=0.2)

        self.wait(2)
        bars = VGroup()

        for leeftijd, freq in frequencies.items():
            bar = Rectangle(
                width=0.4, height=freq * vertical_step, color=BLUE, fill_opacity=0.7
            ).next_to(number_line.n2p(leeftijd), UP, buff=0)
            bars.add(bar)

        self.play(FadeOut(points), run_time=0.5)
        self.play(FadeIn(bars))

        title = Text("Histogram van Leeftijd", font_size=32, color=GOLD_E).to_edge(UP, buff=1)
        self.play(Write(title))
        self.wait(3)

############################################################################################

############################################################################################


############################################################################################


# To run: manim -pql DataTableToHist2.py DataTableToHist2
# pwd = Print working directory path
# # ls = show sub directories
# cd 'directory' = changes the directory
# Location:
# /Users/benjamintelkamp/Desktop/ManimProjects/Tables
# run: 
# manim -qm DataTableToHist2.py DataToHist1

# voor geschiedenis:
# history | grep activate
# Zoeken:
# find . -type d -name "venv"
# activerev venv
# source venv/bin/activate
# of 
# source /Users/benjamintelkamp/Desktop/ManimProjects/Tables/venv/bin/activate

