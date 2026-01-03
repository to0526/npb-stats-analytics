import pandas as pd

def create_training_data(stats_df, players_df):
    records = []
    merged = stats_df.merge(
        players_df,
        left_on="player_id",
        right_on="player_id"
    )
    for player_id, g in merged.groupby("player_id"):
        g = g.sort_values("year")
        if len(g) < 4:
            continue
        for i in range(3, len(g)):
            row = g.iloc[i]
            prev1 = g.iloc[i - 1]
            prev2 = g.iloc[i - 2]
            prev3 = g.iloc[i - 3]
            age = row["year"] - row["birth_year"]
            records.append({
                "age": age,
                "ops_t-1": prev1["ops"],
                "ops_t-2": prev2["ops"],
                "ops_t-3": prev3["ops"],
                "games_t-1": prev1["games"],
                "pa_t-1": prev1["plate_appearances"],
                "target_ops": row["ops"],
            })
    return pd.DataFrame(records)
