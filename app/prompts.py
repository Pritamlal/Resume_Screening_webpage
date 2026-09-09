RESUME_EXTRACTION_PROMPT = """
You are an expert in resume screening. Your task is to extract relevant details from a resume.
-name (string)
-email (string)
-phone (string)
-education (strings or null)
-work experience (integer or null)
-skills (list of strings)
-certifications (list of strings)

Your response should be in JSON format with the following structure.
Use 'null' if a value is missing or not applicable.

Here is the resume text:
{resume_text}

Expected response format:
{{
    "name": "Pritam",
    "email": "abc@gmail.com",
    "phone": "string",
    "education": "Bachelor of Science",
    "work_experience": 9,
    "skills": ["Python", "FastAPI", "JavaScript"],
    "certifications": ["Certified Python Developer", "AWS Certified Solutions Architect"]
}}
"""

# Backward-compatible alias for older code
EXTRACT_CANDIDATE_DETAILS = RESUME_EXTRACTION_PROMPT

EXTRACT_JD_DETAILS = """
You are an expert in filtering the required skills and experience from a given job description. Your task is to extract relevant details from a job description.
- required skills (list of strings
You will receive a job description in text format and you need to identify key information such as : 
- min_work_experience in years (integer or null)
- max_work_experience in years (integer or null)
- skills (list of strings)

your response must be in valid JSON object.
use 'null' if a value is missing or not applicable.
if experience is not available as a range for example "5+ years consider it as 5 fot min_work_experience and 8 for max_work_experience (assuming 3 years of flexibility) and if only one value is given for example "5 years" consider it as 5 for min_work_experience and 8 for max_work_experience (assuming 3 years of flexibility)

Here is the job description text:
{jd_text}

Expected response format:
{{
    "min_work_experience": 5,
    "max_work_experience": 8,
    "skills": ["Python", "FastAPI", "JavaScript"]
}}

"""