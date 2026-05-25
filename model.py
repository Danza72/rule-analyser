import requests


def analyze_rule(rule_str):
    url = ("http://localhost:12434/engines/llama.cpp/v1/chat/completions")
    data = {
        "model": "ai/qwen3-coder",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": f"Analyze this rule:\n\n{rule_str}\n\n"
                    "Explain to me in detail everything about this rule:"
            }
        ]
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]