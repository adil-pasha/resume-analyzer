import streamlit as st
import http.client
import json

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📋 Resume Analyzer Ai")

# --- OTP Section ---
st.subheader("🔐 Login with OTP")

phone_number = st.text_input("Enter Phone Number", "")
otp_code = st.text_input("Enter OTP (after sending)", "")

if st.button("Send OTP"):
    conn = http.client.HTTPSConnection("api.corpus.swecha.org")
    payload = json.dumps({"phone_number": phone_number})
    headers = {'content-type': "application/json"}
    conn.request("POST", "/api/v1/auth/login/send-otp", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    st.write("📩 Response:", data)

if st.button("Verify OTP"):
    conn = http.client.HTTPSConnection("api.corpus.swecha.org")
    payload = json.dumps({"phone_number": phone_number, "otp_code": otp_code})
    headers = {'content-type': "application/json"}
    conn.request("POST", "/api/v1/auth/login/verify-otp", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    st.write("✅ Verification Response:", data)


# --- Resume Analyzer Section ---
st.subheader("📄 Resume Analyzer")

with open("sample_keywords.json", "r") as f:
    role_keywords = json.load(f)

resume_text = st.text_area("Paste your resume content or bullet points:", height=250)
job_role = st.selectbox("Target Job Role:", list(role_keywords.keys()))

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠️ Please paste your resume content.")
    else:
        found_keywords = [kw for kw in role_keywords[job_role] if kw.lower() in resume_text.lower()]
        missing_keywords = [kw for kw in role_keywords[job_role] if kw.lower() not in resume_text.lower()]

        st.success(f"✅ Keywords found for {job_role}: {len(found_keywords)} / {len(role_keywords[job_role])}")

        score = int((len(found_keywords) / len(role_keywords[job_role])) * 100)
        st.metric("📊 Resume Match Score", f"{score}%")

        st.write("🟢 Found Keywords:", ", ".join(found_keywords) or "None")
        st.write("🔴 Missing Keywords:", ", ".join(missing_keywords) or "None")

        if len(found_keywords) < len(role_keywords[job_role]) // 2:
            st.info("💡 Tip: Consider tailoring your resume more for this role.")

        st.subheader("💬 Share Your Feedback")
        user_feedback = st.text_area("What do you think about the suggestions?", height=100)

        if st.button("Submit Feedback"):
            if user_feedback.strip():
                st.success("✅ Thank you! Your feedback has been noted.")
                print("User Feedback:", user_feedback)
            else:
                st.warning("⚠️ Please enter some feedback before submitting.")

        st.markdown("\n---\n")
        st.markdown("[🔗 Fill Google Feedback Form](https://forms.gle/your-form-id)")
