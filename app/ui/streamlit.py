import streamlit as st
import requests

st.set_page_config(page_title="Resume Screening App", page_icon="📄", layout="wide")
st.title("Resume Screening App")
st.caption("Upload a job description and a candidate resume to compare them.")

job_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="job_description")
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")

if job_file is not None or resume_file is not None:
    if job_file is not None:
        st.success(f"Job description uploaded: {job_file.name}")
    if resume_file is not None:
        st.success(f"Resume uploaded: {resume_file.name}")

    if st.button("Analyze Resume", use_container_width=True):
        if job_file is None or resume_file is None:
            st.warning("Please upload both a job description PDF and a resume PDF.")
        else:
            try:
                files = {
                    "job_description": (job_file.name, job_file.getvalue(), "application/pdf"),
                    "resume": (resume_file.name, resume_file.getvalue(), "application/pdf"),
                }
                with st.spinner("Processing the resume and matching it with the job requirements..."):
                    response = requests.post(
                        "http://127.0.0.1:8002/screening/",
                        files=files,
                        timeout=120,
                    )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("error"):
                        st.error(data["error"])
                    else:
                        st.success(f"Candidate status: {data.get('candidate_status', 'Unknown')}")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Skill match", f"{data.get('skill_match_percentage', 0)}%")
                            st.write("Reason:", data.get("reason", "Not available"))
                        with col2:
                            st.write("Matched skills:", data.get("matched_skills") or ["None"])
                            st.write("Missing skills:", data.get("missing_skills") or ["None"])

                        with st.expander("Candidate details"):
                            st.json(data.get("resume", {}))

                        with st.expander("Job description details"):
                            st.json(data.get("jd", {}))
                else:
                    st.error(f"Error processing resume: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(
                    "Could not connect to the backend at http://127.0.0.1:8002. "
                    "Start it with: python -m uvicorn app.main:app --host 127.0.0.1 --port 8002"
                )
                st.code(str(e))
else:
    st.info("Upload both a job description PDF and a resume PDF to begin the screening process.")

