# Resume_Screening_webpage
Resumescreening is for shortlisting the candidate's resume by comparing their respective resume with job description

Project Description 
This project is a resume screening application that helps compare a candidate’s resume against a job description and decide whether the person is a good fit for the role. The app uses a Streamlit web interface where the user uploads a job description PDF and a resume PDF, and then a FastAPI backend processes both files. It extracts text from the PDFs, sends the text to a Groq-powered LLM, and asks the model to convert the unstructured data into clean JSON fields such as name, email, skills, experience, and required qualifications. After that, the application compares the resume data with the job description data, calculates the skill match percentage, and returns a candidate status such as shortlisted, review, or not shortlisted. In short, the project demonstrates how AI can be used for intelligent document parsing and automated hiring screening in a simple web application.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload  
