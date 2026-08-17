# Prompt to generate the JSON file

def get_prompt(currency_code: str) -> str:
    return f"""Generate a JSON object for the currency {currency_code} following this exact structure:

    {{
      "code": "{currency_code}",
      "symbol": "correct currency symbol",
      "currency_units": [
        {{ "name": "unit name", "plural": "plural form", "value": "1.00" }},
        {{ "name": "subunit name", "plural": "plural form", "value": "0.xx" }}
      ]
    }}

    Requirements:
    - Use the official currency code and the correct symbol for {currency_code}.
    - Include the main currency unit and the most common subunits (like cents, centavos, etc.).
    - All values must be strings with exactly 2 decimal places.
    - Keep the same key names and structure as the example.
    - Respond with ONLY the valid JSON. No explanations, no markdown, no extra text.
    """
