import pandas as pd
from manim import (
    Scene,
    NumberPlane,
    config,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    PI,
    DEGREES,
    smooth,
    Create,
    FadeIn,
    FadeOut,
    Transform,
    Write,
    MoveAlongPath,
    VGroup,
    Text,
    Rectangle,
    Dot,
    MathTex,
    DashedLine,
    Arrow,
    Axes,
    ParametricFunction,
    RED,
    GOLD_A,
)


class DataToHistMW_GPT(Scene):
    def construct(self):
        """
        Demonstration script that:
          1) Displays a 3-col table of data, then shifts it for more rows to show.
          2) Creates a 4-col 'reduced' table (ID, Cond, KvL Score, KvL Klasse).
             Animates the 4th column from blank to actual class labels.
          3) Transforms that 4-col to a new 3-col (ID, Cond, KvL Klasse).
          4) Builds two histogram axes for two conditions (Wandeling & Mindfulness).
          5) Animates data from table cells -> stacked dots in bins.
          6) Transforms stacked dots -> bars.
          7) Displays summary stats (M, MED, SD, SK) + arrows/dashed lines for mean/median.
        """

        # ============= 1) BACKGROUND + COLOR MAP =============
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": "#777777",
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_color": "#777777", "stroke_width": 1},
        )
        self.add(grid)

        # Condition => color
        color_map = {
            "Mindfulness": "#C76E6E",  # pinkish
            "Wandeling": "#688E26",  # greenish
            "Other": "#C0A080",  # fallback
        }

        # ============= 2) LOAD + PREP DATA =============
        data = pd.read_csv("Data/kvl_skew_data.csv", index_col=False)
        if "Unnamed: 0" in data.columns:
            data.drop(columns=["Unnamed: 0"], inplace=True)

        data.columns = ["ID", "Conditie", "KvL Score"]
        data["Conditie"] = data["Conditie"].replace(
            {"Mindfullness": "Mindfulness", "Short Walk": "Wandeling"}
        )

        # create 5‑wide bins => KvL Klasse
        bin_edges = list(range(0, 105, 5))
        bin_labels = [
            f"{bin_edges[i]}-{bin_edges[i + 1]}" for i in range(len(bin_edges) - 1)
        ]
        data["KvL Klasse"] = pd.cut(
            data["KvL Score"], bins=bin_edges, labels=bin_labels, right=True
        )

        # ============= 3) FULL 3‑COLUMN TABLE =============
        col_subset_3 = data.columns[:-1]  # ID, Conditie, KvL Score
        rows_3col = [list(col_subset_3)] + data.head(100)[col_subset_3].values.tolist()

        col_widths_3 = [1, 2, 2]
        y_spacing = 0.75
        x_pos_3 = [
            sum(col_widths_3[:j]) + col_widths_3[j] / 2 - sum(col_widths_3) / 2
            for j in range(len(col_widths_3))
        ]

        table_3col = VGroup()
        for i, row in enumerate(rows_3col):
            for j, val in enumerate(row):
                if i == 0:
                    txt_color = "#FFD700"  # header
                else:
                    cond = row[1]
                    txt_color = color_map.get(cond, color_map["Other"])
                txt = Text(str(val), color=txt_color).scale(0.5)
                rect = Rectangle(
                    width=col_widths_3[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                xcoord = x_pos_3[j]
                txt.move_to([xcoord, -i * y_spacing, 0])
                rect.move_to([xcoord, -i * y_spacing, 0])
                table_3col.add(VGroup(rect, txt))

        # shift table near top
        t3_top_y = table_3col.get_top()[1]
        desired_top = config.frame_height / 2 - 0.5
        table_3col.shift(UP * (desired_top - t3_top_y))

        self.play(Create(table_3col), run_time=5)
        self.wait()

        # shift downward so more rows are visible
        bottom_3col = table_3col.get_bottom()[1]
        screen_bot = -config.frame_height / 2
        self.play(
            table_3col.animate.shift(
                DOWN * (bottom_3col - screen_bot) + UP * (y_spacing * 4 / 3)
            ),
            run_time=12,
            rate_func=smooth,
        )
        self.wait(5)

        # ============= 4) REDUCED TABLE (4 COLUMNS) =============
        # top 5, dummy "...", bottom 4
        dummy_row = pd.DataFrame([["..."] * len(data.columns)], columns=data.columns)
        top_5 = data.head(5)
        bot_4 = data.tail(4)
        reduced_data = pd.concat([top_5, dummy_row, bot_4], ignore_index=True)
        # rows_4col => (ID, Cond, KvL Score, KvL Klasse)
        rows_4col = [list(reduced_data.columns)] + reduced_data.values.tolist()

        col_widths_4 = [1, 2, 2, 2]
        x_pos_4 = [
            sum(col_widths_4[:j]) + col_widths_4[j] / 2 - sum(col_widths_4) / 2
            for j in range(len(col_widths_4))
        ]

        table_4col = VGroup()
        for i, row in enumerate(rows_4col):
            for j, val in enumerate(row):
                if i == 0:
                    color_txt = "#FFD700"
                    disp_val = str(val)
                    txt_obj = Text(disp_val, color=color_txt).scale(0.5)
                else:
                    cond = row[1]
                    color_txt = color_map.get(cond, color_map["Other"])
                    # col 3 => we start blank
                    if j == 3:
                        disp_val = ""
                        txt_obj = Text(disp_val, color=color_txt).scale(0.4)
                    else:
                        disp_val = str(val)
                        txt_obj = Text(disp_val, color=color_txt).scale(0.5)
                border = Rectangle(
                    width=col_widths_4[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                xx = x_pos_4[j]
                txt_obj.move_to([xx, -i * y_spacing, 0])
                border.move_to([xx, -i * y_spacing, 0])
                table_4col.add(VGroup(border, txt_obj))

        table_4col.scale(0.7)
        table_4col.to_edge(LEFT)
        top_4col = table_4col.get_top()[1]
        desired_4col = config.frame_height / 2 - 0.5
        table_4col.shift(UP * (desired_4col - top_4col))

        self.play(FadeOut(table_3col), FadeIn(table_4col), run_time=3)
        self.wait()

        # animate the 4th column
        n_rows_4 = len(rows_4col)  # 1 header + top5 + dummy + bottom4 => 1+10=11
        for i in range(1, n_rows_4):
            cell = table_4col[i * 4 + 3]
            actual_value = str(rows_4col[i][3])
            if actual_value == "...":
                # skip dummy
                continue
            cond = rows_4col[i][1]
            tcol = color_map.get(cond, color_map["Other"])
            new_label = (
                Text(actual_value, color=tcol).scale(0.4).move_to(cell[1].get_center())
            )
            self.play(Transform(cell[1], new_label), run_time=0.5)
            self.wait(max(0.1, 0.5 - 0.03 * i))
        self.wait(2)

        # ============= 5) CREATE THE FINAL 3-COL => "new_reduced_rows" =============
        # so we can animate cells => bins
        # We keep columns: ID(0), Cond(1), KvL Klasse(3)
        self.wait(3)
        new_reduced_rows = []
        for row in rows_4col:
            # row => [ID, Cond, KvL Score, KvL Klasse]
            # keep => [ID, Cond, KvL Klasse]
            new_reduced_rows.append([row[0], row[1], row[3]])

        # build the new table => 3 columns
        col_widths_3b = [1, 2, 2]
        x_pos_3b = [
            sum(col_widths_3b[:j]) + col_widths_3b[j] / 2 - sum(col_widths_3b) / 2
            for j in range(len(col_widths_3b))
        ]

        new_table_3b = VGroup()
        for i, row in enumerate(new_reduced_rows):
            for j, val in enumerate(row):
                if i == 0:
                    # header => gold
                    txt_color = "#FFD700"
                    txt_obj = Text(str(val), color=txt_color).scale(0.5)
                else:
                    cond = row[1]
                    txt_color = color_map.get(cond, color_map["Other"])
                    if j == 2:
                        txt_obj = Text(str(val), color=txt_color).scale(0.4)
                    else:
                        txt_obj = Text(str(val), color=txt_color).scale(0.5)

                rect = Rectangle(
                    width=col_widths_3b[j],
                    height=y_spacing,
                    color=GOLD_A,
                    stroke_opacity=0.4,
                )
                xx = x_pos_3b[j]
                txt_obj.move_to([xx, -i * y_spacing, 0])
                rect.move_to([xx, -i * y_spacing, 0])
                new_table_3b.add(VGroup(rect, txt_obj))

        new_table_3b.scale(0.7)
        new_table_3b.to_edge(LEFT)
        top3b = new_table_3b.get_top()[1]
        desired3b = config.frame_height / 2 - 0.5
        new_table_3b.shift(UP * (desired3b - top3b))

        # transform the 4-col => new 3-col
        self.play(Transform(table_4col, new_table_3b), run_time=1)
        self.wait(2)

        # reduce stroke, add outer frame
        table_4col.set_stroke(opacity=0.2)
        outer_frame = Rectangle(
            width=table_4col.get_width(),
            height=table_4col.get_height(),
            color=GOLD_A,
            stroke_width=2,
            fill_opacity=0,
        )
        outer_frame.move_to(table_4col.get_center())
        self.play(FadeIn(outer_frame), run_time=1)
        self.wait(2)

        # ============= 6) SETUP HISTOGRAM AXES =============
        x_range = [0, 100, 5]
        y_range = [0, 11, 2]

        # custom ticks => midpoints => 2.5, 7.5, ...
        custom_tick_positions = [2.5 + 5 * i for i in range(20)]
        custom_tick_labels = [f"{5 * i}-{5 * (i + 1)}" for i in range(20)]

        # top axes => Wandeling
        axes_top = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=8,
            y_length=2.5,
            axis_config={"color": GOLD_A, "include_numbers": False},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": custom_tick_positions,
                "include_tip": False,
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(0, 12, 2),
                "numbers_to_exclude": [],
                "include_tip": False,
            },
        )
        axes_top.to_edge(RIGHT, buff=0.8)
        axes_top.shift(UP * 2.3)

        # replace x ticks => custom labels
        for i, tick in enumerate(axes_top.x_axis.numbers):
            lbl = Text(custom_tick_labels[i], font_size=15, color=GOLD_A)
            lbl.rotate(45 * DEGREES)
            lbl.move_to(tick.get_center())
            tick.become(lbl)
        for t in axes_top.y_axis.numbers:
            t.set(font_size=18)
        for tk in axes_top.x_axis.get_tick_marks():
            tk.set_stroke(width=1, opacity=0.5)
        for tk in axes_top.y_axis.get_tick_marks():
            tk.set_stroke(width=1, opacity=0.5)

        vert_lab_top = Text("Frequentie", font_size=15, color=GOLD_A).rotate(PI / 2)
        vert_lab_top.next_to(axes_top.y_axis, LEFT, buff=0.0)
        title_top = Text(
            "KvL Scores voor Conditie 'Wandeling'", font_size=20, color=GOLD_A
        )
        title_top.next_to(axes_top, UP, buff=0.0)

        # bottom => Mindfulness
        axes_bottom = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=8,
            y_length=2.5,
            axis_config={"color": GOLD_A, "include_numbers": False},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": custom_tick_positions,
                "include_tip": False,
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": range(0, 12, 2),
                "numbers_to_exclude": [],
                "include_tip": False,
            },
        )
        axes_bottom.next_to(axes_top, DOWN, buff=0.5)
        axes_bottom.align_to(axes_top, RIGHT)

        for i, tick in enumerate(axes_bottom.x_axis.numbers):
            lbl = Text(custom_tick_labels[i], font_size=15, color=GOLD_A)
            lbl.rotate(45 * DEGREES)
            lbl.move_to(tick.get_center())
            tick.become(lbl)
        for t in axes_bottom.y_axis.numbers:
            t.set(font_size=15)
        for tk in axes_bottom.x_axis.get_tick_marks():
            tk.set_stroke(width=1, opacity=0.5)
        for tk in axes_bottom.y_axis.get_tick_marks():
            tk.set_stroke(width=1, opacity=0.5)

        vert_lab_bot = Text("Frequentie", font_size=15, color=GOLD_A).rotate(PI / 2)
        vert_lab_bot.next_to(axes_bottom.y_axis, LEFT, buff=0.0)
        title_bottom = Text(
            "KvL Scores voor Conditie 'Mindfulness'", font_size=20, color=GOLD_A
        )
        title_bottom.next_to(axes_bottom, UP, buff=-0.25)

        self.play(Create(axes_top), Write(title_top), Write(vert_lab_top), run_time=4)
        self.wait(1)
        self.play(
            Create(axes_bottom), Write(title_bottom), Write(vert_lab_bot), run_time=4
        )
        self.wait(2)

        # ============= 7) ANIMATE TABLE CELLS => DOTS (HISTOGRAM BINS) =============

        # build a map => "0-5" => 2.5, ...
        klasse_midpoints = {f"{5 * i}-{5 * (i + 1)}": 2.5 + 5 * i for i in range(20)}

        def parabola_path(p0, p1, height=1.5):
            return ParametricFunction(
                lambda t: (1 - t) ** 2 * p0
                + 2 * (1 - t) * t * ((p0 + p1) / 2 + UP * height)
                + t**2 * p1,
                t_range=[0, 1],
            ).set_stroke(width=2)

        # measure vertical step from top => freq=0..1
        y0t = axes_top.y_axis.n2p(0)
        y1t = axes_top.y_axis.n2p(1)
        vertical_step = (y1t - y0t)[1]

        frequencies = {}
        dot_map = {}

        # top rows => i=1..5
        for i in range(1, 6):
            row_data = new_reduced_rows[i]  # [ID, Cond, KvL Klasse]
            cond = row_data[1]
            klasse_label = row_data[2]
            if klasse_label in ["", "..."]:
                continue
            # table_4col => we originally had 4 columns => the cell for (i, col=3) => index => i*4+3
            cell_idx = i * 4 + 3
            start_pos = table_4col[cell_idx].get_center()

            freq_key = (klasse_label, cond)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            # pick color
            if cond == "Wandeling":
                target_axes = axes_top
                dot_color = color_map["Wandeling"]
            else:
                target_axes = axes_bottom
                dot_color = color_map["Mindfulness"]

            # highlight
            highlight = Rectangle(
                width=col_widths_4[2],
                height=y_spacing,
                color=dot_color,
            ).move_to(start_pos)
            self.play(Create(highlight), run_time=0.7)

            # temporary text
            anim_txt = Text(str(klasse_label), color=dot_color).scale(0.5)
            anim_txt.move_to(start_pos)
            self.play(FadeIn(anim_txt), run_time=0.7)

            mp_val = klasse_midpoints.get(klasse_label, None)
            if mp_val is None:
                continue

            freq_cnt = frequencies[freq_key] + 1
            x_axis_pos = target_axes.x_axis.n2p(mp_val)
            target_pos = x_axis_pos + UP * (freq_cnt * vertical_step)

            dot = Dot(color=dot_color, radius=0.05).move_to(start_pos)
            dot_map.setdefault(freq_key, []).append(dot)
            path = parabola_path(start_pos, target_pos, height=1.5)
            self.play(MoveAlongPath(dot, path), run_time=0.9)

            self.play(FadeOut(anim_txt), run_time=0.4)
            frequencies[freq_key] = freq_cnt
            self.play(FadeOut(highlight), run_time=0.3)
            self.wait(0.1)

        # leftover => dummy => index=6 => new_reduced_rows[6] => leftover data is from row 5..96
        leftover_data = data.iloc[5:96]
        for idx, row in leftover_data.iterrows():
            kl = row["KvL Klasse"]
            cond = row["Conditie"]
            if kl in ["", "..."]:
                continue
            # the dummy row => i=6 => 4th col => i*4+3 => 6*4+3=27
            dummy_cell_center = table_4col[6 * 4 + 3].get_center()
            start_pos = dummy_cell_center

            freq_key = (kl, cond)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            if cond == "Wandeling":
                target_axes = axes_top
                dot_color = color_map["Wandeling"]
            else:
                target_axes = axes_bottom
                dot_color = color_map["Mindfulness"]

            mp_val = klasse_midpoints.get(kl, None)
            if mp_val is None:
                continue

            freq_cnt = frequencies[freq_key] + 1
            x_axis_pos = target_axes.x_axis.n2p(mp_val)
            target_pos = x_axis_pos + UP * (freq_cnt * vertical_step)

            dot = Dot(color=dot_color, radius=0.05).move_to(start_pos)
            dot_map.setdefault(freq_key, []).append(dot)

            self.play(dot.animate.move_to(target_pos), run_time=0.2)
            frequencies[freq_key] = freq_cnt

        # bottom rows => i=7..10
        for i in range(7, 11):
            row_data = new_reduced_rows[i]
            kl = row_data[2]
            cond = row_data[1]
            if kl in ["", "..."]:
                continue

            cell_idx = i * 4 + 3
            start_pos = table_4col[cell_idx].get_center()

            freq_key = (kl, cond)
            frequencies[freq_key] = frequencies.get(freq_key, 0)

            if cond == "Wandeling":
                target_axes = axes_top
                dot_color = color_map["Wandeling"]
            else:
                target_axes = axes_bottom
                dot_color = color_map["Mindfulness"]

            highlight = Rectangle(
                width=col_widths_4[2],
                height=y_spacing,
                color=dot_color,
            ).move_to(start_pos)
            self.play(Create(highlight), run_time=0.5)
            anim_txt = Text(kl, color=dot_color).scale(0.5).move_to(start_pos)
            self.play(FadeIn(anim_txt), run_time=0.5)

            mp_val = klasse_midpoints.get(kl, None)
            if mp_val is None:
                continue
            freq_cnt = frequencies[freq_key] + 1
            x_axis_pos = target_axes.x_axis.n2p(mp_val)
            target_pos = x_axis_pos + UP * (freq_cnt * vertical_step)

            dot = Dot(color=dot_color, radius=0.05).move_to(start_pos)
            dot_map.setdefault(freq_key, []).append(dot)
            path = parabola_path(start_pos, target_pos, height=0.5)
            self.play(MoveAlongPath(dot, path), run_time=0.7)

            self.play(FadeOut(anim_txt), run_time=0.3)
            frequencies[freq_key] = freq_cnt
            self.play(FadeOut(highlight), run_time=0.2)
            self.wait(0.1)

        self.wait(2)

        # ============= 8) DOTS => BARS TRANSITION =============
        bars = VGroup()
        transforms = []
        top_xlen = axes_top.x_length

        for (klass_label, cond_label), freq_count in frequencies.items():
            if freq_count <= 0:
                continue
            if (klass_label, cond_label) not in dot_map:
                continue
            dot_list = dot_map[(klass_label, cond_label)]
            dot_group = VGroup(*dot_list)

            if cond_label == "Wandeling":
                target_axes = axes_top
                bar_c = color_map["Wandeling"]
            else:
                target_axes = axes_bottom
                bar_c = color_map["Mindfulness"]

            mp_val = klasse_midpoints.get(klass_label, None)
            if mp_val is None:
                continue
            x_coord = target_axes.x_axis.n2p(mp_val)
            bar_height = freq_count * vertical_step

            bar_width = 5 * (top_xlen / (x_range[1] - x_range[0]))  # ~0.4
            bar_rect = Rectangle(
                width=bar_width,
                height=bar_height,
                color=bar_c,
                fill_color=bar_c,
                fill_opacity=0.8,
            )
            bar_rect.move_to(x_coord, aligned_edge=DOWN)

            transforms.append(Transform(dot_group, bar_rect))
            bars.add(bar_rect)

        self.play(*transforms, run_time=2)
        self.play(FadeIn(bars))
        self.wait(2)

        # ============= 9) SUMMARY STATS + MEAN/MEDIAN LINES =============
        means = data.groupby("Conditie")["KvL Score"].mean()
        medians = data.groupby("Conditie")["KvL Score"].median()
        stds = data.groupby("Conditie")["KvL Score"].std()
        skews = data.groupby("Conditie")["KvL Score"].skew()

        def stats_block(cond_name, color):
            mu = means[cond_name]
            md = medians[cond_name]
            sd = stds[cond_name]
            sk = skews[cond_name]
            l1 = MathTex(rf"\mathit{{M}} = {mu:.2f}", color=color, font_size=20)
            l2 = MathTex(rf"\mathit{{MED}} = {md:.2f}", color=color, font_size=20)
            l3 = MathTex(rf"\mathit{{SD}} = {sd:.2f}", color=color, font_size=20)
            l4 = MathTex(rf"\mathit{{SK}} = {sk:.2f}", color=color, font_size=20)
            return VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        stats_w = stats_block("Wandeling", color_map["Wandeling"])
        stats_m = stats_block("Mindfulness", color_map["Mindfulness"])

        # place them near each axis
        stats_w.next_to(axes_top.y_axis, RIGHT, buff=0.5).shift(UP * 0.1)
        stats_m.next_to(axes_bottom.y_axis, RIGHT, buff=0.5).shift(UP * 0.1)

        self.play(FadeIn(stats_w), FadeIn(stats_m))
        self.wait(1)

        def add_stat_indicator(ax, x_val, color, label_tex, is_median=False):
            axis_pt = ax.x_axis.n2p(x_val)
            arrow_start = axis_pt + DOWN * 0.7
            if is_median:
                # dashed line
                dline = DashedLine(
                    start=arrow_start,
                    end=axis_pt,
                    dash_length=0.06,
                    color=color,
                    stroke_width=3,
                )
                lbl = MathTex(label_tex, color=color, font_size=20)
                lbl.next_to(dline, DOWN * 0.1 + RIGHT, buff=0.10)
                return VGroup(dline, lbl)
            else:
                # arrow
                arr = Arrow(
                    start=arrow_start,
                    end=axis_pt,
                    buff=0,
                    stroke_width=3,
                    color=color,
                )
                lbl = MathTex(label_tex, color=color, font_size=20)
                lbl.next_to(arr, DOWN * 0.1 + LEFT, buff=0.10)
                return VGroup(arr, lbl)

        # top => Wandeling
        mean_w = means["Wandeling"]
        med_w = medians["Wandeling"]
        w_mean_ind = add_stat_indicator(
            axes_top, mean_w, color_map["Wandeling"], r"\mathit{M}", False
        )
        w_med_ind = add_stat_indicator(
            axes_top, med_w, color_map["Wandeling"], r"\mathit{MED}", True
        )

        # bottom => Mindfulness
        mean_m = means["Mindfulness"]
        med_m = medians["Mindfulness"]
        m_mean_ind = add_stat_indicator(
            axes_bottom, mean_m, color_map["Mindfulness"], r"\mathit{M}", False
        )
        m_med_ind = add_stat_indicator(
            axes_bottom, med_m, color_map["Mindfulness"], r"\mathit{MED}", True
        )

        self.play(
            FadeIn(w_mean_ind),
            FadeIn(w_med_ind),
            FadeIn(m_mean_ind),
            FadeIn(m_med_ind),
            run_time=2,
        )
        self.wait(3)


# source .venv/bin/activate
# manim -qm --disable_caching DataTableToHistMindWalkGPT.py DataToHistMW_GPT | tee outputMWGPT.txt
# manim -qk -p --disable_caching DataTableToHistMindWalkGTP.py DataToHistMW_GPT
