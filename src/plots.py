import plotly.graph_objects as go
from plotly.graph_objects import Figure

from colors import Colors
from data import Data, get_yearly_geographic_data
from data import get_index_change_geographic_data
from config import Config


def plot_evolution_regions() -> None:
    data = Data()
    config = Config()
    colors = Colors()

    fig = go.Figure()

    fig.update_layout(
        width=720, height=500, plot_bgcolor="white",
        yaxis=dict(range=[0, 10.1], tickvals=[i for i in range(11)],
                   ticks="outside", ticklen=0,
                   tickfont=dict(size=14, color=colors.DARK_GRAY, weight=400),
                   zeroline=True, zerolinewidth=2, showgrid=True,
                   zerolinecolor=colors.DARK_GRAY, gridcolor=colors.LIGHT_GRAY,
                   gridwidth=1, griddash="solid"),
        xaxis=dict(range=[2005.9, 2024.1],
                   tickvals=[year for year in range(2007, 2024, 2)],
                   ticks="outside", tickcolor=colors.DARK_GRAY, tickwidth=2,
                   tickfont=dict(size=14, color=colors.DARK_GRAY, weight=400),
                   zeroline=False),
        showlegend=False,
        margin=dict(l=20, r=20, t=85, b=50)
    )

    regions = list(data.df["Region"].unique())
    y_offsets = dict(zip(regions, [-0.25, 0.25, 0.3, 0.25, 0.25, 0.25, -0.25]))
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

    fig.add_annotation(
        text="<b>The Economist Democracy Index, 2006 - 2024</b>",
        x=-0.03, y=1.18, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows the evolution of The Economist Democracy Index"
             " between 2006 and 2024, averaged<br>by region.",
        x=-0.03, y=1.1, showarrow=False, align="left",
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 14})
    fig.add_annotation(
        text="<b>MORE DEMOCRATIC</b>",
        x=0.001, y=9.8, showarrow=False,
        xref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 10})
    fig.add_annotation(
        text="<b>LESS DEMOCRATIC</b>",
        x=0.001, y=0.2, showarrow=False,
        xref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 10})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=-0.03, y=-0.08, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 11})

    fig.write_html("reports/html/time_series_by_region.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image("reports/figures/time_series_by_region.png")


def plot_evolution_countries() -> None:
    data = Data()
    colors = Colors()

    fig = go.Figure()

    fig.update_layout(
        width=720, height=500, plot_bgcolor="white",
        yaxis=dict(range=[0, 10.1], tickvals=[i for i in range(11)],
                   ticks="outside", ticklen=0,
                   tickfont=dict(size=14, color=colors.DARK_GRAY, weight=400),
                   zeroline=True, zerolinewidth=2, showgrid=True,
                   zerolinecolor=colors.DARK_GRAY, gridcolor=colors.LIGHT_GRAY,
                   gridwidth=1, griddash="solid"),
        xaxis=dict(range=[2005.9, 2024.1],
                   tickvals=[year for year in range(2007, 2024, 2)],
                   ticks="outside", tickcolor=colors.DARK_GRAY, tickwidth=2,
                   tickfont=dict(size=14, color=colors.DARK_GRAY, weight=400),
                   zeroline=False),
        showlegend=False,
        margin=dict(l=20, r=20, t=85, b=50)
    )

    for country in data.df["Country"].unique():
        country_data = data.df[data.df["Country"] == country]
        fig.add_trace(
            go.Scatter(x=country_data["Year"],
                       y=country_data["DemocracyIndex"],
                       mode="lines", name=country,
                       line=dict(color=colors.LIGHT_GRAY, width=0.5),
                       hoverinfo="skip"))

    _add_country(fig, "Argentina", (2018, 7.3), colors.BLUE)
    _add_country(fig, "Mali", (2013, 6.2), colors.ORANGE)
    _add_country(fig, "Bhutan", (2022.5, 5.25), colors.GREEN)
    _add_country(fig, "Afghanistan", (2022.5, 0.7), colors.RED)
    _add_country(fig, "Norway", (2018, 9.6), colors.PURPLE)

    fig.add_annotation(
        text="<b>The Economist Democracy Index, 2006 - 2024</b>",
        x=-0.03, y=1.18, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows the evolution of The Economist Democracy Index"
             " between 2006 and 2024 for<br>selected countries.",
        x=-0.03, y=1.1, showarrow=False, align="left",
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 14})
    fig.add_annotation(
        text="<b>MORE DEMOCRATIC</b>",
        x=0.001, y=9.8, showarrow=False,
        xref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 10})
    fig.add_annotation(
        text="<b>LESS DEMOCRATIC</b>",
        x=0.001, y=0.2, showarrow=False,
        xref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 10})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=-0.03, y=-0.08, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 11})

    fig.write_html("reports/html/time_series_by_country.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image("reports/figures/time_series_by_country.png")


def _add_country(fig: Figure, country: str, label_pos: tuple,
                 color: str):
    data = Data()
    country_data = data.df[data.df["Country"] == country]
    fig.add_trace(
        go.Scatter(x=country_data["Year"],
                   y=country_data["DemocracyIndex"],
                   mode="markers+lines", name=country,
                   line=dict(color=color, width=2),
                   hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>"
                                 "Index: %{y}<extra></extra>",
                   hoverlabel=dict(
                       bgcolor="white",
                       bordercolor="rgb(0, 0, 0, 0)",
                       font=dict(color=color))))
    fig.add_annotation(
        text="<b>" + country + "</b>", x=label_pos[0], y=label_pos[1],
        showarrow=False, yanchor="middle",
        font={"color": color, "size": 12})


def plot_world_map_index(year: int) -> None:
    df = get_yearly_geographic_data(year=year)
    colors = Colors()

    fig = go.Figure(
        data=go.Choropleth(
            locations=df['ISO_A3_EH'], z=df['DemocracyIndex'],
            text=df['Country'], colorscale='viridis',
            autocolorscale=False, marker_line_color='white',
            marker_line_width=0.3, zmin=0, zmax=10,
            hovertemplate="<b>%{text}</b><br>Index: %{z}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgb(0, 0, 0, 0)"),
            colorbar=dict(
                orientation="h", x=0.5, y=0,
                xanchor="center", yanchor="bottom",
                len=1, thickness=5, tickvals=[0, 2, 4, 6, 8, 10],
            )))

    fig.update_layout(
        width=720, height=400, plot_bgcolor="white",
        showlegend=False, margin=dict(l=10, r=10, t=0, b=10),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
            lataxis=dict(range=[-60, 90])))

    fig.add_annotation(
        text=f"<b>The Economist Democracy Index Map, {year}</b>",
        x=0, y=1.01, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows a world map of the Economist Democracy Index"
             f" in {year}.",
        x=0, y=0.95, showarrow=False, align="left",
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 14})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=0, y=0.002, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 11})

    fig.write_html(f"reports/html/map_index_{year}.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image(f"reports/figures/map_index_{year}.png")


def plot_world_map_index_change(start_year: int, end_year: int) -> None:
    colors = Colors()
    df = get_index_change_geographic_data(start_year, end_year)

    fig = go.Figure(
        data=go.Choropleth(
            locations=df['ISO_A3_EH'], z=df['IndexChange'],
            text=df['Country'],
            colorscale=colors.colorscales["RdWtGr"],
            autocolorscale=False, marker_line_color='white',
            marker_line_width=0.3, zmin=-4, zmax=4,
            hovertemplate="<b>%{text}</b><br>Change: %{z}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgb(0, 0, 0, 0)"),
            colorbar=dict(
                orientation="h", x=0.5, y=0,
                xanchor="center", yanchor="bottom",
                len=1, thickness=5, tickvals=[-4, -3, -2, -1, 0, 1, 2, 3, 4],
            )))

    fig.update_layout(
        width=720, height=400, plot_bgcolor="white",
        showlegend=False, margin=dict(l=10, r=10, t=0, b=10),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
            lataxis=dict(range=[-60, 90])))

    fig.add_annotation(
        text=f"<b>The Economist Democracy Index Variation"
             f" Map, {start_year} - {end_year}</b>",
        x=0, y=1.01, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows a world map of the Economist Democracy Index,"
             f" coloured by the change between<br>{start_year} and"
             f" {end_year}.",
        x=0, y=0.95, showarrow=False, align="left",
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 14})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=0, y=0.002, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 11})

    fig.write_html(f"reports/html/map_index_change_{start_year}"
                   f"_to_{end_year}.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image(f"reports/figures/map_index_change_{start_year}"
                    f"_to_{end_year}.png")


if __name__ == "__main__":
    plot_evolution_regions()
    plot_evolution_countries()
    plot_world_map_index(year=2006)
    plot_world_map_index(year=2023)
    plot_world_map_index(year=2024)
    plot_world_map_index_change(start_year=2006, end_year=2015)
    plot_world_map_index_change(start_year=2006, end_year=2024)
