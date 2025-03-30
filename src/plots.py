import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from colors import Colors
from dataset import Data, get_yearly_geographic_data
from dataset import get_index_change_geographic_data
from config import Config

plt.style.use("./styles/line.mplstyle")


def plot_evolution_regions():
    data = Data()
    config = Config()

    fig, ax = plt.subplots()

    ax.set_ylim(0, 10)
    ax.set_xlim(2006, 2023)
    ax.set_xticks([year for year in range(2007, 2024, 2)])
    ax.set_yticks([i for i in range(11)])

    for country in data.df["Country"].unique():
        country_data = data.df[data.df["Country"] == country]
        ax.plot(
            country_data["Year"], country_data["DemocracyIndex"], lw=0.25,
            color=config.region_bg_colors[country_data["Region"].values[0]])

    regions = data.df["Region"].unique()
    regions_xpos = dict(zip(regions,
                            [2019, 2011, 2017.5, 2014, 2018.5, 2017, 2008]))
    regions_ypos = dict(zip(regions,
                            [8.75, 8.2, 5.15, 6.6, 5.85, 3.3, 4.5]))
    region_df = data.get_region_averages()
    for region in regions:
        region_data = region_df[region_df["Region"] == region]
        ax.plot(region_data["Year"], region_data["DemocracyIndex"],
                color=config.region_colors[region])
        ax.text(s=region, x=regions_xpos[region], y=regions_ypos[region],
                va="center", ha="center", color=config.region_colors[region],
                weight=600, path_effects=[pe.withStroke(
                    linewidth=1.5, foreground="w")])

    _add_texts(ax)

    fig.tight_layout()
    fig.savefig("reports/figures/time_series_by_region.png")


def plot_evolution_countries():
    data = Data()
    colors = Colors()
    fig, ax = plt.subplots()

    ax.set_ylim(0, 10)
    ax.set_xlim(2006, 2023)
    ax.set_xticks([year for year in range(2007, 2024, 2)])
    ax.set_yticks([i for i in range(11)])

    for country in data.df["Country"].unique():
        country_data = data.df[data.df["Country"] == country]
        ax.plot(country_data["Year"], country_data["DemocracyIndex"],
                color=colors.BACKGROUND_LINE, lw=0.25, alpha=0.5)

    _add_country(ax, "Argentina", (2018, 7.25), colors.BLUE)
    _add_country(ax, "United States", (2021, 7.6), colors.ORANGE)
    _add_country(ax, "Ireland", (2022, 9.4), colors.GREEN)
    _add_country(ax, "Canada", (2011, 9.3), colors.RED)
    _add_country(ax, "Norway", (2018, 9.6), colors.PURPLE)

    ax.text(s="World", x=2010, y=5.2, va="center", ha="center",
            color="#f1f3f5", weight=600)

    _add_texts(ax)

    fig.tight_layout()
    fig.savefig("reports/figures/time_series_by_country.png")


def _add_texts(ax: plt.Axes):
    ax.text(
        s="The Economist Democracy Index, 2006 to 2023",
        x=-0.05, y=1.25, weight=600, ha="left", va="top", size=10,
        transform=ax.transAxes)
    ax.text(
        s="The Democracy Index published by the Economist Group is an"
        + " index measuring the quality of democracy across the world.",
        x=-0.05, y=1.18, ha="left", va="top", size=5.5,
        transform=ax.transAxes)
    ax.text(
        s="This quantitative and comparative assessment is centrally"
        + " concerned with democratic rights and democratic institutions.",
        x=-0.05, y=1.14, ha="left", va="top", size=5.5,
        transform=ax.transAxes)
    ax.text(
        s="The index is based on 60"
        + " indicators grouped into five categories, measuring pluralism,"
        + " civil liberties, and political culture.",
        x=-0.05, y=1.10, ha="left", va="top", size=5.5,
        transform=ax.transAxes)
    ax.text(
        s="Source(s):",
        x=-0.05, y=-0.12, weight=600, ha="left", va="top", size=4,
        transform=ax.transAxes)
    ax.text(
        s="The Economist/Wikipedia "
        + "(https://en.wikipedia.org/wiki/The_Economist_Democracy_Index)",
        x=0.01, y=-0.12, ha="left", va="top", size=4,
        transform=ax.transAxes)
    ax.text(
        s="LESS DEMOCRATIC",
        x=0.005, y=0.01, weight=600, ha="left", va="bottom", size=4,
        transform=ax.transAxes, path_effects=[pe.withStroke(
            linewidth=1.5, foreground="w")])
    ax.text(
        s="MORE DEMOCRATIC",
        x=0.005, y=0.99, weight=600, ha="left", va="top", size=4,
        transform=ax.transAxes, path_effects=[pe.withStroke(
            linewidth=1.5, foreground="w")])


