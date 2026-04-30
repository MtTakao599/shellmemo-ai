from openai import OpenAI
import re

client = OpenAI()

def gpt_generate(query):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Linuxコマンドを1つだけ出力。説明・コードブロック・記号は不要。"
            },
            {"role": "user", "content": query}
        ],
    )

    text = res.choices[0].message.content.strip()

    # 🔥 コードブロック除去
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "")

    # 🔥 バッククォート除去
    text = text.replace("`", "")

    return text.strip()
