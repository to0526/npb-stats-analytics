import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from features.builder import build_features
from constants import FEATURE_COLS, TARGET_COL

def main():
    stats_df = pd.read_csv("data/batter_stats.csv")
    players_df = pd.read_csv("data/players.csv")
    feature_df = build_features(stats_df, players_df)
    train_df = feature_df.dropna(subset=FEATURE_COLS + [TARGET_COL])
    X = train_df[FEATURE_COLS]
    y = train_df[TARGET_COL]
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "models/linear_ops.pkl")
    print("model trained")
    print("features:", FEATURE_COLS)

if __name__ == "__main__":
    main()
