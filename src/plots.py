import plotly.graph_objects as go
from plotly.graph_objects import Figure
import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors

from colors import Colors
from data import Data, get_yearly_geographic_data
from data import get_index_change_geographic_data, get_migration_matrix
from config import Config


def plot_evolution_regions() -> None:
    """
    Plots the evolution of the Democracy Index by region from 2006 to 2024.
    """
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
    """
    Plots the evolution of the Democracy Index for selected countries from
    2006 to 2024.
    """
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

    _add_country(fig, "Argentina", (2018, 7.3), colors.BLUE)
    _add_country(fig, "Mali", (2013, 6.2), colors.ORANGE)
    _add_country(fig, "Bhutan", (2022.5, 5.25), colors.GREEN)
    _add_country(fig, "Afghanistan", (2022.5, 0.7), colors.RED)
    _add_country(fig, "Norway", (2018, 9.6), colors.PURPLE)
    _add_country(fig, "Nicaragua", (2023, 1.9), colors.BROWN)

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
                 color: str) -> None:
    """
    Adds a country to the figure with its corresponding data.

    Parameters
    ----------
    fig : Figure
        The Plotly figure instance to add the country to.
    country : str
        The name of the country to add.
    label_pos : tuple
        The x and y coordinates for the label position.
    color : str
        The color for the country line and label.
    """
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
    """
    Plots a world map of the Democracy Index for a given year.

    Parameters
    ----------
    year : int
        The year for which to plot the map.
    """
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
    """
    Plots a world map of the change in the Democracy Index between two years.

    Parameters
    ----------
    start_year : int
        The starting year for the change calculation.
    end_year : int
        The ending year for the change calculation.
    """
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


