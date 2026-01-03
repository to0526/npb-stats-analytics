import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from ml.features import create_training_data
from ml.model import create_model

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

def main():
    stats_df = pd.read_csv(DATA_DIR / "batter_stats.csv")
    players_df = pd.read_csv(DATA_DIR / "players.csv")

    print("stats_df:", stats_df.shape)
    print(stats_df.head())
    print("players_df:", players_df.shape)
    print(players_df.head())


    train_df = create_training_data(stats_df, players_df)

    if train_df.empty:
        raise RuntimeError("学習データが作れませんでした")

    X = train_df.drop(columns=["target_ops"])
    y = train_df["target_ops"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = create_model()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)

    print(f"Training records: {len(train_df)}")
    print(f"MAE: {mae:.4f}")

    joblib.dump(model, "models/ops_model.pkl")
    print("Model saved to models/ops_model.pkl")


if __name__ == "__main__":
    main()

