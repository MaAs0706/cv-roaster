import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="CV Roaster", page_icon="🔥", layout="centered")

st.title("🔥 CV Roaster")
st.write("Upload your resume and get brutally honest feedback")

uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "txt"])

roast = st.button("Roast my CV", use_container_width=True)

if roast:
    if not uploaded_file:
        st.error("Upload your CV first!")
    else:
        with st.spinner("Roasting..."):
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    cv_text = ""
                    for page in pdf.pages:
                        cv_text += page.extract_text()
            else:
                cv_text = uploaded_file.read().decode("utf-8")

            model = genai.GenerativeModel("gemini-1.5-flash-8b")
            response = model.generate_content(
                f"""You are a brutally honest senior tech recruiter with 20 years of experience. 
                Roast the given resume — be funny, harsh, and specific about what's weak. 
                But end with 3 genuine actionable improvements.
                
                Resume:
                {cv_text}"""
            )
            st.markdown(response.text)