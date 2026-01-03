import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PLAYERS_CSV = DATA_DIR / "players.csv"
STATS_CSV = DATA_DIR / "batter_stats.csv"

def fetch_player(url: str):
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    # player_id（URLから）
    player_id = url.rstrip("/").split("/")[-1].split(".")[0]
    # 選手名
    name = soup.select_one("li#pc_v_name").text.strip()
    # 生年（例：2002年）
    birth_year = None
    for tr in soup.select("table tr"):
        th = tr.find("th")
        td = tr.find("td")
        if not th or not td:
            continue
        if th.text.strip() == "生年月日":
            # 例: 2001年12月25日
            birth_year = int(td.text.strip()[:4])
            break
    # players.csv 追記
    players_df = pd.DataFrame([{
        "player_id": player_id,
        "name": name,
        "birth_year": str(birth_year),
    }])
    append_csv(PLAYERS_CSV, players_df, key="player_id")
    # 打撃成績テーブル
    rows = []
    table = soup.select_one("table#tablefix_b")
    for tr in table.select("tbody tr"):
        tds = [td.text.strip() for td in tr.select("td")]
        if not tds or not tds[0].isdigit():
            continue
        rows.append({
            "player_id": player_id,
            "year": int(tds[0]),
            "games": int(tds[2]),
            "plate_appearances": int(tds[3]),
            "ops": float(tds[21]) + float(tds[22]),
        })
    stats_df = pd.DataFrame(rows)
    append_csv(STATS_CSV, stats_df, keys=["player_id", "year"])

def append_csv(path: Path, df: pd.DataFrame, key=None, keys=None):
    if path.exists():
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True)
        if key:
            df = df.drop_duplicates(subset=[key])
        if keys:
            df = df.drop_duplicates(subset=keys)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    url = input("NPB選手ページURLを入力してください: ").strip()
    fetch_player(url)
    time.sleep(5)

