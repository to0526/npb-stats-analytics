import pandas as pd

def build_features(stats_df: pd.DataFrame, players_df: pd.DataFrame) -> pd.DataFrame:
    df = stats_df.merge(players_df, on="player_id", how="left")
    # 年齢
    df["age"] = df["year"] - df["birth_year"]
    # OPSラグ
    for lag in [1, 2, 3]:
        df[f"ops_t-{lag}"] = df.groupby("player_id")["ops"].shift(lag)
    # 試合数・打席数（直前年）
    df["games_t-1"] = df.groupby("player_id")["games"].shift(1)
    df["pa_t-1"] = df.groupby("player_id")["plate_appearances"].shift(1)
    # 目的変数（翌年OPS）
    df["target_ops"] = df.groupby("player_id")["ops"].shift(-1)
    return df
