import streamlit as st
import json

# Load predefined keywords per role
with open("sample_keywords.json", "r") as f:
    role_keywords = json.load(f)

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📋 Resume Analyzer Ai")

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

        # Resume Match Score
        score = int((len(found_keywords) / len(role_keywords[job_role])) * 100)
        st.metric("📊 Resume Match Score", f"{score}%")

        st.write("🟢 Found Keywords:", ", ".join(found_keywords) or "None")
        st.write("🔴 Missing Keywords:", ", ".join(missing_keywords) or "None")

        if len(found_keywords) < len(role_keywords[job_role]) // 2:
            st.info("💡 Tip: Consider tailoring your resume more for this role.")

        # Feedback section
        st.subheader("💬 Share Your Feedback")
        user_feedback = st.text_area("What do you think about the suggestions?", height=100)

        if st.button("Submit Feedback"):
            if user_feedback.strip():
                st.success("✅ Thank you! Your feedback has been noted.")
                # For demo: Print feedback to console (can write to file or db)
                print("User Feedback:", user_feedback)
            else:
                st.warning("⚠️ Please enter some feedback before submitting.")

        # Google Form link for extended feedback
        st.markdown("\n---\n")
        st.markdown("[🔗 Fill Google Feedback Form](https://forms.gle/your-form-id) for detailed feedback and suggestions!")