def plot_regions() -> None:
    """
    Plots a world map of the regions defined in the project.
    """
    df = get_yearly_geographic_data(year=2006)
    colors = Colors()
    config = Config()

    # Define colorscale for regions
    region_mapping = {
        region: i for i, region in enumerate(config.region_colors.keys())}
    df['RegionCode'] = df['Region'].map(region_mapping)
    colorscale = [
        (i / 6, list(config.region_colors.values())[i]) for i in range(7)]

    fig = go.Figure(
        data=go.Choropleth(
            locations=df['ISO_A3_EH'], z=df['RegionCode'], text=df['Country'],
            colorscale=colorscale, customdata=df['Region'],
            marker_line_color='white',
            showscale=False,
            marker_line_width=0.3, zmin=0, zmax=6,
            hovertemplate="<b>%{text}</b><br>Region: "
                          "%{customdata}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgb(0, 0, 0, 0)"),
            ))

    for i, region in enumerate(config.region_colors.keys()):
        fig.add_annotation(
            text="<b>" + region + "</b>",
            x=0, y=0.05 + i * 0.03, showarrow=False,
            xref="paper", yref="paper", xanchor="left", yanchor="middle",
            font={"color": config.region_colors[region], "size": 11})

    fig.update_layout(
        width=720, height=400, plot_bgcolor="white",
        showlegend=False, margin=dict(l=10, r=10, t=0, b=10),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
            lataxis=dict(range=[-60, 90])))

    fig.add_annotation(
        text="<b>World Regions</b>",
        x=0, y=1.01, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows a world map of the different regions.",
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

    fig.write_html("reports/html/map_regions.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image("reports/figures/map_regions.png")


def plot_regime_migration(start_year: int, end_year: int) -> None:
    """
    Plots a heatmap of regime type changes between two years.
    
    Parameters
    ----------
    start_year : int
        The starting year for the reigme change calculation.
    end_year : int
        The ending year for the reigme change calculation.
    """
    colors = Colors()
    m = get_migration_matrix(start_year, end_year)
    column_labels = ["Full<br>Democracies", "Flawed<br>Democracies",
                     "Hybrid<br>Regimes", "Authoritarian<br>Regimes"]
    text_data = np.array([
        [f"Authoritarian regimes in {start_year} that<br>remained"
         f" authoritarian in {end_year}",
         f"Authoritarian regimes in {start_year} that<br>transitioned to"
         f" hybrid regimes by {end_year}",
         f"Authoritarian regimes in {start_year} that<br>transitioned to"
         f" flawed democracies by {end_year}",
         f"Authoritarian regimes in {start_year} that<br>transitioned to full "
         f"democracies by {end_year}",
         f"Total authoritarian regimes in {start_year}"],
        [f"Hybrid regimes in {start_year} that<br>transitioned to"
         f" authoritarian regimes by {end_year}",
         f"Hybrid regimes in {start_year} that<br>remained hybrid in"
         f" {end_year}",
         f"Hybrid regimes in {start_year} that<br>transitioned to flawed "
         f"democracies by {end_year}",
         f"Hybrid regimes in {start_year} that<br>transitioned to full "
         f"democracies by {end_year}",
         f"Total hybrid regimes in {start_year}"],
        [f"Flawed democracies in {start_year} that<br>transitioned to"
         f" authoritarian regimes by {end_year}",
         f"Flawed democracies in {start_year} that<br>transitioned to hybrid "
         f"regimes by {end_year}",
         f"Flawed democracies in {start_year} that<br>remained flawed"
         f" democracies in {end_year}",
         f"Flawed democracies in {start_year} that<br>transitioned to full "
         f"democracies by {end_year}",
         f"Total flawed democracies in {start_year}"],
        [f"Full democracies in {start_year} that<br>transitioned to"
         f" authoritarian regimes by {end_year}",
         f"Full democracies in {start_year} that<br>transitioned to hybrid "
         f"regimes by {end_year}",
         f"Full democracies in {start_year} that<br>transitioned to flawed "
         f"democracies by {end_year}",
         f"Full democracies in {start_year} that<br>remained full democracies "
         f"in {end_year}",
         f"Total full democracies in {start_year}"],
        [f"Total authoritarian regimes in {end_year}",
         f"Total hybrid regimes in {end_year}",
         f"Total flawed democracies in {end_year}",
         f"Total full democracies in {end_year}",
         ""],
    ], dtype=object)

    fig = go.Figure()

    # Draw the heatmap
    fig.add_trace(go.Heatmap(
        z=m, colorscale="viridis", zmin=0, zmax=m[:4, :4].max(),
        text=text_data, showscale=False, hoverinfo="text",
        hoverlabel=dict(
            bgcolor="white", bordercolor=colors.DARK_GRAY,
            font=dict(color=colors.DARK_GRAY)),
        x=np.arange(m.shape[1]), y=np.arange(m.shape[0])[::-1]))

    # Add borders to each square
    num_rows, num_cols = m.shape
    for i in range(num_rows + 1):
        fig.add_shape(type="line", x0=-0.5, x1=num_cols - 0.5, y0=i - 0.5,
                      y1=i - 0.5, line=dict(color="white", width=3))
    for j in range(num_cols + 1):
        fig.add_shape(type="line", x0=j - 0.5, x1=j - 0.5, y0=-0.5,
                      y1=num_rows - 0.5, line=dict(color="white", width=3))

    # Overlay custom colors
    greens = mpl.colormaps.get_cmap("Greens")
    light_green = mcolors.to_hex(greens(0.25))
    medium_green = mcolors.to_hex(greens(0.45))
    dark_green = mcolors.to_hex(greens(0.65))
    reds = mpl.colormaps.get_cmap("Reds")
    light_red = mcolors.to_hex(reds(0.25))
    medium_red = mcolors.to_hex(reds(0.45))
    dark_red = mcolors.to_hex(reds(0.65))
    cmat = [
         ["white",  light_green, medium_green, dark_green, "gainsboro"],
         [light_red, "white", light_green, medium_green, "gainsboro"],
         [medium_red, light_red, "white", light_green, "gainsboro"],
         [dark_red, medium_red, light_red, "white", "gainsboro"],
         ["gainsboro", "gainsboro", "gainsboro", "gainsboro", "white"]]
    for r in range(num_rows):
        for c in range(num_cols):
            fig.add_shape(
                type="rect", x0=c - 0.5, x1=c + 0.5,
                y0=num_rows - r - 1.5, y1=num_rows - r - 0.5,
                fillcolor=cmat[r][c], line=dict(width=3, color="white"))

    # Add annotations for values
    for r in range(num_rows):
        for c in range(num_cols):
            if not np.isnan(m[r, c]):
                fig.add_annotation(
                    x=c, y=num_rows - r - 1, showarrow=False,
                    text="<b>" + str(int(m[r, c])) + "</b>",
                    font=dict(color=colors.DARK_GRAY, size=18))

    # Add labels for columns and rows
    for i, col in enumerate(column_labels):
        fig.add_annotation(
            x=i, y=1, text=column_labels[len(column_labels) - i - 1],
            showarrow=False, yref="paper", xanchor="center", yanchor="bottom",
            textangle=270, align="left",
            font=dict(color=colors.DARK_GRAY, size=14))
        fig.add_annotation(
            x=0.05, y=i + 1, text=col, xref="paper", showarrow=False,
            xanchor="right", yanchor="middle", align="right",
            font=dict(color=colors.DARK_GRAY, size=14))

    fig.add_shape(type="line", x0=-0.228, y0=0.2, x1=-0.228, y1=1,
                  xref="paper", yref="paper",
                  line=dict(color=colors.DARK_GRAY, width=1.3))
    fig.add_shape(type="line", x0=0.07, y0=1.31, x1=0.77, y1=1.31,
                  xref="paper", yref="paper",
                  line=dict(color=colors.DARK_GRAY, width=1.3))
    fig.add_annotation(
        x=0.4, y=1.38, text=f"<b>{end_year}</b>", xref="paper",
        showarrow=False, align="center", yref="paper",
        font=dict(color=colors.DARK_GRAY, size=15))
    fig.add_annotation(
        x=-0.291, y=0.6, text=f"<b>{start_year}</b>", xref="paper",
        showarrow=False, align="center", yref="paper", textangle=270,
        font=dict(color=colors.DARK_GRAY, size=15))

    fig.add_annotation(
        text=f"<b>Changes in Regime Types, {start_year} - {end_year}</b>",
        x=-0.42, y=1.5, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 20})
    fig.add_annotation(
        text="This chart shows the change in regime types between"
             f" {start_year} and {end_year}.",
        x=-0.42, y=1.425, showarrow=False, align="left",
        xref="paper", yref="paper", xanchor="left", yanchor="middle",
        font={"color": colors.DARK_GRAY, "size": 14})
    fig.add_annotation(
        text="<b>Source(s):</b> "
        + "<a href='https://en.wikipedia.org/wiki/The_Economist"
        + "_Democracy_Index'>The Economist/Wikipedia</a>",
        x=-0.42, y=0, showarrow=False,
        xref="paper", yref="paper", xanchor="left", yanchor="top",
        font={"color": colors.DARK_GRAY, "size": 11})

    fig.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   scaleanchor="y"),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   scaleanchor="x"),
        width=500, height=500,
        plot_bgcolor="white",
        margin=dict(l=150, r=8, t=170, b=25),
    )

    fig.write_html("reports/html/regime_migration.html",
                   full_html=False, include_plotlyjs='cdn')
    fig.write_image("reports/figures/regime_migration.png")


if __name__ == "__main__":
    # plot_evolution_regions()
    # plot_evolution_countries()
    # plot_world_map_index(year=2006)
    # plot_world_map_index(year=2024)
    # plot_world_map_index_change(start_year=2006, end_year=2015)
    # plot_world_map_index_change(start_year=2006, end_year=2024)
    # plot_world_map_index_change(start_year=2020, end_year=2024)
    # plot_regions()
    plot_regime_migration(start_year=2006, end_year=2024)
