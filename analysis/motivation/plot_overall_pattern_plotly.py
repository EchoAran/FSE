from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import plotly.graph_objects as go


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "motivation" / "results"
LSRI_PATH = RESULTS_DIR / "analysis" / "lsri.jsonl"
SUMMARY_PATH = RESULTS_DIR / "summary.json"
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_STEM = OUTPUT_DIR / "motivation_overall_pattern_plotly"
FIGURE_WIDTH = 1840
FIGURE_HEIGHT = 1080
MARGINS = dict(l=60, r=60, t=65, b=65)
PLOT_HEIGHT = FIGURE_HEIGHT - MARGINS["t"] - MARGINS["b"]
PLOT_WIDTH = FIGURE_WIDTH - MARGINS["l"] - MARGINS["r"]
NODE_THICKNESS = 22
FONT_FAMILY = "Times New Roman"

REQUIREMENT_TYPES = [
    "Functional Behavior",
    "Constraint & Environment",
    "Data",
    "Interface",
    "Exception & Boundary",
    "Quality",
    "Business Rule",
    "Actor & Permission",
]
EEO_LEVELS = ["Yes", "Uncertain", "No"]
UPTAKE_LEVELS = ["Revised", "Extended", "No Uptake", "Insufficient Evidence"]

TYPE_COLORS = {
    "Functional Behavior": "#3E6FB0",
    "Constraint & Environment": "#7561AA",
    "Data": "#2CA6C2",
    "Interface": "#008F9C",
    "Exception & Boundary": "#9854A2",
    "Quality": "#4D8FD0",
    "Business Rule": "#697CB5",
    "Actor & Permission": "#607D91",
}
EEO_COLORS = {
    "Yes": "#D99A23",
    "Uncertain": "#E56B2F",
    "No": "#B83B48",
}
UPTAKE_COLORS = {
    "Revised": "#C2543F",
    "Extended": "#E2A437",
    "No Uptake": "#8C375A",
    "Insufficient Evidence": "#8F8278",
}


def rgba(hex_color: str, alpha: float) -> str:
    color = hex_color.lstrip("#")
    red, green, blue = (int(color[index : index + 2], 16) for index in (0, 2, 4))
    return f"rgba({red},{green},{blue},{alpha})"


FLOW_COLOR = rgba("#5D656E", 0.34)


