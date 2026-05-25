import requests

url = ("http://localhost:12434/engines/llama.cpp/v1/chat/completions")


user_input = []

while True:
    print("Please enter the rule you wish to analyse: (type 'END' on a new line to finish):")
    while True:
        line = input()
        if line.lower() == "end":
            break
        user_input.append(line)

    joined_input = "\n".join(user_input)


    data = {
        "model": "ai/qwen3-coder",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": f"Analyze this rule:\n\n{joined_input}\n\nExplain to me in detail everything about this rule:"
            }
        ]
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    print(response.json()["choices"][0]["message"]["content"])