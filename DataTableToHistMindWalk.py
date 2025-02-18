import pandas as pd
from manim import (
    Scene,
    NumberPlane,
    config,
    UP,
    Create,
    FadeIn,
    VGroup,
    Text,
    Rectangle,
    DOWN,
    smooth,
    GOLD_A,
    LEFT,
    RIGHT,
    FadeOut,
    Transform,
    Axes,
    Write,
    DEGREES,
    PI,
    Dot,
    VMobject,
    ParametricFunction,
    MoveAlongPath,
    Circle,
    RED,
    MathTex,
    DashedLine,
    Arrow,
)


class DataToHistMindWalk(Scene):
    def construct(self):
        # --- 1. Create a standard grid as background ---
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": "#777777",
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "stroke_color": "#777777",
                "stroke_width": 1,
            },
        )
        self.add(grid)

        # --- 2. Import the new dataset ---
        data = pd.read_csv("Data/kvl_skew_data.csv", index_col=False)
        if "Unnamed: 0" in data.columns:
            data = data.drop(columns=["Unnamed: 0"])

        print("Total observations in data:", len(data))
        print(data.head(3))
        print("Column names in dataset:", data.columns)

        # --- 3. Rename columns and update labels ---
        # We work with the original three columns first.
        data.columns = ["ID", "Conditie", "KvL Score"]
        data["Conditie"] = data["Conditie"].replace(
            {"Mindfullness": "Mindfulness", "Short Walk": "Wandeling"}
        )
        print("Updated dataset structure:")
        print(data.head(3))

        # Check descriptive statistics
        min_qol = data["KvL Score"].min()
        max_qol = data["KvL Score"].max()
        print(f"Kwaliteit v. Leven min: {min_qol}, max: {max_qol}")

        # --- 4. Calculate Class Bins (for the new column, not shown yet) ---
        bin_edges = list(range(0, 105, 5))
        bin_labels = [
            f"{bin_edges[i]}-{bin_edges[i + 1]}" for i in range(len(bin_edges) - 1)
        ]
        data["KvL Klasse"] = pd.cut(
            data["KvL Score"], bins=bin_edges, labels=bin_labels, right=True
        )
        print(data[["KvL Score", "KvL Klasse"]].head(10))
        self.wait(2)

        # --- 5. Build the Full Table (3 columns only) ---
        # We still build the full table with only the first three columns.
        rows = [list(data.columns[:-1])] + data.head(100).iloc[:, :-1].values.tolist()
        table = VGroup()
        column_widths_full = [1, 2, 2]  # for columns: ID, Conditie, Kwaliteit v. Leven
        y_spacing = 0.75
        x_positions = [
            sum(column_widths_full[:j])
            + column_widths_full[j] / 2
            - sum(column_widths_full) / 2
            for j in range(len(column_widths_full))
        ]

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if i == 0:
                    text_color = "#FFD700"  # header: gold
                else:
                    condition = row[1]
                    if condition == "Mindfulness":
                        text_color = "#C76E6E"
                    elif condition == "Wandeling":
                        text_color = "#688E26"
                    else:
                        text_color = "#C0A080"
                cell_text = Text(str(value), color=text_color).scale(0.5)
                cell_border = Rectangle(
                    width=column_widths_full[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                x_pos = x_positions[j]
                cell_text.move_to([x_pos, -i * y_spacing, 0])
                cell_border.move_to([x_pos, -i * y_spacing, 0])
                cell = VGroup(cell_border, cell_text)
                table.add(cell)

        # Position and animate the full table.
        table_top_y = table.get_top()[1]
        target_top_y = config.frame_height / 2
        table.shift(UP * (target_top_y - table_top_y - 0.5))
        self.play(Create(table), run_time=5)
        self.wait()

        table_bottom_y = table.get_bottom()[1]
        screen_bottom_y = -config.frame_height / 2
        self.play(
            table.animate.shift(
                DOWN * (table_bottom_y - screen_bottom_y) + UP * y_spacing * 4 / 3
            ),
            run_time=12,
            rate_func=smooth,
        )
        # wait for a while to let the user see the table.
        self.wait(5)

        # --- 6. Create the Reduced Table (with 4 columns) ---
        # Build reduced data: top 5 rows, a dummy row, and bottom 4 rows.
        # For the dummy row, use four "..." entries.
        dummy_row = pd.DataFrame([["..."] * len(data.columns)], columns=data.columns)
        top_rows = data.head(5)  # all 4 columns
        bottom_rows = data.tail(4)  # all 4 columns
        reduced_data = pd.concat([top_rows, dummy_row, bottom_rows], ignore_index=True)
        reduced_rows = [list(reduced_data.columns)] + reduced_data.values.tolist()
        # Now, reduced_rows is a list of lists where each row has 4 items:
        # ["ID", "Conditie", "Kwaliteit v. Leven", "KvL Klasse"] in the header, and data rows follow.

        # Define column widths for 4 columns.
        column_widths_reduced = [1, 2, 2, 2]
        reduced_x_positions = [
            sum(column_widths_reduced[:j])
            + column_widths_reduced[j] / 2
            - sum(column_widths_reduced) / 2
            for j in range(len(column_widths_reduced))
        ]

        reduced_table = VGroup()
        # Build the table row by row.
        # For the fourth column (index 3) in non-header rows, we initially show an empty string.
        for i, row in enumerate(reduced_rows):
            for j, value in enumerate(row):
                if i == 0:
                    # Header row: always display as is with scale 0.5.
                    text_color = "#FFD700"
                    display_value = str(value)
                    cell_text = Text(display_value, color=text_color).scale(0.5)
                else:
                    # Non-header rows:
                    if j == 3:
                        # For the KvL Klasse column, start with a blank value.
                        display_value = ""
                    else:
                        display_value = str(value)
                    # Set the text color based on the "Conditie" value.
                    condition = row[1]
                    if condition == "Mindfulness":
                        text_color = "#C76E6E"
                    elif condition == "Wandeling":
                        text_color = "#688E26"
                    else:
                        text_color = "#C0A080"
                    # Use a smaller scale for the KvL Klasse cells in non-header rows.
                    if j == 3:
                        cell_text = Text(display_value, color=text_color).scale(0.4)
                    else:
                        cell_text = Text(display_value, color=text_color).scale(0.5)

                cell_border = Rectangle(
                    width=column_widths_reduced[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                x_pos = reduced_x_positions[j]
                cell_text.move_to([x_pos, -i * y_spacing, 0])
                cell_border.move_to([x_pos, -i * y_spacing, 0])
                cell = VGroup(cell_border, cell_text)
                reduced_table.add(cell)
        # Scale the table down and position it to the left.
        reduced_table.scale(0.7)
        # Move the reduced table to the left edge of the screen
        reduced_table.to_edge(LEFT)
        # Calculate the desired top position (0.5 below the top of the screen)
        target_top_y = config.frame_height / 2 - 0.5
        # Get the current top y-value of the reduced table
        current_top_y = reduced_table.get_top()[1]
        # Shift the table vertically so that its top is at the target position
        reduced_table.shift(UP * (target_top_y - current_top_y))

        self.play(FadeOut(table), FadeIn(reduced_table), run_time=3)
        self.wait()

        # --- 7. Animate the Appearance of the Fourth Column ---
        # For each non-header row in the reduced table, animate the fourth column cell's text
        # from blank to its actual value.
        num_rows = len(reduced_rows)  # header + 5 top + 1 dummy + 4 bottom = 11 rows

        # Loop over rows (skipping header at index 0)
        for i in range(1, num_rows):
            # The cell for the fourth column in row i is at index: i * 4 + 3
            cell = reduced_table[i * 4 + 3]
            actual_value = str(reduced_rows[i][3])
            # Recalculate the text color based on the condition in column 1:
            cond = reduced_rows[i][1]
            if cond == "Mindfulness":
                text_color = "#C76E6E"
            elif cond == "Wandeling":
                text_color = "#688E26"
            else:
                text_color = "#C0A080"
            # Now, regardless of the condition, create the new label with the desired smaller scale (0.4)
            new_label = (
                Text(actual_value, color=text_color)
                .scale(0.4)  # using 0.4 to keep the smaller font size
                .move_to(cell.get_center())
            )
            self.play(Transform(cell[1], new_label), run_time=0.5)
            self.wait(max(0.1, 0.5 - 0.03 * i))
        self.wait(2)

        # --- 8. Replace the Reduced Table with a New 3-Column Table ---
        self.wait(3)  # Pause so viewers can study the current 4-column table.

        # Build new table data by selecting only columns 0, 1, and 3 (i.e. ID, Conditie, KvL Klasse)
        new_reduced_rows = []
        for row in reduced_rows:
            # row[0] is "ID", row[1] is "Conditie", row[3] is "KvL Klasse"
            new_reduced_rows.append([row[0], row[1], row[3]])

        # Define new column widths for 3 columns. Adjust these values as desired.
        new_column_widths = [1, 2, 2]
        y_spacing = 0.75  # (Use the same y_spacing as before)
        new_x_positions = [
            sum(new_column_widths[:j])
            + new_column_widths[j] / 2
            - sum(new_column_widths) / 2
            for j in range(len(new_column_widths))
        ]

        new_reduced_table = VGroup()
        # Build the new table row by row.
        for i, row in enumerate(new_reduced_rows):
            for j, cell_val in enumerate(row):
                if i == 0:
                    # Header row: use header color and scale 0.5.
                    text_color = "#FFD700"
                    cell_text = Text(str(cell_val), color=text_color).scale(0.5)
                else:
                    # Data rows: determine text color based on the "Conditie" (which is now row[1]).
                    condition = row[1]
                    if condition == "Mindfulness":
                        text_color = "#C76E6E"
                    elif condition == "Wandeling":
                        text_color = "#688E26"
                    else:
                        text_color = "#C0A080"
                    # For the KvL Klasse column (which is now the third cell, j == 2) use a smaller scale.
                    if j == 2:
                        cell_text = Text(str(cell_val), color=text_color).scale(0.4)
                    else:
                        cell_text = Text(str(cell_val), color=text_color).scale(0.5)
                cell_border = Rectangle(
                    width=new_column_widths[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                new_x = new_x_positions[j]
                cell_text.move_to([new_x, -i * y_spacing, 0])
                cell_border.move_to([new_x, -i * y_spacing, 0])
                cell = VGroup(cell_border, cell_text)
                new_reduced_table.add(cell)

        # Scale the new table down and position it at the left edge.
        new_reduced_table.scale(0.7)
        new_reduced_table.to_edge(LEFT)
        # Adjust its vertical position so the top is 0.5 below the top of the screen.
        target_top_y = config.frame_height / 2 - 0.5
        current_top_y = new_reduced_table.get_top()[1]
        new_reduced_table.shift(UP * (target_top_y - current_top_y))

        # Replace the old reduced table with the new one.
        self.play(Transform(reduced_table, new_reduced_table), run_time=1)
        self.wait(2)

        # --- 9. Adjust Table Frame Appearance ---
        # Lower the stroke opacity for the interior cell borders so that overlapping lines are less bright.
        reduced_table.set_stroke(opacity=0.2)

        # Now, draw an outer frame (a single rectangle) around the entire table.
        outer_frame = Rectangle(
            width=reduced_table.get_width(),
            height=reduced_table.get_height(),
            color=GOLD_A,
            stroke_width=2,  # a thicker line for the outer border
            fill_opacity=0,  # no fill
        )
        outer_frame.move_to(reduced_table.get_center())
        self.play(FadeIn(outer_frame), run_time=1)
        self.wait(2)

        # --- 10. Set Up Histogram Axes for Wandeling and Mindfulness with Custom Tick Labels ---

        # We want the physical x-axis to span from 0 to 100.
        x_range = [0, 100, 5]
        # The y-axis will cover frequency from 0 to 20.
        y_range = [0, 11, 2]

        # Define custom tick positions for the x-axis:
        # For 5-unit class intervals, the midpoints are 2.5, 7.5, 12.5, ..., 97.5.
        custom_tick_positions = [2.5 + 5 * i for i in range(20)]
        # Define custom labels corresponding to these midpoints:
        # The first label should be "0-5", then "5-10", "10-15", ..., "95-100".
        custom_tick_labels = [f"{5 * i}-{5 * (i + 1)}" for i in range(20)]

        # ========= Create Top Axes (for Wandeling) =========
        axes_top = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=8,  # Set the horizontal length (in scene units)
            y_length=2.5,  # A shorter vertical extent
            axis_config={
                "color": GOLD_A,
                "include_numbers": False,  # We will add custom numbers manually.
            },
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": custom_tick_positions,  # Place ticks at midpoints.
                "include_tip": False,
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(0, 11, 2),
                "numbers_to_exclude": [],  # Exclude no numbers
                "include_tip": False,
            },
        )
        # Position the top axes:
        axes_top.to_edge(
            # Align the right edge to the right of the screen with a 0.8-unit margin.
            RIGHT,
            buff=0.8,
        )
        axes_top.shift(UP * 2.3)  # Shift the top axes upward.

        # Replace the automatically generated x-axis tick labels with our custom labels.
        for i, tick in enumerate(axes_top.x_axis.numbers):
            # Create a new Text object with our custom label.
            new_label = Text(custom_tick_labels[i], font_size=15, color=GOLD_A)
            new_label.rotate(45 * DEGREES)  # Rotate by 45 degrees.
            new_label.move_to(
                tick.get_center()
            )  # Position it exactly where the original tick label was.
            tick.become(new_label)  # Replace the tick label.
        # Set the y-axis tick labels to a smaller font.
        for tick in axes_top.y_axis.numbers:
            tick.set(font_size=18)

        # Adjust the tick marks (the little lines) to be thinner.
        # (Use get_tick_marks() instead of tick_lines, which is deprecated.)
        for tick in axes_top.x_axis.get_tick_marks():
            tick.set_stroke(width=1, opacity=0.5)
        for tick in axes_top.y_axis.get_tick_marks():
            tick.set_stroke(width=1, opacity=0.5)

        # Add a vertical axis title for the top axes ("Frequentie"):
        vertical_label_top = Text("Frequentie", font_size=15, color=GOLD_A).rotate(
            PI / 2
        )
        # Position it to the left of the y-axis.
        vertical_label_top.next_to(axes_top.y_axis, LEFT, buff=0.0)
        # Add a horizontal title for the top axes.
        title_top = Text(
            "KvL Scores voor Conditie 'Wandeling'", font_size=20, color=GOLD_A
        )
        # Position it above the top axes.
        title_top.next_to(axes_top, UP, buff=0.0)

        # ========= Create Bottom Axes (for Mindfulness) =========
        axes_bottom = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=8,
            y_length=2.5,  # same vertical length as top
            axis_config={
                "color": GOLD_A,
                "include_numbers": False,
            },
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": custom_tick_positions,
                "include_tip": False,
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(0, 11, 2),
                "numbers_to_exclude": [],  # Exclude no numbers
                "include_tip": False,
            },
        )
        # Initially position the bottom axes below the top axes with a small gap.
        axes_bottom.next_to(axes_top, DOWN, buff=0.5)
        # *** Force the bottom axes to align horizontally with the top axes ***
        axes_bottom.align_to(axes_top, RIGHT)

        # Replace the x-axis tick labels for the bottom axes similarly.
        for i, tick in enumerate(axes_bottom.x_axis.numbers):
            new_label = Text(custom_tick_labels[i], font_size=15, color=GOLD_A)
            new_label.rotate(45 * DEGREES)
            new_label.move_to(tick.get_center())
            tick.become(new_label)
        for tick in axes_bottom.y_axis.numbers:
            tick.set(font_size=15)
        # Adjust the tick marks for the bottom axes.
        for tick in axes_bottom.x_axis.get_tick_marks():
            tick.set_stroke(width=1, opacity=0.5)
        for tick in axes_bottom.y_axis.get_tick_marks():
            tick.set_stroke(width=1, opacity=0.5)

        vertical_label_bottom = Text("Frequentie", font_size=15, color=GOLD_A).rotate(
            PI / 2
        )
        vertical_label_bottom.next_to(axes_bottom.y_axis, LEFT, buff=0.0)

        title_bottom = Text(
            "KvL Scores voor Conditie 'Mindfulness'", font_size=20, color=GOLD_A
        )
        # Position it above the bottom axes.
        title_bottom.next_to(axes_bottom, UP, buff=-0.25)

        # Animate the axes and titles.
        self.play(
            Create(axes_top), Write(title_top), Write(vertical_label_top), run_time=4
        )
        self.wait(1)
        self.play(
            Create(axes_bottom),
            Write(title_bottom),
            Write(vertical_label_bottom),
            run_time=4,
        )
        self.wait(2)

        # After your Step 10 but before your Step 11:

        # 1) Build a dictionary mapping each KvL Klasse label to its numerical midpoint.
        #    For example, "0-5" -> 2.5, "5-10" -> 7.5, etc.
        klasse_midpoints = {f"{5 * i}-{5 * (i + 1)}": 2.5 + 5 * i for i in range(20)}

        # Then you can proceed with Step 11, referencing klasse_midpoints

        # --- 11. Animate the Transfer of KvL Klasse Data from Table Cells to Histogram Dots ---

        # We'll define a helper function that creates a parabolic (quadratic) path
        # from p0 to p1, arching upward by 'height' scene units.

        def parabola_path(p0, p1, height=1.5):
            return ParametricFunction(
                lambda t: (1 - t) ** 2 * p0
                + 2 * (1 - t) * t * ((p0 + p1) / 2 + UP * height)
                + t**2 * p1,
                t_range=[0, 1],
                fill_opacity=0,
            ).set_stroke(width=2)

        # 1) We'll define exactly one vertical_step by measuring the top axes from freq=0..1.
        #    Because you said top/bottom have the same scale/length, we can share this step.
        y0_top = axes_top.y_axis.n2p(0)
        y1_top = axes_top.y_axis.n2p(1)
        vertical_step = (y1_top - y0_top)[
            1
        ]  # the difference in y-coordinates => 1 freq

        # 2) We'll keep a frequency dictionary keyed by (klasse_label, condition).
        #    That way, each condition's category increments on its own, without interfering.
        frequencies = {}

        # 3) For smaller dots, we specify a radius=0.05, say.
        dot_radius = 0.05

        # 4) We'll define row ranges: top rows = i in [1..5], dummy = i=6, bottom = i in [7..10].
        #    new_reduced_rows[0] is header.

        # Create a VGroup to hold all dots
        dots = VGroup()
        # Create a dictionary to map each dot to its corresponding cell
        dot_map = {}

        # ========= Animate Top Rows (1..5) =========
        for i in range(1, 6):
            row_data = new_reduced_rows[i]  # e.g. [ID, Conditie, KvL Klasse]
            condition = row_data[1]
            klasse_label = row_data[2]
            if klasse_label in ["", "..."]:
                continue
            # The KvL Klasse cell index = i*3 + 2
            cell_idx = i * 3 + 2
            start_pos = new_reduced_table[cell_idx].get_center()

            # Build the freq key => (label, condition)
            freq_key = (klasse_label, condition)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            # Decide which axes we use
            if condition == "Wandeling":
                target_axes = axes_top
                dot_color = "#688E26"
            else:
                target_axes = axes_bottom
                dot_color = "#C76E6E"

            # Highlight the cell
            highlight = Rectangle(
                width=new_column_widths[2],
                height=y_spacing,
                color=dot_color,
            ).move_to(start_pos)
            self.play(Create(highlight), run_time=0.7)

            # Temporary red text label
            anim_text = (
                Text(str(klasse_label), color=dot_color).scale(0.5).move_to(start_pos)
            )
            self.play(FadeIn(anim_text), run_time=0.7)

            # Decide which axes we use
            if condition == "Wandeling":
                target_axes = axes_top
                dot_color = "#688E26"
            else:
                target_axes = axes_bottom
                dot_color = "#C76E6E"

            # Convert KvL label to midpoint
            midpoint_val = klasse_midpoints.get(klasse_label, None)
            if midpoint_val is None:
                continue

            # x-coord = target_axes.x_axis.n2p(midpoint_val)
            x_axis_pos = target_axes.x_axis.n2p(midpoint_val)

            # Next frequency count
            freq_count = frequencies[freq_key] + 1
            # The target position is x_axis_pos plus freq_count * vertical_step upward
            target_pos = x_axis_pos + UP * (freq_count * vertical_step)

            # Create dot with smaller radius
            dot = Dot(color=dot_color, radius=dot_radius).move_to(start_pos)
            # Add dot to the dot_map
            dot_map.setdefault((klasse_label, condition), []).append(dot)

            # Build a parabolic path
            path = parabola_path(start_pos, target_pos, height=1.5)
            self.play(MoveAlongPath(dot, path), run_time=0.9)

            self.play(FadeOut(anim_text), run_time=0.4)
            frequencies[freq_key] = freq_count
            dots.add(dot)
            self.play(FadeOut(highlight), run_time=0.3)
            self.wait(0.1)

        # ========= Animate Middle Row (Dummy) => i=6 =========
        dummy_idx = 6
        # Suppose the leftover data is from index 5..96 in original dataset => 91 rows
        leftover_data = data.iloc[5:96]
        for idx, row in leftover_data.iterrows():
            klasse_label = str(row["KvL Klasse"])
            condition = row["Conditie"]
            if klasse_label in ["", "..."]:
                continue
            dummy_cell_center = new_reduced_table[dummy_idx * 3 + 2].get_center()
            # Add small horizontal offset
            start_pos = dummy_cell_center

            freq_key = (klasse_label, condition)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            if condition == "Wandeling":
                target_axes = axes_top
                dot_color = "#688E26"
            else:
                target_axes = axes_bottom
                dot_color = "#C76E6E"

            midpoint_val = klasse_midpoints.get(klasse_label, None)
            if midpoint_val is None:
                continue
            x_axis_pos = target_axes.x_axis.n2p(midpoint_val)
            freq_count = frequencies[freq_key] + 1
            target_pos = x_axis_pos + UP * (freq_count * vertical_step)

            dot = Dot(color=dot_color, radius=dot_radius).move_to(start_pos)
            # Add dot to the dot_map
            dot_map.setdefault((klasse_label, condition), []).append(dot)

            # Animate quickly
            self.play(dot.animate.move_to(target_pos), run_time=0.2)
            frequencies[freq_key] = freq_count
            dots.add(dot)

        # ========= Animate Bottom Rows (7..10) =========
        for i in range(7, 11):
            row_data = new_reduced_rows[i]
            klasse_label = row_data[2]
            condition = row_data[1]
            if klasse_label in ["", "..."]:
                continue

            cell_idx = i * 3 + 2
            start_pos = new_reduced_table[cell_idx].get_center()

            freq_key = (klasse_label, condition)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            if condition == "Wandeling":
                target_axes = axes_top
                dot_color = "#688E26"
            else:
                target_axes = axes_bottom
                dot_color = "#C76E6E"

            highlight = Rectangle(
                width=new_column_widths[2], height=y_spacing, color=dot_color
            ).move_to(start_pos)
            self.play(Create(highlight), run_time=0.5)
            anim_text = (
                Text(klasse_label, color=dot_color).scale(0.5).move_to(start_pos)
            )
            self.play(FadeIn(anim_text), run_time=0.5)

            if condition == "Wandeling":
                target_axes = axes_top
                dot_color = "#688E26"
            else:
                target_axes = axes_bottom
                dot_color = "#C76E6E"

            midpoint_val = klasse_midpoints.get(klasse_label, None)
            if midpoint_val is None:
                continue
            freq_count = frequencies[freq_key] + 1
            x_axis_pos = target_axes.x_axis.n2p(midpoint_val)
            target_pos = x_axis_pos + UP * (freq_count * vertical_step)

            dot = Dot(color=dot_color, radius=dot_radius).move_to(start_pos)
            # Add dot to the dot_map
            dot_map.setdefault((klasse_label, condition), []).append(dot)
            path = parabola_path(start_pos, target_pos, height=0.5)
            self.play(MoveAlongPath(dot, path), run_time=0.7)

            self.play(FadeOut(anim_text), run_time=0.3)
            frequencies[freq_key] = freq_count
            dots.add(dot)
            self.play(FadeOut(highlight), run_time=0.2)
            self.wait(0.1)

        self.wait(2)

        # --- 12. Transition from Stacked Dots to Histogram Bars ---
        # We'll build one bar per (klasse_label, condition).

        # 1) Collect the dots by (klasse_label, condition).
        #    We assume we created them in Step 11. For that, we can keep a dictionary:
        #      dot_map[(klasse_label, condition)] = list of Dot objects
        #    If not, we can still find them by referencing the frequencies or by storing them as we created them.

        # If you DID NOT store them as you created them, we can do something like this:
        #    We'll search the master 'dots' group and see which label each belongs to.
        # But that means each dot must have a 'label_key' attribute or something.
        # Easiest is to store them as we go. Example:
        #   dot_map.setdefault(freq_key, []).append(dot)
        #  We'll assume we already did that in Step 11. If not, here's how you'd do it in step 11 for each dot:
        #
        #     dot_map.setdefault((klasse_label, condition), []).append(dot)
        #
        # We'll assume dot_map is now defined and each key is (klasse_label, condition), and each value is a list of Dot objects.

        # 2) For each (klasse_label, condition), create a bar at the correct x, with height = frequency * vertical_step, same color as dots.

        # We also need to decide which axis is used (top or bottom).
        # We'll keep them in a VGroup bars so we can animate them all in at once if we like.
        bars = VGroup()

        # We'll assume you have two vertical_step variables, one for top, one for bottom, or just one if you’re sure
        # the axes are the same scale. Let’s assume one step => 'vertical_step'.
        # Also we’ll assume 'klasse_midpoints' is defined.

        # A dictionary to map condition => color used for the bar, same as the dot color.
        color_map = {
            "Wandeling": "#688E26",  # greenish
            "Mindfulness": "#C76E6E",  # pinkish
        }

        # For each entry in frequencies => (klasse_label, condition) => freq_count
        # we build a bar at the correct x midpoint, from y=0..freq_count, in the correct axis.
        # Then we do a Transform from the dot group to the bar.

        # We’ll store all transforms in a list so we can do them in parallel or sequence.
        transforms = []

        for (klasse_label, condition), freq_count in frequencies.items():
            if freq_count <= 0:
                continue
            # Find the list of dots for this key => dot_map[(klasse_label, condition)]
            if (klasse_label, condition) not in dot_map:
                continue
            dot_list = dot_map[(klasse_label, condition)]
            dot_group = VGroup(*dot_list)

            # Decide top or bottom axes
            if condition == "Wandeling":
                target_axes = axes_top
                bar_color = color_map["Wandeling"]
            else:
                target_axes = axes_bottom
                bar_color = color_map["Mindfulness"]

            # Convert label to midpoint
            midpoint_val = klasse_midpoints.get(klasse_label, None)
            if midpoint_val is None:
                continue
            x_axis_pos = target_axes.x_axis.n2p(midpoint_val)
            # The bar's height in scene units = freq_count * vertical_step
            bar_height = freq_count * vertical_step

            # We can choose some bar width in scene coords. For instance, 0.6 scene units.
            # We'll center the bar at 'x_axis_pos' horizontally, and anchor it to the x-axis at the bottom.
            bar_width = 5 * (axes_top.x_length / (x_range[1] - x_range[0]))
            # axes_top.x_length is 8 scene units.
            # which simplifies to 5 * (8 / 100) = 0.4

            # The bottom of the bar is at x_axis_pos, i.e. x_axis_pos.x, y = 0 in that axis’s scene coords.
            # But we can just do something like:
            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                color=bar_color,
                fill_color=bar_color,
                fill_opacity=0.8,
            )
            # We'll place the bar so that its bottom is on the axis.
            # x_axis_pos is the coordinate of freq=0 in the scene for that bin.
            # We want the bar's bottom to be at x_axis_pos. Then we shift upward by bar_height/2
            # to center the bar shape. Actually, we want the bottom edge to be at freq=0, so we can do:
            bar.move_to(x_axis_pos, aligned_edge=DOWN)
            # Now the bar is anchored with its bottom at freq=0. Next we need to shift it up by bar_height/2,
            # or we can do 'aligned_edge=DOWN' so the bar's bottom edge is exactly at that position.
            # Then we shift it left or right so that the bar is horizontally centered at x_axis_pos.x
            # bar.shift(RIGHT * (bar_width / 2))

            # Now we define a transform from dot_group => bar
            # Usually you'd do something like:
            transforms.append(Transform(dot_group, bar))

            # Add the bar to the 'bars' group so we can show or keep it at the end
            bars.add(bar)

        # 3) We run all transforms in one animation or sequentially.
        # E.g.:
        self.play(*transforms, run_time=2)

        # If you want to fade the bars in, you might do a FadeIn(bars) afterwards or set them in
        # the scene first with zero opacity, etc.

        # You can show them fully at the end:
        self.play(FadeIn(bars))
        self.wait(2)

        # --- 13. Display Basic Stats (M, MED, SD) for Each Condition ---
        # plus labeled vertical lines (arrows) for mean (solid) and median (dashed).

        # 1) Compute the sample means, medians, and std devs from the dataset.
        means = data.groupby("Conditie")["KvL Score"].mean()
        medians = data.groupby("Conditie")["KvL Score"].median()
        stds = data.groupby("Conditie")["KvL Score"].std()
        skews = data.groupby("Conditie")["KvL Score"].skew()
        print(means)
        print(medians)
        print(stds)
        print(skews)

        # 2) Build a function that returns a VGroup of four lines:
        #    M = ...
        #    MED = ...
        #    SD = ...
        #    Skewness = ...
        # all stacked vertically with buff=0.5.
        def stats_block(cond_name, color):
            mean_val = means[cond_name]
            med_val = medians[cond_name]
            sd_val = stds[cond_name]
            sk_val = skews[cond_name]

            # Use italic M, MED, SD in the labels:
            line1 = MathTex(
                rf"\mathit{{M}} = {mean_val:.2f}", color=color, font_size=20
            )
            line2 = MathTex(
                rf"\mathit{{MED}} = {med_val:.2f}", color=color, font_size=20
            )
            line3 = MathTex(rf"\mathit{{SD}} = {sd_val:.2f}", color=color, font_size=20)

            line4 = MathTex(rf"\mathit{{SK}} = {sk_val:.2f}", color=color, font_size=20)

            group = VGroup(line1, line2, line3, line4).arrange(
                DOWN, buff=0.2, aligned_edge=LEFT
            )
            return group

        # 3) Build one stats block for "Wandeling" (top axes) and one for "Mindfulness" (bottom axes).
        stats_wandeling = stats_block("Wandeling", color_map["Wandeling"])
        stats_mindful = stats_block("Mindfulness", color_map["Mindfulness"])

        # 4) Position them near each histogram’s y-axis.
        stats_wandeling.next_to(axes_top.y_axis, RIGHT, buff=0.5)
        stats_mindful.next_to(axes_bottom.y_axis, RIGHT, buff=0.5)

        # Optionally shift them up or down a bit:
        stats_wandeling.shift(UP * 0.1)
        stats_mindful.shift(UP * 0.1)

        # 5) Animate them onto the screen.
        self.play(FadeIn(stats_wandeling), FadeIn(stats_mindful))
        self.wait(1)

        # 6) Create small helpers for the mean/median indicators (arrows/lines).
        #    We'll let "is_median" = True => dashed line + label on the down-right,
        #    otherwise a solid arrow + label on the down-left.
        def add_stat_indicator(ax, x_value, color, label_tex, is_median=False):
            """Place an indicator for either the mean or the median on the x-axis.

            - If is_median=True, uses a dashed line + label on the down-right.
            - Otherwise uses a solid arrow + label on the down-left.
            """
            axis_coord = ax.x_axis.n2p(x_value)
            arrow_start = axis_coord + DOWN * 0.7

            if is_median:
                # Dashed line from below the axis up to freq=0
                line = DashedLine(
                    start=arrow_start,
                    end=axis_coord,
                    dash_length=0.06,
                    color=color,
                    stroke_width=3,
                )
                label = MathTex(label_tex, color=color, font_size=20)
                # Put the label slightly down-right:
                label.next_to(line, DOWN * 0.1 + RIGHT, buff=0.10)
                group = VGroup(line, label)
            else:
                # Solid arrow from below axis
                arrow = Arrow(
                    start=arrow_start,
                    end=axis_coord,
                    buff=0,
                    stroke_width=3,
                    color=color,
                )
                label = MathTex(label_tex, color=color, font_size=20)
                # Put the label slightly down-left:
                label.next_to(arrow, DOWN * 0.1 + LEFT, buff=0.10)
                group = VGroup(arrow, label)

            return group

        # 7) Mark mean and median for each group:
        # -- top axes (Wandeling) --
        mean_w = means["Wandeling"]
        med_w = medians["Wandeling"]
        mean_indicator_w = add_stat_indicator(
            axes_top, mean_w, color_map["Wandeling"], r"\mathit{M}", is_median=False
        )
        median_indicator_w = add_stat_indicator(
            axes_top, med_w, color_map["Wandeling"], r"\mathit{MED}", is_median=True
        )

        # -- bottom axes (Mindfulness) --
        mean_m = means["Mindfulness"]
        med_m = medians["Mindfulness"]
        mean_indicator_m = add_stat_indicator(
            axes_bottom,
            mean_m,
            color_map["Mindfulness"],
            r"\mathit{M}",
            is_median=False,
        )
        median_indicator_m = add_stat_indicator(
            axes_bottom,
            med_m,
            color_map["Mindfulness"],
            r"\mathit{MED}",
            is_median=True,
        )

        # 8) Animate them in.
        self.play(
            FadeIn(mean_indicator_w),
            FadeIn(median_indicator_w),
            FadeIn(mean_indicator_m),
            FadeIn(median_indicator_m),
            run_time=2,
        )
        self.wait(3)


# Specifics: No differences with version DataTableToHistMindWalk00.py
# Specifications for the video:
# Two groups: Wandeling and Mindfulness
# Two histograms: Wandeling and Mindfulness
# Mindfulness is more skewed to the left.
# No running mean or median.
# Things to still change:


# source .venv/bin/activate
# manim -qm --disable_caching DataTableToHistMindWalk2.py DataToHistMW2 | tee outputMW2.txt
# manim -qk -p --disable_caching DataTableToHistMindWalk.py DataToHistMW
