from dataclasses import dataclass
import pandas as pd

from features.builder import build_features
from constants import FEATURE_COLS
from domain.age_category import calc_age, age_category
from domain.expectation import expectation_star
from domain.similar_players import find_similar_players_by_age_window


@dataclass
class PredictionResult:
    player_name: str
    age: int
    age_group: str
    past_ops: pd.DataFrame
    pred_ops: float
    expectation: str
    similar_players: list


def predict_ops(
    player_id: int,
    stats_df: pd.DataFrame,
    players_df: pd.DataFrame,
    model,
) -> PredictionResult:
    feature_df = build_features(stats_df, players_df)
    player_df = feature_df[feature_df["player_id"] == player_id].sort_values("year")
    latest_row = player_df.iloc[-1]

    X_pred = latest_row[FEATURE_COLS].to_frame().T
    pred_ops = model.predict(X_pred)[0]

    player_row = players_df[players_df["player_id"] == player_id].iloc[0]
    birth_year = player_row["birth_year"]
    latest_year = int(latest_row["year"])

    age = calc_age(birth_year, latest_year)

    return PredictionResult(
        player_name=player_row["name"],
        age=age,
        age_group=age_category(age),
        past_ops=(
            stats_df[stats_df["player_id"] == player_id]
            .sort_values("year")
            .tail(3)[["year", "ops"]]
        ),
        pred_ops=pred_ops,
        expectation=expectation_star(pred_ops),
        similar_players=find_similar_players_by_age_window(
            target_player_id=player_id,
            stats_df=stats_df,
            players_df=players_df,
        ),
    )
