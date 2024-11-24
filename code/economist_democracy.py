from colors import Colors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
plt.style.use("./styles/line.mplstyle")


class DemocracyData:
    def __init__(self):
        self.df = None
        self._setup_data()

    def _setup_data(self):
        self.df = pd.read_csv("data/economist_democracy.csv")
        self.df.drop(columns=["2023 rank"], inplace=True)
        self.df["Region"] = self.df["Region"].astype("category")
        self.df["RegimeType"] = self.df["RegimeType"].astype("category")

        self.df = self.df.melt(
            id_vars=["Region", "Country", "RegimeType"],
            var_name="Year",
            value_name="DemocracyIndex"
        )
        self.df["Year"] = self.df["Year"].astype(int)

    def filter_by_region(self, regions: list[str]) -> pd.DataFrame:
        return self._filter("Region", regions)

    def filter_by_country(self, countries: list[str]) -> pd.DataFrame:
        return self._filter("Country", countries)

    def filter_by_regime(self, regimes: list[str]) -> pd.DataFrame:
        return self._filter("RegimeType", regimes)

    def _filter(self, key: str, values: list[str]) -> pd.DataFrame:
        return self.df[self.df[key].isin(values)]

    def get_world_average(self):
        return self.df.groupby("Year")[
            "DemocracyIndex"].mean().reset_index(name="DemocracyIndex")

    def get_region_averages(self):
        return self.df.groupby(
            ["Region", "Year"], observed=True)[
                "DemocracyIndex"].mean().reset_index(
                    name="DemocracyIndex")


class DemocracyFigures:
    def __init__(self, data: DemocracyData):
        self.data = data

    def plot_evolution_regions(self):
        colors = Colors()
        fig, ax = plt.subplots()

        ax.set_ylim(0, 10)
        ax.set_xlim(2006, 2023)
        ax.set_xticks([year for year in range(2007, 2024, 2)])
        ax.set_yticks([i for i in range(11)])

        for country in self.data.df["Country"].unique():
            country_data = self.data.df[self.data.df["Country"] == country]
            ax.plot(country_data["Year"], country_data["DemocracyIndex"],
                    color=colors.BACKGROUND_LINE, lw=0.25, alpha=0.5)

        world_df = self.data.get_world_average()
        ax.plot(world_df["Year"], world_df["DemocracyIndex"],
                color=colors.LINE, ls="--", zorder=15)

        region_df = self.data.get_region_averages()
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
        ax.text(s="World", x=2010, y=5.25,
                va="center", ha="center", color=colors.BLACK, weight=600,
                path_effects=[pe.withStroke(
                    linewidth=1.5, foreground="w")])

        self._add_texts(ax)

        fig.tight_layout()
        fig.savefig("images/economist_democracy/regions.png")

    def plot_evolution_countries(self):
        colors = Colors()
        fig, ax = plt.subplots()

        ax.set_ylim(0, 10)
        ax.set_xlim(2006, 2023)
        ax.set_xticks([year for year in range(2007, 2024, 2)])
        ax.set_yticks([i for i in range(11)])

        for country in self.data.df["Country"].unique():
            country_data = self.data.df[self.data.df["Country"] == country]
            ax.plot(country_data["Year"], country_data["DemocracyIndex"],
                    color=colors.BACKGROUND_LINE, lw=0.25, alpha=0.5)

        world_df = self.data.get_world_average()
        ax.plot(world_df["Year"], world_df["DemocracyIndex"],
                color=colors.BLACK)

        self._add_country(ax, "Argentina", (2018, 7.25), colors.PALETTE[0])
        self._add_country(ax, "United States", (2021, 7.6), colors.PALETTE[1])
        self._add_country(ax, "Ireland", (2022, 9.4), colors.PALETTE[2])
        self._add_country(ax, "Canada", (2011, 9.3), colors.PALETTE[3])
        self._add_country(ax, "Norway", (2018, 9.6), colors.PALETTE[4])

        ax.text(s="World", x=2010, y=5.2, va="center", ha="center",
                color="#f1f3f5", weight=600)

        self._add_texts(ax)

        fig.tight_layout()
        fig.savefig("images/economist_democracy/countries.png")

    def _add_country(self, ax: plt.Axes, country: str, text_pos: tuple,
                     color: str):
        country_data = self.data.df[self.data.df["Country"] == country]
        ax.plot(country_data["Year"], country_data["DemocracyIndex"],
                color=color)
        ax.text(s=country, x=text_pos[0], y=text_pos[1], va="center",
                ha="center", color=color, weight=600,
                path_effects=[pe.withStroke(linewidth=1.5, foreground="w")])

    def _add_texts(self, ax: plt.Axes):
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


if __name__ == "__main__":
    data = DemocracyData()
    figures = DemocracyFigures(data)
    figures.plot_evolution_regions()
    figures.plot_evolution_countries()
