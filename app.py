import streamlit as st
import http.client
import json

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")
st.title("📋 Resume Analyzer AI")

# --- Session State ---
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# --- OTP Section (only if not logged in) ---
if not st.session_state.is_logged_in:
    st.subheader("🔐 Login with OTP")

    phone_number = st.text_input("Enter Phone Number", "")
    otp_code = st.text_input("Enter OTP (after sending)", "")

    if st.button("Send OTP"):
        try:
            conn = http.client.HTTPSConnection("api.corpus.swecha.org")
            payload = json.dumps({"phone_number": phone_number})
            headers = {"content-type": "application/json"}
            conn.request("POST", "/api/v1/auth/login/send-otp", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            st.write("📩 Response:", data)
        except Exception as e:
            st.error(f"⚠️ Error sending OTP: {e}")

    if st.button("Verify OTP"):
        try:
            conn = http.client.HTTPSConnection("api.corpus.swecha.org")
            payload = json.dumps({"phone_number": phone_number, "otp_code": otp_code})
            headers = {"content-type": "application/json"}
            conn.request("POST", "/api/v1/auth/login/verify-otp", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            st.write("✅ Verification Response:", data)

            # Parse JSON response
            result = json.loads(data)
            if "access_token" in result:
                st.session_state.is_logged_in = True
                st.session_state.access_token = result["access_token"]
                st.session_state.user_id = result.get("user_id")
                st.success("🎉 Logged in successfully! Now you can use Resume Analyzer.")
            else:
                st.error("❌ OTP verification failed. Try again.")
        except Exception as e:
            st.error(f"⚠️ Error verifying OTP: {e}")

# --- Resume Analyzer Section (only if logged in) ---
if st.session_state.is_logged_in:
    st.subheader("📄 Resume Analyzer")

    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.is_logged_in = False
        st.session_state.access_token = None
        st.session_state.user_id = None
        st.info("You have been logged out.")

    else:
        # Load keywords JSON
        try:
            with open("sample_keywords.json", "r") as f:
                role_keywords = json.load(f)
        except FileNotFoundError:
            st.error("⚠️ sample_keywords.json not found. Please add it.")
            role_keywords = {}

        if role_keywords:
            resume_text = st.text_area("Paste your resume content or bullet points:", height=250)
            job_role = st.selectbox("Target Job Role:", list(role_keywords.keys()))

            if st.button("Analyze Resume"):
                if not resume_text.strip():
                    st.warning("⚠️ Please paste your resume content.")
                else:
                    found_keywords = [kw for kw in role_keywords[job_role] if kw.lower() in resume_text.lower()]
                    missing_keywords = [kw for kw in role_keywords[job_role] if kw.lower() not in resume_text.lower()]

                    st.success(
                        f"✅ Keywords found for {job_role}: {len(found_keywords)} / {len(role_keywords[job_role])}"
                    )

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
                            print("User Feedback:", user_feedback)  # (Optional: save to DB/file)
                        else:
                            st.warning("⚠️ Please enter some feedback before submitting.")

                    st.markdown("\n---\n")
                    st.markdown("[🔗 Fill Google Feedback Form](https://forms.gle/your-form-id)")
