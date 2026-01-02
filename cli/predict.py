import argparse
import pandas as pd
from ml.model import DummyOPSModel

def load_player(player_id):
    df = pd.read_csv("data/players.csv")
    player = df[df["player_id"] == player_id].iloc[0]
    return player

def load_stats(player_id):
    df = pd.read_csv("data/batter_stats.csv")
    stats = df[df["player_id"] == player_id].sort_values("year")
    return stats

def make_features(stats, birth_year):
    if len(stats) < 3:
        raise ValueError("予測には3年分の成績が必要です")
    s = stats.iloc[-3:]
    latest_year = s.iloc[-1]["year"]
    age = latest_year - birth_year
    features = {
        "age": age,
        "ops_t-1": s.iloc[-1]["ops"],
        "ops_t-2": s.iloc[-2]["ops"],
        "ops_t-3": s.iloc[-3]["ops"],
        "games_t-1": s.iloc[-1]["games"],
        "pa_t-1": s.iloc[-1]["plate_appearances"],
    }
    return pd.DataFrame([features])

def main(player_id):
    player = load_player(player_id)
    stats = load_stats(player_id)
    X = make_features(stats, player["birth_year"])
    model = DummyOPSModel()
    pred_ops = model.predict(X)[0]
    print(f"選手名: {player['name']}")
    print(f"年齢: {X.iloc[0]['age']}")
    print("\n過去成績:")
    for _, row in stats.iterrows():
        print(f"{int(row['year'])} OPS: {row['ops']}")
    print("\n来季予測OPS:", round(pred_ops, 3))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_id", type=int, required=True)
    args = parser.parse_args()
    main(args.player_id)
