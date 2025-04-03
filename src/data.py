import pandas as pd
import geopandas as gpd
import numpy as np


class Data:
    def __init__(self):
        self.df = None
        self._setup_data()

    def _setup_data(self):
        self.df = pd.read_csv("data/raw/democracy_index.csv")
        self.df = self.df[self.df.columns.drop(
            list(self.df.filter(regex=' rank')))]
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

    def filter_by_year(self, year: int) -> pd.DataFrame:
        return self.df[self.df["Year"] == year]

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


def get_merged_dataframe() -> pd.DataFrame:
    data = Data().df
    countries = gpd.read_file(
        "data/external/ne_110m_admin_0_countries/"
        "ne_110m_admin_0_countries.shp")

    # Use names in `data`
    to_replace = [
        "Bosnia and Herz.", "Côte d'Ivoire", "United States of America",
        "Central African Rep.", "Eq. Guinea", "Congo", "eSwatini",
        "Czechia", "Dominican Rep.", "Dem. Rep. Congo", "Timor-Leste",
        "Greenland", "Falkland Is."]
    value = [
        "Bosnia and Herzegovina", "Ivory Coast", "United States",
        "Central African Republic", "Equatorial Guinea",
        "Republic of the Congo", "Eswatini", "Czech Republic",
        "Dominican Republic", "Democratic Republic of the Congo",
        "East Timor", "Denmark", "Argentina"]
    countries.replace(to_replace=to_replace, value=value, inplace=True)

    merged_df = countries.merge(data, left_on="NAME", right_on="Country",
                                how="left")

    return merged_df


def get_yearly_data(year: int) -> pd.DataFrame:
    df = Data().df
    df = df[df["Year"] == year]

    # Remap regime types to this year
    df["RegimeType"] = df["DemocracyIndex"].apply(assign_regime_type)

    return df


def get_yearly_geographic_data(year: int) -> pd.DataFrame:
    df = get_merged_dataframe()
    df = df[df["NAME"] != "Antarctica"]
    df = df[df["Year"] == year]

    # Remap regime types to this year
    df["RegimeType"] = df["DemocracyIndex"].apply(assign_regime_type)

    return df


def assign_regime_type(democracy_index: float) -> str:
    regime_type = "Authoritarian"
    if democracy_index >= 8.0:
        regime_type = "Full democracy"
    elif democracy_index >= 6.0:
        regime_type = "Flawed democracy"
    elif democracy_index >= 4.0:
        regime_type = "Hybrid regime"
    return regime_type


def get_index_change_geographic_data(start_year: int,
                                     end_year: int) -> pd.DataFrame:
    df = get_merged_dataframe()
    df = df[df["NAME"] != "Antarctica"]
    index_change = df[df["Year"] == end_year]["DemocracyIndex"].to_numpy() \
        - df[df["Year"] == start_year]["DemocracyIndex"].to_numpy()
    df = df[df["Year"] == end_year]
    df["IndexChange"] = index_change
    return df


def get_migration_matrix(start_year: int, end_year: int) -> np.ndarray:
    df1 = get_yearly_data(start_year)
    df2 = get_yearly_data(end_year)

    regimes = ["Authoritarian", "Hybrid regime",
               "Flawed democracy", "Full democracy"]
    n_regimes = len(regimes)

    m = np.zeros((n_regimes + 1, n_regimes + 1))
    for i, r1 in enumerate(regimes):
        for j, r2 in enumerate(regimes):
            m[i, j] = ((df1["RegimeType"].to_numpy() == r1)
                       & (df2["RegimeType"].to_numpy() == r2)).sum()
    m[-1, -1] = np.nan
    m[-1, :n_regimes] = np.sum(m[:n_regimes, :n_regimes], axis=0)
    m[:n_regimes, -1] = np.sum(m[:n_regimes, :n_regimes], axis=1)
    return m
