import requests
from config import GEMINI_API_KEY, GEMINI_URL

def ask_gemini_raw(command: str) -> str:
    if not GEMINI_API_KEY:
        return RuntimeError("GEMINI_API_KEY is not set")

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {
        "contents": [
            {"parts": [{"text": f"Answer briefly and conversationally, in 2-3 sentences, "
                                  f"since this will be read aloud: {command}"}]}
        ]
    }
    response = requests.post(GEMINI_URL, headers=headers, params=params, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()