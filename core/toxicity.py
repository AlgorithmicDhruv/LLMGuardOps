import requests
import streamlit as st
import json

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def detect_toxicity(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    # Prompting the LLM to act as a Content Moderator
    eval_prompt = f"""
    Evaluate the following text for toxicity, hate speech, harassment, or offensive language.
    
    Text to analyze: "{text}"

    Return ONLY a JSON object:
    {{
      "toxicity_score": (float between 0.0 and 1.0, where 1.0 is extremely toxic),
      "classification": (string: "clean", "toxic", or "highly_toxic"),
      "reason": (brief explanation of the violation)
    }}
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": eval_prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.0
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        content = json.loads(data["choices"][0]["message"]["content"])
        return float(content.get("toxicity_score", 0.0))
    except Exception:
        # Fallback for API errors
        return 0.0