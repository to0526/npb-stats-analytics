import argparse
import pandas as pd
import joblib

from usecase.predict_ops import predict_ops
from presentation.console import print_result
from presentation.llm_payload import build_llm_payload
from llm.explain import explain_prediction
from utils.spinner import Spinner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_id", type=int, required=True)
    args = parser.parse_args()

    stats_df = pd.read_csv("data/batter_stats.csv")
    players_df = pd.read_csv("data/players.csv")
    model = joblib.load("models/linear_ops.pkl")

    result = predict_ops(
        player_id=args.player_id,
        stats_df=stats_df,
        players_df=players_df,
        model=model,
    )

    print_result(result)

    spinner = Spinner("AIが分析中")
    spinner.start()

    comment = explain_prediction(**build_llm_payload(result))

    spinner.stop()
    print("\nAIコメント:")
    print(comment)


if __name__ == "__main__":
    main()

