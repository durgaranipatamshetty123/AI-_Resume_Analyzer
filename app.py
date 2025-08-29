import streamlit as st
import pdfplumber
import re

# ✅ If using OpenAI for suggestions (make sure to install and set API key!)
# from openai import OpenAI
# client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="AI Resume Analyzer")

# ----------------------------
# Functions
# ----------------------------

def extract_text_from_pdf(file):
    """Extract text from uploaded PDF."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def calculate_match(resume_text, jd_text):
    """Calculate match percentage between resume and JD."""
    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    common_words = resume_words.intersection(jd_words)
    if not jd_words:
        return 0
    return round(len(common_words) / len(jd_words) * 100, 2)

def suggest_skills(resume_text, jd_text):
    """Suggest missing skills based on JD."""
    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    missing = jd_words - resume_words
    # Pick only skill-like words (basic filter)
    skills = [w for w in missing if len(w) > 2]
    return skills[:10]  # return top 10

def ai_suggestions(resume_text):
    """Mock AI suggestions (can be replaced with OpenAI API)."""
    suggestions = []
    if "sql" not in resume_text.lower():
        suggestions.append("🔹 Highlight any SQL experience you have.")
    if "project" not in resume_text.lower():
        suggestions.append("🔹 Add more details about your projects.")
    if "python" not in resume_text.lower():
        suggestions.append("🔹 Mention your Python programming skills.")
    if not suggestions:
        suggestions.append("✅ Your resume looks strong! Just tailor it to the job description.")
    return suggestions

# ----------------------------
# Streamlit UI
# ----------------------------

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume (PDF only) and a Job Description to get an ATS-style analysis.")

# Resume Upload
uploaded_resume = st.file_uploader("Upload your Resume", type=["pdf"])

# JD Upload
uploaded_jd = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])

# ----------------------------
# Processing
# ----------------------------
if uploaded_resume is not None:
    st.success("✅ Resume uploaded successfully!")
    resume_text = extract_text_from_pdf(uploaded_resume)

    if resume_text:
        st.subheader("📄 Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=250)

        # If JD is also uploaded
        if uploaded_jd is not None:
            if uploaded_jd.name.endswith(".pdf"):
                jd_text = extract_text_from_pdf(uploaded_jd)
            else:
                jd_text = uploaded_jd.read().decode("utf-8")

            st.subheader("📑 Job Description")
            st.text_area("JD Content", jd_text, height=200)

            # Match Percentage
            match_score = calculate_match(resume_text, jd_text)
            st.metric("Match Percentage", f"{match_score}%")

            # Suggested Skills
            missing_skills = suggest_skills(resume_text, jd_text)
            if missing_skills:
                st.subheader("🛠 Suggested Skills to Add")
                st.write(", ".join(missing_skills))
            else:
                st.success("✅ Your resume already covers most skills!")

        # AI Suggestions
        st.subheader("🤖 AI Suggestions")
        suggestions = ai_suggestions(resume_text)
        for s in suggestions:
            st.write(s)
    else:
        st.error("⚠️ Could not extract text from the PDF.")