def _add_country(ax: plt.Axes, country: str, text_pos: tuple,
                 color: str):
    data = Data()
    country_data = data.df[data.df["Country"] == country]
    ax.plot(country_data["Year"], country_data["DemocracyIndex"],
            color=color)
    ax.text(s=country, x=text_pos[0], y=text_pos[1], va="center",
            ha="center", color=color, weight=600,
            path_effects=[pe.withStroke(linewidth=1.5, foreground="w")])


def plot_world_map_index():
    df = get_yearly_geographic_data(year=2023)

    fig, ax = plt.subplots()

    ax.set_xlim(-180, 180)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["bottom"].set_visible(False)

    df.plot(column="DemocracyIndex", ax=ax, edgecolor="white",
            linewidth=0.1, vmin=0, vmax=10, legend=True, cmap="viridis",
            legend_kwds={"location": "bottom", "aspect": 80, "pad": 0.03})

    cbar = ax.get_figure().axes[-1]
    cbar.xaxis.set_ticks_position('top')
    cbar.xaxis.set_label_position('top')
    cbar.tick_params(axis="x", length=0, labelsize=5, pad=2)
    for spine in cbar.spines.values():
        spine.set_visible(False)

    ax.text(
        s="The Economist Democracy Index Map, 2023",
        x=0, y=1.075, weight=600, ha="left", va="top", size=12,
        transform=ax.transAxes)
    ax.text(
        s="Source(s):",
        x=0, y=-0.1, weight=600, ha="left", va="top", size=4,
        transform=ax.transAxes)
    ax.text(
        s="The Economist/Wikipedia "
        + "(https://en.wikipedia.org/wiki/The_Economist_Democracy_Index)",
        x=0.06, y=-0.1, ha="left", va="top", size=4,
        transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig("reports/figures/map_index_2023.png")


def plot_world_map_index_change(start_year: int, end_year: int) -> None:
    colors = Colors()

    df = get_index_change_geographic_data(start_year, end_year)

    fig, ax = plt.subplots()

    ax.set_xlim(-180, 180)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["bottom"].set_visible(False)

    df.plot(column="IndexChange", ax=ax, edgecolor="white",
            linewidth=0.1, vmin=-4, vmax=4, legend=True,
            cmap=colors.colormaps["RdWtGr"],
            legend_kwds={"location": "bottom", "aspect": 80, "pad": 0.03})

    cbar = ax.get_figure().axes[-1]
    cbar.xaxis.set_ticks_position('top')
    cbar.xaxis.set_label_position('top')
    cbar.tick_params(axis="x", length=0, labelsize=5, pad=2)
    for spine in cbar.spines.values():
        spine.set_visible(False)

    ax.text(
        s="Change in the Economist Democracy Index, "
          f"{start_year} - {end_year}",
        x=0, y=1.075, weight=600, ha="left", va="top", size=12,
        transform=ax.transAxes)
    ax.text(
        s="Source(s):",
        x=0, y=-0.1, weight=600, ha="left", va="top", size=4,
        transform=ax.transAxes)
    ax.text(
        s="The Economist/Wikipedia "
        + "(https://en.wikipedia.org/wiki/The_Economist_Democracy_Index)",
        x=0.06, y=-0.1, ha="left", va="top", size=4,
        transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig("reports/figures/map_index_change_"
                f"{start_year}_to_{end_year}.png")


if __name__ == "__main__":
    plot_evolution_regions()
    plot_evolution_countries()
    plot_world_map_index()
    plot_world_map_index_change(start_year=2006, end_year=2023)
    plot_world_map_index_change(start_year=2006, end_year=2015)
