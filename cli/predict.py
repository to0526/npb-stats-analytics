import argparse
import pandas as pd
import joblib

from features.builder import build_features
from constants import FEATURE_COLS
from llm.explain import explain_prediction

def load_player_info(player_id: int):
    players_df = pd.read_csv("data/players.csv")
    row = players_df[players_df["player_id"] == player_id]
    if row.empty:
        return None
    return {
        "name": row.iloc[0]["name"],
        "birth_year": row.iloc[0]["birth_year"],
    }

def load_past_ops(player_id: int):
    stats_df = pd.read_csv("data/batter_stats.csv")
    df = stats_df[stats_df["player_id"] == player_id] \
        .sort_values("year")
    return df[["year", "ops"]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_id", type=int, required=True)
    args = parser.parse_args()
    stats_df = pd.read_csv("data/batter_stats.csv")
    players_df = pd.read_csv("data/players.csv")
    feature_df = build_features(stats_df, players_df)
    player_df = feature_df[
        feature_df["player_id"] == args.player_id
    ].sort_values("year")
    latest_row = player_df.iloc[-1]
    X_pred = latest_row[FEATURE_COLS].to_frame().T
    model = joblib.load("models/linear_ops.pkl")
    pred_ops = model.predict(X_pred)[0]
    player_info = load_player_info(args.player_id)
    past_ops_df = load_past_ops(args.player_id)
    print("================================")
    if player_info:
        print(f"選手名: {player_info['name']}")
    print()
    print("過去のOPS:")
    for _, row in past_ops_df.iterrows():
        print(f"  {int(row['year'])}: {row['ops']:.3f}")
    print()
    print(f"予測OPS: {pred_ops:.3f}")
    print("================================")
    comment = explain_prediction(
        player_name=player_info["name"],
        age=int(latest_row["age"]),
        past_ops=past_ops_df.to_string(index=False),
        pred_ops=pred_ops,
    )
    print("\nAIコメント:")
    print(comment)

if __name__ == "__main__":
    main()
