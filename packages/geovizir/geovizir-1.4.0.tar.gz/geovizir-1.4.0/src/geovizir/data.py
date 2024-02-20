import wbgapi as wb
import datetime
import pandas as pd

# Fix for Python >= 3.10 until wbdata is updated
import collections
collections.Sequence = collections.abc.Sequence

def get_data(indicator: str, year: int) -> pd.DataFrame:
    """Get data from the World Bank API

    Parameters
    ----------
    indicator : str
        Indicator code
    year : int
        Year

    Returns
    -------
    pandas.DataFrame
        Dataframe with the data
    """
    data = wb.data.DataFrame(indicator, "all", year, labels=True)
    data.reset_index(inplace=True)
    data.rename(columns={indicator: "value", "Country": "country", "economy": "iso3c"}, inplace=True)
    data["date"] = year
    data["indicator"] = indicator

    return data