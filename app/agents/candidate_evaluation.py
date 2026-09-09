import json
import re


def _as_dict(payload):
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        stripped = payload.strip()
        if not stripped:
            return {}
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
            if not match:
                return {}
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _as_int(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        match = re.search(r"-?\d+(?:\.\d+)?", value)
        if match:
            return int(float(match.group(0)))
    return None


def _as_skill_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        if not value.strip():
            return []
        return [part.strip() for part in re.split(r"[,;]|\n", value) if part.strip()]
    if isinstance(value, (list, tuple, set)):
        skills = []
        for item in value:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    skills.append(cleaned)
        return skills
    return []


def evaluate_candidate(resume, jd):
    resume_data = _as_dict(resume)
    jd_data = _as_dict(jd)

    candidate_experience = _as_int(
        resume_data.get("work_experience", resume_data.get("experience", resume_data.get("years_of_experience")))
    )
    jd_min_experience = _as_int(jd_data.get("min_work_experience"))
    jd_max_experience = _as_int(jd_data.get("max_work_experience"))

    resume_skills = _as_skill_list(resume_data.get("skills", []))
    jd_skills = _as_skill_list(jd_data.get("skills", []))

    resume_lookup = {skill.lower(): skill for skill in resume_skills}
    matched_skills = []
    for skill in jd_skills:
        normalized = skill.lower()
        if normalized in resume_lookup:
            matched_skills.append(resume_lookup[normalized])

    missing_skills = []
    for skill in jd_skills:
        if skill.lower() not in {item.lower() for item in resume_skills}:
            missing_skills.append(skill)

    if jd_skills:
        skill_match_percentage = round((len(matched_skills) / len(jd_skills)) * 100)
    else:
        skill_match_percentage = 0

    experience_ok = True
    if jd_min_experience is not None and candidate_experience is not None:
        experience_ok = candidate_experience >= jd_min_experience
    if jd_max_experience is not None and candidate_experience is not None:
        experience_ok = experience_ok and candidate_experience <= jd_max_experience

    if not jd_skills and candidate_experience is None:
        candidate_status = "Requires review"
        reason = "No job skill requirements or candidate experience were detected."
    elif not experience_ok:
        candidate_status = "Not shortlisted"
        reason = (
            f"Candidate experience ({candidate_experience} years) does not meet the job requirement "
            f"range of {jd_min_experience if jd_min_experience is not None else 'N/A'} to "
            f"{jd_max_experience if jd_max_experience is not None else 'N/A'} years."
        )
    elif skill_match_percentage >= 60:
        candidate_status = "Shortlisted"
        reason = (
            f"Strong skill alignment: {len(matched_skills)} of {len(jd_skills)} required skills match, "
            f"with {candidate_experience} years of experience."
        )
    elif skill_match_percentage >= 40:
        candidate_status = "Review"
        reason = (
            f"Partial match for the role. Candidate matches {len(matched_skills)} of {len(jd_skills)} required skills "
            f"and has {candidate_experience} years of experience."
        )
    else:
        candidate_status = "Not shortlisted"
        reason = (
            f"Skill match is low ({skill_match_percentage}%). Candidate matches {len(matched_skills)} of "
            f"{len(jd_skills)} required skills."
        )

    return {
        "candidate_status": candidate_status,
        "reason": reason,
        "skill_match_percentage": skill_match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "candidate_experience": candidate_experience,
        "required_experience": {
            "min": jd_min_experience,
            "max": jd_max_experience,
        },
    }
