import streamlit as st
import json

# Load predefined keywords per role
with open("sample_keywords.json", "r") as f:
    role_keywords = json.load(f)

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📋 Resume Analyzer (No API)")

st.write("Paste your resume content or bullet points:")

resume_text = st.text_area("Your Resume Text", height=250)
job_role = st.selectbox("Target Job Role:", list(role_keywords.keys()))

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠️ Please paste your resume content.")
    else:
        found_keywords = []
        missing_keywords = []

        for kw in role_keywords[job_role]:
            if kw.lower() in resume_text.lower():
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

        st.success(f"✅ Keywords found for {job_role}: {len(found_keywords)} / {len(role_keywords[job_role])}")
        st.write("🟢 Found Keywords:", ", ".join(found_keywords) or "None")
        st.write("🔴 Missing Keywords:", ", ".join(missing_keywords) or "None")

        if len(found_keywords) < len(role_keywords[job_role]) // 2:
            st.info("💡 Tip: Consider tailoring your resume more for this role.")
