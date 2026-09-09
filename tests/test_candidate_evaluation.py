from app.agents.candidate_evaluation import evaluate_candidate


def test_evaluate_candidate_shortlists_match():
    resume = {
        "work_experience": 4,
        "skills": ["Python", "FastAPI", "PostgreSQL"],
    }
    jd = {
        "min_work_experience": 3,
        "max_work_experience": 7,
        "skills": ["Python", "FastAPI", "SQL", "Docker"],
    }

    result = evaluate_candidate(resume, jd)

    assert result["candidate_status"] == "Shortlisted"
    assert result["skill_match_percentage"] >= 50
    assert "Python" in result["matched_skills"]
