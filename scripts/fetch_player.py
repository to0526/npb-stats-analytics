import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PLAYERS_CSV = DATA_DIR / "players.csv"
STATS_CSV = DATA_DIR / "batter_stats.csv"
TEAM_URLS = {
    "G": "https://npb.jp/bis/teams/rst_g.html",  # 巨人
    "T": "https://npb.jp/bis/teams/rst_t.html",  # 阪神
    "D": "https://npb.jp/bis/teams/rst_d.html",  # 中日
    "C": "https://npb.jp/bis/teams/rst_c.html",  # 広島
    "DB": "https://npb.jp/bis/teams/rst_db.html",  # DeNA
    "S": "https://npb.jp/bis/teams/rst_s.html",  # ヤクルト
    "H": "https://npb.jp/bis/teams/rst_h.html",  # ソフトバンク
    "F": "https://npb.jp/bis/teams/rst_f.html",  # 日本ハム
    "M": "https://npb.jp/bis/teams/rst_m.html",  # ロッテ
    "E": "https://npb.jp/bis/teams/rst_e.html",  # 楽天
    "L": "https://npb.jp/bis/teams/rst_l.html",  # 西武
    "B": "https://npb.jp/bis/teams/rst_b.html",  # オリックス
}

def fetch_team_batters(team_url: str) -> list[str]:
    res = requests.get(team_url, headers={"User-Agent": "Mozilla/5.0"})
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    player_urls = []
    for tr in soup.select("table tr"):
        tds = tr.select("td")
        if len(tds) < 4:
            continue
        position = tds[3].text.strip()
        if position == "投手":
            continue  # 投手を除外
        a = tds[1].select_one("a")
        if not a:
            continue
        href = a.get("href")
        if href and href.startswith("/bis/players/"):
            player_urls.append("https://npb.jp" + href)
    return player_urls

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
        label = th.text.strip()
        value = td.text.strip()
        if label == "ポジション":
            if value == "投手":
                print(f"skip pitcher: {name} ({player_id})")
                return
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

def load_existing_player_ids() -> set[str]:
    if not PLAYERS_CSV.exists():
        return set()
    df = pd.read_csv(PLAYERS_CSV)
    return set(df["player_id"].astype(str))

if __name__ == "__main__":
    existing_ids = load_existing_player_ids()
    for team, team_url in TEAM_URLS.items():
        print(f"\n=== {team} ===")
        player_urls = fetch_team_batters(team_url)
        for url in player_urls:
            player_id = url.rstrip("/").split("/")[-1].split(".")[0]
            if player_id in existing_ids:
                print(f"skip existing: {player_id}")
                continue
            print(f"fetching {url}")
            fetch_player(url)
            existing_ids.add(player_id)  # メモリ上でも更新
            time.sleep(5)
