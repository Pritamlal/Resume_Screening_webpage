from fastapi import FastAPI, File, UploadFile  # pyright: ignore[reportMissingImports]

from app.agents.candidate_evaluation import evaluate_candidate
from app.agents.jd_extractor import analyze_jd
from app.agents.resume_extractor import extract_resume_data
from app.parsepdf import parse_pdf

app = FastAPI()


@app.post("/screening/")
async def screening(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
):
    try:
        print("INFO: Starting resume screening...")
        print(f"INFO: Received resume file: {resume.filename}")
        print(f"INFO: Received JD file: {job_description.filename}")

        resume_text = parse_pdf(resume.file)
        print("INFO: Resume PDF parsed successfully.")
        resume_details_extracted = extract_resume_data(resume_text)
        print("INFO: Resume extraction completed.")

        jd_text = parse_pdf(job_description.file)
        print("INFO: Job description PDF parsed successfully.")
        jd_extracted = analyze_jd(jd_text)
        print("INFO: JD analysis completed.")
        evaluation = evaluate_candidate(resume_details_extracted, jd_extracted)
        print(f"INFO: Candidate status: {evaluation['candidate_status']}")

        return {
            "resume": resume_details_extracted,
            "jd": jd_extracted,
            "candidate_status": evaluation["candidate_status"],
            "reason": evaluation["reason"],
            "skill_match_percentage": evaluation["skill_match_percentage"],
            "matched_skills": evaluation["matched_skills"],
            "missing_skills": evaluation["missing_skills"],
        }
    except Exception as exc:
        print(f"ERROR: Screening failed: {str(exc)}")
        return {"error": str(exc)}