from openai import OpenAI

client = OpenAI()

def explain_prediction(player_name, age, age_group, expectation, past_ops, pred_ops):
    prompt = f"""
あなたはプロ野球のデータ分析アナリストです。

選手名: {player_name}
年齢: {age}
過去のOPS:
{past_ops}

来季予測OPS: {pred_ops:.3f}

この選手の来季の期待値を、野球ファン向けに分かりやすく説明してください。
"""
    # res = client.responses.create(
    #     model="gpt-4.1-mini",
    #     input=prompt
    # )
    # return res.output_text
    return prompt
