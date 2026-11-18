# PowerPoint Exhibit Deck (no Gamma)

Tested python-pptx recipe for Step 2, Path B: title slide, neutral divider,
native chart, native table, 16:9. Keep the helpers; replace the calls at the
bottom with the case's slides in interview order.

## Contents

- Setup
- Recipe
- Verify the file
- Adapting it

## Setup

- `pip install python-pptx`, or run without installing:
  `uv run --with python-pptx python build_deck.py`.
- Save the script in a working folder, never inside a skills folder.
- Name the output after the case (`case-7-exhibits.pptx`).

## Recipe

```python
"""Case exhibit deck: one exhibit per slide, native charts and tables, 16:9."""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

FONT = "Arial"  # renders the same in PowerPoint and Google Slides
INK, MUTED, WHITE = RGBColor(0x1F, 0x29, 0x37), RGBColor(0x6B, 0x72, 0x80), RGBColor(0xFF, 0xFF, 0xFF)
PALETTE = [RGBColor(0x1D, 0x4E, 0xD8), RGBColor(0x94, 0xA3, 0xB8), RGBColor(0x0F, 0x76, 0x6E), RGBColor(0xD9, 0x77, 0x06)]
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def style(p, size, bold=False, color=INK):
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = FONT, Pt(size), bold, color


def add_text(slide, text, top, size, bold=False, color=INK, height=0.8):
    tf = slide.shapes.add_textbox(Inches(0.7), Inches(top), Inches(11.9), Inches(height)).text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        style(p, size, bold, color)


def new_slide(title, subtitle=None, note=None):
    slide = prs.slides.add_slide(BLANK)
    add_text(slide, title, 0.4, 30, bold=True)
    if subtitle:
        add_text(slide, subtitle, 1.1, 16, color=MUTED, height=0.5)
    if note:  # source footnote, kept verbatim
        add_text(slide, note, 6.85, 12, color=MUTED, height=0.5)
    return slide


def title_slide(title, tags, prompt, question):
    slide = new_slide(title, tags)
    add_text(slide, prompt, 1.9, 20 if len(prompt) < 450 else 16, height=2.9)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(5.1), Inches(11.9), Inches(1.4))
    box.fill.solid()
    box.fill.fore_color.rgb = PALETTE[0]
    box.line.fill.background()
    box.text_frame.word_wrap = True
    box.text_frame.paragraphs[0].text = question
    style(box.text_frame.paragraphs[0], 22, bold=True, color=WHITE)


def divider(title, note=None):
    slide = prs.slides.add_slide(BLANK)
    add_text(slide, title, 3.0, 40, bold=True, height=1.0)
    if note:  # e.g. "Placeholder: paste the original exhibit here"
        add_text(slide, note, 4.1, 18, color=MUTED)


def chart_slide(title, categories, series, y_title=None, x_title=None, fmt="#,##0",
                kind=XL_CHART_TYPE.COLUMN_CLUSTERED, y_max=None, subtitle=None, note=None):
    slide = new_slide(title, subtitle, note)
    data = CategoryChartData(number_format=fmt)
    data.categories = categories
    for name, values in series.items():
        data.add_series(name, values)
    chart = slide.shapes.add_chart(kind, Inches(0.7), Inches(1.7), Inches(11.9), Inches(5.0), data).chart
    chart.font.name, chart.font.size = FONT, Pt(14)
    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.number_format, plot.data_labels.number_format_is_linked = fmt, False
    pie = kind in (XL_CHART_TYPE.PIE, XL_CHART_TYPE.DOUGHNUT)
    for i, item in enumerate(plot.series[0].points if pie else plot.series):
        item.format.fill.solid()
        item.format.fill.fore_color.rgb = PALETTE[i % len(PALETTE)]
    if pie:
        plot.data_labels.show_category_name = True
        chart.has_legend = False
        return
    for axis, label in ((chart.value_axis, y_title), (chart.category_axis, x_title)):
        if label:
            axis.has_title = True
            axis.axis_title.text_frame.text = label
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.tick_labels.number_format = fmt
    chart.value_axis.tick_labels.number_format_is_linked = False
    if y_max is not None:  # match the source exhibit's scale
        chart.value_axis.minimum_scale, chart.value_axis.maximum_scale = 0, y_max
    chart.has_legend = len(series) > 1
    if chart.has_legend:
        chart.legend.position, chart.legend.include_in_layout = XL_LEGEND_POSITION.BOTTOM, False


def table_slide(title, header, rows, subtitle=None, note=None):
    slide = new_slide(title, subtitle, note)
    n_rows = len(rows) + 1
    shape = slide.shapes.add_table(n_rows, len(header), Inches(0.7), Inches(1.7),
                                   Inches(11.9), Inches(min(0.55 * n_rows, 5.0)))
    for r, row in enumerate([header] + rows):
        for c, value in enumerate(row):
            cell = shape.table.cell(r, c)
            cell.text = value  # strings exactly as printed: "1,250", "(30)", "12%"
            p = cell.text_frame.paragraphs[0]
            style(p, 18, bold=r == 0, color=WHITE if r == 0 else INK)
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.RIGHT


# Placeholder values below: replace every figure with the source's exact numbers.
title_slide("Case 7: Solar Panel Maker", "Industrial goods  ·  Market entry",
            "Our client, a mid-sized solar panel maker, is weighing entry into a new market.",
            "Should the client enter the market, and how?")
divider("Part 1: Market size")
chart_slide("Exhibit A: Installed capacity by year", ["2022", "2023", "2024"],
            {"Client": [1.2, 2.0, 3.1], "Market": [4.0, 5.5, 7.2]},
            y_title="GW", x_title="Year", fmt="0.0", y_max=8, note="Source: industry association")
chart_slide("Exhibit B: Market share", ["Firm A", "Firm B", "Firm C", "Other"],
            {"Share": [0.35, 0.25, 0.20, 0.20]}, fmt="0%", kind=XL_CHART_TYPE.PIE)
table_slide("Exhibit C: Income statement ($M)", ["Line item", "2023", "2024"],
            [["Revenue", "1,250", "1,410"], ["COGS", "(800)", "(905)"], ["Gross profit", "450", "505"]])
divider("Part 2: Recommendation")
prs.save("case-7-exhibits.pptx")
```