def load_data() -> tuple[list[dict], dict]:
    rows = [
        json.loads(line)
        for line in LSRI_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    return rows, summary


def validate_data(rows: list[dict], summary: dict) -> None:
    if len(rows) != summary["lsri_total"]:
        raise ValueError("LSRI total does not reconcile with summary.json")
    for field, levels in [
        ("requirement_type", REQUIREMENT_TYPES),
        ("eeo", EEO_LEVELS),
        ("response_uptake", UPTAKE_LEVELS),
    ]:
        observed = Counter(row[field] for row in rows)
        if observed != Counter(summary[field]):
            raise ValueError(f"{field} counts do not reconcile with summary.json")
        if set(observed) != set(levels):
            raise ValueError(f"Unexpected {field} values: {sorted(set(observed) - set(levels))}")


def node_y_positions(levels: list[str], totals: Counter, scale: float) -> list[float]:
    gaps = [6.5] * 6 + [36, 0] if levels == REQUIREMENT_TYPES else [75 / (len(levels) - 1)] * len(levels)
    cursor = 15.0
    positions = []
    for level, gap in zip(levels, gaps):
        height = totals[level] * scale
        positions.append((cursor + height / 2) / PLOT_HEIGHT)
        cursor += height + gap
    return positions


def build_figure(rows: list[dict]) -> go.Figure:
    total = len(rows)
    type_totals = Counter(row["requirement_type"] for row in rows)
    eeo_totals = Counter(row["eeo"] for row in rows)
    uptake_totals = Counter(row["response_uptake"] for row in rows)
    type_to_eeo = Counter((row["requirement_type"], row["eeo"]) for row in rows)
    eeo_to_uptake = Counter((row["eeo"], row["response_uptake"]) for row in rows)

    levels = REQUIREMENT_TYPES + EEO_LEVELS + UPTAKE_LEVELS
    level_index = {level: index for index, level in enumerate(levels)}
    totals = type_totals | eeo_totals | uptake_totals
    small_levels = {"Actor & Permission", "Insufficient Evidence"}
    labels = [
        "" if level in small_levels else f"{level}  {totals[level] / total * 100:.1f}%"
        for level in levels
    ]
    node_colors = [
        *[TYPE_COLORS[level] for level in REQUIREMENT_TYPES],
        *[EEO_COLORS[level] for level in EEO_LEVELS],
        *[UPTAKE_COLORS[level] for level in UPTAKE_LEVELS],
    ]

    sources: list[int] = []
    targets: list[int] = []
    values: list[int] = []
    link_colors: list[str] = []
    link_labels: list[str] = []

    for requirement_type in REQUIREMENT_TYPES:
        for eeo in EEO_LEVELS:
            count = type_to_eeo[(requirement_type, eeo)]
            if count == 0:
                continue
            sources.append(level_index[requirement_type])
            targets.append(level_index[eeo])
            values.append(count)
            link_colors.append(FLOW_COLOR)
            link_labels.append(
                f"{requirement_type} → {eeo}<br>"
                f"{count / type_totals[requirement_type]:.1%} within {requirement_type}"
            )

    for eeo in EEO_LEVELS:
        for uptake in UPTAKE_LEVELS:
            count = eeo_to_uptake[(eeo, uptake)]
            if count == 0:
                continue
            sources.append(level_index[eeo])
            targets.append(level_index[uptake])
            values.append(count)
            link_colors.append(FLOW_COLOR)
            link_labels.append(
                f"{eeo} → {uptake}<br>"
                f"{count / eeo_totals[eeo]:.1%} within EEO = {eeo}"
            )

    node_x = [0.02] * len(REQUIREMENT_TYPES)
    node_x += [0.50] * len(EEO_LEVELS)
    node_x += [0.98] * len(UPTAKE_LEVELS)
    scale = (PLOT_HEIGHT - 7 * 15) / total
    node_y = node_y_positions(REQUIREMENT_TYPES, type_totals, scale)
    node_y += node_y_positions(EEO_LEVELS, eeo_totals, scale)
    node_y += node_y_positions(UPTAKE_LEVELS, uptake_totals, scale)

    figure = go.Figure(
        go.Sankey(
            arrangement="fixed",
            orientation="h",
            valueformat=",d",
            node=dict(
                pad=15,
                thickness=NODE_THICKNESS,
                line=dict(color="rgba(31,41,55,0.75)", width=0.8),
                label=labels,
                color=node_colors,
                x=node_x,
                y=node_y,
                customdata=levels,
                hovertemplate=(
                    "<b>%{customdata}</b><br>%{value:,} LSRI units"
                    "<extra></extra>"
                ),
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=link_colors,
                customdata=link_labels,
                hovertemplate=(
                    "<b>%{customdata}</b><br>%{value:,} LSRI units"
                    "<extra></extra>"
                ),
            ),
            textfont=dict(family=FONT_FAMILY, size=26, color="#1F2937", shadow="none", weight=700),
        )
    )
    figure.update_layout(
        width=FIGURE_WIDTH,
        height=FIGURE_HEIGHT,
        margin=MARGINS,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_FAMILY, size=26, color="#1F2937", weight=700),
        annotations=[
            dict(
                x=(0.02 - NODE_THICKNESS / (2 * PLOT_WIDTH) + 0.488) / 2,
                y=1.005,
                xref="paper",
                yref="paper",
                text="<b>P(EEO | requirement type)</b>",
                showarrow=False,
                xanchor="center",
                yanchor="bottom",
                font=dict(size=36, color="#000000", weight=700),
            ),
            dict(
                x=(0.512 + 0.98 + NODE_THICKNESS / (2 * PLOT_WIDTH)) / 2,
                y=1.005,
                xref="paper",
                yref="paper",
                text="<b>P(response uptake | EEO)</b>",
                showarrow=False,
                xanchor="center",
                yanchor="bottom",
                font=dict(size=36, color="#000000", weight=700),
            ),
            dict(
                x=0.02,
                y=-0.005,
                xref="paper",
                yref="paper",
                text="<b>Requirement type</b>",
                showarrow=False,
                xanchor="left",
                yanchor="top",
                font=dict(size=33, color="#000000", weight=700),
            ),
            dict(
                x=0.50,
                y=-0.005,
                xref="paper",
                yref="paper",
                text="<b>Earlier elicitation opportunity (EEO)</b>",
                showarrow=False,
                xanchor="center",
                yanchor="top",
                font=dict(size=33, color="#000000", weight=700),
            ),
            dict(
                x=0.98,
                y=-0.005,
                xref="paper",
                yref="paper",
                text="<b>Response uptake</b>",
                showarrow=False,
                xanchor="right",
                yanchor="top",
                font=dict(size=33, color="#000000", weight=700),
            ),
            dict(
                x=0.02 + (NODE_THICKNESS / 2 + 3) / PLOT_WIDTH,
                y=19 / PLOT_HEIGHT,
                xref="paper", yref="paper",
                text=f"Actor & Permission  {type_totals['Actor & Permission'] / total * 100:.1f}%",
                showarrow=False, xanchor="left", yanchor="bottom",
                font=dict(size=26, color="#1F2937", weight=700),
            ),
            dict(
                x=0.96,
                y=19 / PLOT_HEIGHT,
                xref="paper", yref="paper",
                text=f"Insufficient Evidence  {uptake_totals['Insufficient Evidence'] / total * 100:.1f}%",
                showarrow=False, xanchor="right", yanchor="bottom",
                font=dict(size=26, color="#1F2937", weight=700),
            ),
        ],
        shapes=[
            dict(
                type="rect", xref="paper", yref="paper",
                x0=x0, x1=x1,
                y0=15 / PLOT_HEIGHT, y1=1 - 15 / PLOT_HEIGHT,
                line=dict(color=color, width=1.5, dash="dash"), layer="above",
            )
            for x0, x1, color in [
                (0.02 - NODE_THICKNESS / (2 * PLOT_WIDTH), 0.488, "rgba(65,105,145,0.55)"),
                (0.512, 0.98 + NODE_THICKNESS / (2 * PLOT_WIDTH), "rgba(165,104,50,0.55)"),
            ]
        ],
    )
    return figure


def save_figure(figure: go.Figure) -> None:
    figure.write_html(
        OUTPUT_STEM.with_suffix(".html"),
        include_plotlyjs="inline",
        full_html=True,
        config={"displayModeBar": False, "responsive": True},
    )
    figure.write_image(OUTPUT_STEM.with_suffix(".svg"), format="svg")
    figure.write_image(OUTPUT_STEM.with_suffix(".pdf"), format="pdf")
    figure.write_image(OUTPUT_STEM.with_suffix(".png"), format="png", scale=1)


def main() -> None:
    rows, summary = load_data()
    validate_data(rows, summary)
    figure = build_figure(rows)
    save_figure(figure)
    print(f"Validated {len(rows):,} LSRI units.")
    print(f"Wrote {OUTPUT_STEM}.html/.svg/.pdf/.png")


if __name__ == "__main__":
    main()
