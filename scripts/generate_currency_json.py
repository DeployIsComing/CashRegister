# The core idea of this script is to access an external free AI tool to generate different
# JSONs files for any other country.
import json
from pathlib import Path
import requests
from prompt import get_prompt


# Simple, free AI tool service
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY= ""


def ai_generator(currency_code: str) -> dict | list:
    # Starting the json generation
    prompt: str = get_prompt(currency_code)

    payload = {
        "model": "llama-3.3-70b-versatile",  # modelo bom e rápido
        "messages": [
            {
                "role": "system",
                "content": "You are a precise JSON generator. Always respond with pure valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    # String sanitization
    if content.startswith("```"):
        content = content.strip("`").replace("json\n", "", 1).strip()

    return json.loads(content)


def get_country_currency(currency_code: str) -> dict | list:

    # A few protection
    if len(currency_code) != 3:
        raise Exception(f"Invalid currency code {currency_code}")

    file_name: str = f"{currency_code}.json"
    folder_path: str = f"config/i18n/currencies"
    path: Path = Path(folder_path) / file_name

    # File already exists no need re-generate and waste AI tokens
    if path.exists():
        print(f"File {file_name} already exists, loading...")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # generating
    print(f"File {file_name} does not exist. Generating using AI support...")
    data = ai_generator(currency_code)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n\n✅ New currency code saved at: {path}")
    return data


if __name__ == "__main__":
    print("==================================")
    print("--- AI CURRENCY JSON GENERATOR ---")
    print("==================================")

    if GROQ_API_KEY == "":
        print("First time running this script?")
        print("Please go to: https://console.groq.com create a free account.")
        print("Then go to: api keys and generate a free key and inform here: GROQ_API_KEY")
        raise Exception("No API key provided")
    else:
        currency_code = input("Enter 3-digit currency code: ")
        currency_data = get_country_currency(currency_code)
        print(json.dumps(currency_data, indent=2, ensure_ascii=False))
        print("\n\nPowered by Groq 2026 (c)")
