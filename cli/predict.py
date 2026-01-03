import argparse
import pandas as pd
import joblib

from features.builder import build_features
from constants import FEATURE_COLS

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
    print(f"Predicted OPS: {pred_ops:.3f}")

if __name__ == "__main__":
    main()