## Verify the file

Run after every build: `python verify_deck.py case-7-exhibits.pptx`. It
re-opens the file, prints each slide's title and every chart or table value,
and flags any slide holding two exhibits. Check each printed number against
the source.

```python
import sys
from pptx import Presentation

for i, slide in enumerate(Presentation(sys.argv[1]).slides, 1):
    title = next((s.text_frame.text for s in slide.shapes if s.has_text_frame), "")
    exhibits = [s for s in slide.shapes if s.has_chart or s.has_table]
    print(f"{i}. {title}" + ("  <-- MORE THAN ONE EXHIBIT" if len(exhibits) > 1 else ""))
    for s in exhibits:
        if s.has_chart:
            for ser in s.chart.plots[0].series:
                print(f"   {ser.name}: {list(ser.values)}")
        else:
            for row in s.table.rows:
                print("   " + " | ".join(c.text for c in row.cells))
```

## Adapting it

- **Chart kinds:** `COLUMN_CLUSTERED` (default), `BAR_CLUSTERED` for long
  category names, `COLUMN_STACKED` for stacked bars, `LINE_MARKERS` for
  trends (keeps the theme's line colors), `PIE` or `DOUGHNUT` for shares.
- **`fmt`:** an Excel number format that matches the source's labels:
  `"#,##0"`, `"0.0"`, `"$#,##0"`, `"0%"` (pass 0.35 to show 35%).
- **`y_max`:** set it when the source chart has a fixed scale.
- **Tables:** pass every cell as a string exactly as printed, brackets and
  units included; never reformat or round.
- **Placeholder exhibit:** `divider("Exhibit B: <title>", "Placeholder: paste
  the original exhibit here")`, then tell the user in Step 3.
- **Nothing else on the slides:** no speaker notes, images, or logos.
