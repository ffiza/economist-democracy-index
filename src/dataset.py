import pandas as pd


class Data:
    def __init__(self):
        self.df = None
        self._setup_data()

    def _setup_data(self):
        self.df = pd.read_csv("data/raw/economist_democracy.csv")
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
