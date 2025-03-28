import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from colors import Colors
from dataset import Data

plt.style.use("./styles/line.mplstyle")


def plot_evolution_regions():
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

    region_df = data.get_region_averages()
    for i, region in enumerate(region_df["Region"].unique()):
        region_data = region_df[region_df["Region"] == region]
        ax.plot(region_data["Year"], region_data["DemocracyIndex"],
                color=colors.PALETTE[i])
    ax.text(s="Asia and Australasia", x=2018.5, y=5.85,
            va="center", ha="center", color=colors.PALETTE[0], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="Central and Eastern Europe", x=2017.5, y=5.15,
            va="center", ha="center", color=colors.PALETTE[1], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="Latin America and the Caribbean", x=2014, y=6.6,
            va="center", ha="center", color=colors.PALETTE[2], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="Middle East and North Africa", x=2017, y=3.3,
            va="center", ha="center", color=colors.PALETTE[3], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="North America", x=2019, y=8.75,
            va="center", ha="center", color=colors.PALETTE[4], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="Sub-Saharan Africa", x=2008, y=4.5,
            va="center", ha="center", color=colors.PALETTE[5], weight=600,
            path_effects=[pe.withStroke(
                linewidth=1.5, foreground="w")])
    ax.text(s="Western Europe", x=2011, y=8.2,
            va="center", ha="center", color=colors.PALETTE[6], weight=600,
            path_effects=[pe.withStroke(
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

    _add_country(ax, "Argentina", (2018, 7.25), colors.PALETTE[0])
    _add_country(ax, "United States", (2021, 7.6), colors.PALETTE[1])
    _add_country(ax, "Ireland", (2022, 9.4), colors.PALETTE[2])
    _add_country(ax, "Canada", (2011, 9.3), colors.PALETTE[3])
    _add_country(ax, "Norway", (2018, 9.6), colors.PALETTE[4])

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


if __name__ == "__main__":
    plot_evolution_regions()
    plot_evolution_countries()
