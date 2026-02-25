from bs4 import BeautifulSoup
import pandas as pd 
import requests, json
from functions import clean_name


def scrape_table_1(url: str) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup (page.text, "lxml")
    table = soup.find("table", id = "reportable")
    thead = table.find("thead")
    th_tags = thead.find_all("th")
    titles = [th.text.strip().replace("\xa0"," ") for th in th_tags]
    tbody = table.find("tbody")
    rows_html = tbody.find_all("tr")
    all_rows = []
    for row in rows_html:
        row_data = row.find_all('td')   # ← find_all
        individual_row_data = [data.text.strip() for data in row_data]
        all_rows.append(individual_row_data)
    df = pd.DataFrame(all_rows, columns=titles)
    df = df.loc[:, df.columns != ""]
    df["Player"] = df["Player"].str.replace("\xa0", " ", regex=False)
    df["Player"] = df["Player"].apply(clean_name)
    return df

def scrape_table_2(url: str) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url,headers = headers)
    soup = BeautifulSoup(page.text,"lxml")
    script = soup.find("script", {"data-for": "player-stats-table", "type": "application/json"})
    payload = json.loads(script.string) 
    data_dict = payload["x"]["tag"]["attribs"]["data"]
    df = pd.DataFrame(data_dict)
    cols_to_keep = [
        "Player","Surface","Matches",
        "Wins","Losses","WinPercentage","Titles",
        "EloServe","EloReturn","PointsWonPercentage","GamesWonPercentage",
        "SetsWonPercentage","DecSets","DecSetWins","DecSetWinPercentage",
        "TieBreaks","TieBreaksWon","FirstServePercentage","FirstServeWonPercentage",
        "SecondServeWonPercentage","ServicePointsWonPercentage","ServiceGamesWonPercentage",
        "AcePercentage","DoubleFaultPercentage","FirstServeReturnPointsWonPercentage",
        "SecondServeReturnPointsWonPercentage","AceAgainstPercentage","BreakPointsConvertedPercentage",
    ]
    df = df[cols_to_keep]
    df["Player"] = df["Player"].apply(clean_name)
    return df
