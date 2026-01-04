def build_llm_payload(result):
    similar_players_text = "\n".join(
        f"- {p['name']}: OPS {p['ops']}"
        for p in result.similar_players
    )

    return dict(
        player_name=result.player_name,
        age=result.age,
        age_group=result.age_group,
        expectation=result.expectation,
        past_ops=result.past_ops.to_string(index=False),
        similar_players=similar_players_text,
        pred_ops=result.pred_ops,
    )

