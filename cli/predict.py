import argparse
import pandas as pd
import joblib

from features.builder import build_features
from constants import FEATURE_COLS
from llm.explain import explain_prediction
from domain.age_category import calc_age, age_category
from domain.expectation import expectation_star
from utils.spinner import Spinner
from domain.similar_players import find_similar_players_by_age_window

def load_player_info(player_id: int):
    players_df = pd.read_csv("data/players.csv")
    row = players_df[players_df["player_id"] == player_id]
    if row.empty:
        return None
    return {
        "name": row.iloc[0]["name"],
        "birth_year": row.iloc[0]["birth_year"],
    }

def load_past_ops(player_id: int, n_years: int = 3):
    stats_df = pd.read_csv("data/batter_stats.csv")
    df = (
        stats_df[stats_df["player_id"] == player_id]
        .sort_values("year")
        .tail(n_years)
    )
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
    birth_year = player_info["birth_year"]
    latest_year = int(latest_row["year"])
    age = calc_age(birth_year, latest_year)
    age_group = age_category(age)
    expectation = expectation_star(pred_ops)
    similar_players = find_similar_players_by_age_window(
        target_player_id=args.player_id,
        stats_df=stats_df,
        players_df=players_df,
    )
    print("================================")
    if player_info:
        print(f"選手名: {player_info['name']}")
        print(f"年齢: {age}（{age_group}）")
    print()
    print("過去のOPS:")
    for _, row in past_ops_df.iterrows():
        print(f"  {int(row['year'])}: {row['ops']:.3f}")
    print()
    print(f"予測OPS: {pred_ops:.3f}")
    print(f"期待度: {expectation}")
    print("\nOPS推移が近い選手:")
    for p in similar_players:
        print(
            f"  {p['name']} "
            f"  {p['age_range']}歳"
            f"(OPS推移: {', '.join(f'{x:.3f}' for x in p['ops'])})"
        )
    print("================================")
    # スピナー開始
    spinner = Spinner("AIが分析中")
    spinner.start()
    similar_players_text = "\n".join(
        f"- {p['name']}: OPS {p['ops']}"
        for p in similar_players
    )
    comment = explain_prediction(
        player_name=player_info["name"],
        age=age,
        age_group=age_group,
        expectation=expectation,
        past_ops=past_ops_df.to_string(index=False),
        similar_players=similar_players_text,
        pred_ops=pred_ops,
    )
    # スピナー停止
    spinner.stop()
    print("\nAIコメント:")
    print(comment)

if __name__ == "__main__":
    main()
