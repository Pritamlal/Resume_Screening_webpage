import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

from app.prompts import EXTRACT_JD_DETAILS

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)


def _clean_json_text(content):
    if not isinstance(content, str):
        return content

    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _parse_jd_response(content):
    cleaned = _clean_json_text(content)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return {"error": "JD model returned invalid JSON.", "raw_response": cleaned}


def analyze_jd(text: str):
    """Analyze the extracted job description text and return a structured JSON payload."""
    print("INFO: Extracting job description details...")
    prompt = EXTRACT_JD_DETAILS.format(jd_text=text)
    try:
        print("INFO: Sending JD text to AI model...")
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are an expert in extracting structured job description requirements."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1000,
        )
        content = response.choices[0].message.content
        print("INFO: JD response received from AI model.")
        if content:
            print(content[:500])
        return _parse_jd_response(content)
    except Exception as e:
        print(f"ERROR: Failed to analyze JD: {str(e)}")
        return {"error": str(e)}