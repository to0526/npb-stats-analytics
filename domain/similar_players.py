import numpy as np
import pandas as pd

def find_similar_players(
    target_player_id: int,
    stats_df: pd.DataFrame,
    players_df: pd.DataFrame,
    n_years: int = 3,
    top_k: int = 3,
):
    # OPS履歴を作る
    def ops_history(player_id):
        df = (
            stats_df[stats_df["player_id"] == player_id]
            .sort_values("year")
            .tail(n_years)
        )
        if len(df) < n_years:
            return None
        return df["ops"].tolist()
    target_ops = ops_history(target_player_id)
    if target_ops is None:
        return []
    results = []
    for pid in stats_df["player_id"].unique():
        if pid == target_player_id:
            continue
        ops = ops_history(pid)
        if ops is None:
            continue
        dist = np.linalg.norm(
            np.array(target_ops) - np.array(ops)
        )
        name = players_df.loc[
            players_df["player_id"] == pid, "name"
        ].values[0]
        results.append({
            "player_id": pid,
            "name": name,
            "distance": dist,
            "ops": ops,
        })
    results.sort(key=lambda x: x["distance"])
    return results[:top_k]
