"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"



def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())

    # Start measuring response time
    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=MODEL,
        contents=question
    )

    # Calculate response time
    elapsed_time = time.perf_counter() - start_time

    # Get token usage
    usage = response.usage_metadata

    print(f"Response time: {elapsed_time:.2f} seconds")
    print(f"Input tokens: {usage.prompt_token_count}")
    print(f"Output tokens: {usage.candidates_token_count}")

    return response.text



def chat_loop() -> None:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print("Chat started! Type 'exit' to quit.")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Chat ended.")
            break

        if not question:
            continue

        response = chat.send_message(question)
        print(f"Gemini: {response.text}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--chat", action="store_true")

    args = parser.parse_args()

    if args.chat:
        chat_loop()
        return

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
