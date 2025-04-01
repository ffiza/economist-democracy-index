import pandas as pd
import wikipedia as wp


def get_raw_data():
    html = wp.page("The_Economist_Democracy_Index").html().encode("UTF-8")

    try:
        df = pd.read_html(html)[5]
    except IndexError:
        raise ValueError("The expected table was not found on the Wikipedia.")

    df.rename(columns={"Regime type": "RegimeType"}, inplace=True)
    df.to_csv("data/raw/democracy_index.csv", index=False)


if __name__ == "__main__":
    get_raw_data()
