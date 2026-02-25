import pandas as pd 
from bs4.filter import SoupStrainer 
import re

# This function is implemented to make sure the names are exact in both DataFrames
def clean_name(name: str) -> str:
    name = str(name).replace("Â", "").replace("\xa0", " ")
    name = name.lower().replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()
    return name

def filter_by_surface(df:pd.DataFrame, surface: str) -> pd.DataFrame:
    filtered_df = df[df["Surface"] == surface]
    filtered_df = filtered_df.loc[:, df.columns != "Surface"]
    return filtered_df

def get_player_row (df:pd.DataFrame,name:str)->pd.Series | None :
    key = clean_name(name)
    row = df[df["Player"] == key ]
    if row.empty:
        return None
    return row.iloc[0]
