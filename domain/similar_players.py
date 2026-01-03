import numpy as np

def ops_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def find_similar_players_by_age_window(
    target_player_id: int,
    stats_df,
    players_df,
    n_years: int = 3,
    top_k: int = 3,
):
    # 年齢付きOPSを作る
    def age_ops(player_id):
        birth_year = players_df.loc[
            players_df["player_id"] == player_id, "birth_year"
        ].values[0]
        df = (
            stats_df[stats_df["player_id"] == player_id]
            .sort_values("year")
            .assign(age=lambda x: x["year"] - birth_year)
        )
        return df[["age", "ops"]]
    # ターゲット
    target_df = age_ops(target_player_id).tail(n_years)
    target_ops = target_df["ops"].tolist()
    target_ages = target_df["age"].tolist()
    results = []
    for pid in stats_df["player_id"].unique():
        if pid == target_player_id:
            continue
        df = age_ops(pid)
        # 年齢スライドウィンドウ
        for start_age in df["age"].unique():
            window = df[df["age"].between(start_age, start_age + n_years - 1)]
            if len(window) != n_years:
                continue
            ops = window["ops"].tolist()
            dist = ops_distance(target_ops, ops)
            name = players_df.loc[
                players_df["player_id"] == pid, "name"
            ].values[0]
            results.append({
                "player_id": pid,
                "name": name,
                "age_range": f"{start_age}–{start_age + n_years - 1}",
                "ops": ops,
                "distance": dist,
            })
    results.sort(key=lambda x: x["distance"])
    return results[:top_k]
