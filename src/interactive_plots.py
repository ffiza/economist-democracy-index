import plotly.graph_objects as go
from plotly.graph_objects import Figure

from colors import Colors
from data import Data
from config import Config


def _add_annotations(fig: Figure) -> None:
    colors = Colors()
    fig.add_annotation(
        text="<b>The Economist Democracy Index, 2006 - 2023</b>",
        x=-0.03, y=1.25, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 30})
    fig.add_annotation(
        text="The Democracy Index published by the Economist Group is an"
        + " index measuring the quality of democracy across the world. This"
        + " quantitative",
        x=-0.03, y=1.17, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 15})
    fig.add_annotation(
        text="and comparative assessment is centrally concerned"
        + " with democratic rights and democratic institutions. The index is"
        + " based on 60 indicators",
        x=-0.03, y=1.13, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 15})
    fig.add_annotation(
        text="grouped into five categories, measuring pluralism,"
        + " civil liberties, and political culture.",
        x=-0.03, y=1.09, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 15})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=-0.03, y=-0.06, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 11, "weight": 600})
    fig.add_annotation(
        text="<b>LESS DEMOCRATIC</b>",
        x=0.001, y=0.01, showarrow=False,
        xref="paper", xanchor="left", yanchor="bottom",
        font={"color": colors.GRAY, "size": 11})
    fig.add_annotation(
        text="<b>MORE DEMOCRATIC</b>",
        x=0.001, y=9.99, showarrow=False,
        xref="paper", xanchor="left", yanchor="top",
        font={"color": colors.GRAY, "size": 11})


def plot_evolution_regions(_add_annotations):
    data = Data()
    config = Config()
    colors = Colors()

    fig = go.Figure()

    fig.update_layout(
        width=736, height=514, plot_bgcolor="white",
        yaxis=dict(range=[0, 10.1], tickvals=[i for i in range(11)],
                   ticks="outside", ticklen=0,
                   tickfont=dict(size=16, color=colors.GRAY, weight=500),
                   zeroline=True, zerolinewidth=2, zerolinecolor=colors.GRAY,
                   showgrid=True, gridcolor=colors.LIGHT_GRAY,
                   gridwidth=2, griddash="dot"),
        xaxis=dict(range=[2006, 2023],
                   tickvals=[year for year in range(2007, 2024, 2)],
                   ticks="outside", tickcolor=colors.GRAY, tickwidth=2,
                   tickfont=dict(size=16, color=colors.GRAY, weight=500),
                   zeroline=False),
        showlegend=False,
        margin=dict(l=30, r=30, t=120, b=60)
    )

    regions = list(data.df["Region"].unique())
    y_offsets = dict(zip(regions, [0.2, -0.2, 0.125, 0.2, -0.2, -0.2, 0.2]))
    region_df = data.get_region_averages()
    for region in regions:
        region_data = region_df[region_df["Region"] == region]
        fig.add_trace(
            go.Scatter(x=region_data["Year"], y=region_data["DemocracyIndex"],
                       mode="markers+lines", name=region,
                       line=dict(color=config.region_colors[region], width=2),
                       hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>"
                                     "Index: %{y}<extra></extra>",
                       hoverlabel=dict(
                           bgcolor="white",
                           bordercolor="rgb(0, 0, 0, 0)",
                           font=dict(color=config.region_colors[region]))))
        fig.add_annotation(
            text="<b>" + region + "</b>", x=0.001, xref="paper",
            y=region_data["DemocracyIndex"][
                region_data["Year"] == 2006].values[0] + y_offsets[region],
            showarrow=False, yanchor="middle",
            font={"color": config.region_colors[region], "size": 12})

    _add_annotations(fig=fig)

    fig.write_html("reports/html/time_series_by_region.html",
                   full_html=False, include_plotlyjs='cdn')


if __name__ == "__main__":
    plot_evolution_regions(_add_annotations)
