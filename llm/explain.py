import subprocess
from typing import Optional

def explain_prediction(
    player_name: str,
    age: int,
    age_group: str,
    past_ops: str,
    pred_ops: float,
    expectation: str,
    model_name: str = "llama3",
    timeout: int = 60,
) -> str:
    """
    Llama3 (via Ollama) を使って予測結果の説明文を生成する
    """
    prompt = f"""
以下はプロ野球選手の打撃成績予測です。

選手名: {player_name}
年齢: {age}歳（{age_group}）
過去のOPS:
{past_ops}

予測OPS: {pred_ops:.3f}
期待度: {expectation}

この情報をもとに、
・野球ファン向け
・前向きだが過度に煽らない
・100文字前後
・日本語
でコメントを生成してください。
"""
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        return result.stdout.strip()
    except Exception as e:
        # LLM失敗時のフォールバック
        return (
            f"{player_name}は近年安定した成績を残しており、"
            f"次シーズンもOPS {pred_ops:.3f}前後が期待されます。"
            f"（LLM生成失敗: {e}）"
        )
