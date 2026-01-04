def print_result(result):
    print("================================")
    print(f"選手名: {result.player_name}")
    print(f"年齢: {result.age}（{result.age_group}）\n")

    print("過去のOPS:")
    for _, row in result.past_ops.iterrows():
        print(f"  {int(row['year'])}: {row['ops']:.3f}")

    print(f"\n予測OPS: {result.pred_ops:.3f}")
    print(f"期待度: {result.expectation}")

    print("\nOPS推移が近い選手:")
    for p in result.similar_players:
        print(
            f"  {p['name']} {p['age_range']}歳 "
            f"(OPS推移: {', '.join(f'{x:.3f}' for x in p['ops'])})"
        )
    print("================================")

