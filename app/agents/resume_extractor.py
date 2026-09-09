import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

from app.prompts import RESUME_EXTRACTION_PROMPT

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


def _parse_resume_response(content):
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
        return {"error": "Resume model returned invalid JSON.", "raw_response": cleaned}


def extract_resume_text(resume_data):
    print("INFO: Extracting resume details...")
    prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=resume_data)
    print("INFO: Sending resume to AI model...")
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts relevant information from resumes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1200,
    )
    content = response.choices[0].message.content
    print("INFO: Response from AI model received.")
    if content:
        print(content[:500])
    return _parse_resume_response(content)


# Backward-compatible alias used by app.main
def extract_resume_data(resume_data):
    return extract_resume_text(resume_data)
