import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="CV Roaster", page_icon="🔥", layout="centered")

st.title("🔥 CV Roaster")
st.write("Paste your resume and get brutally honest feedback")

cv_text = st.text_area("Paste your CV here", height=300, placeholder="Paste your resume text here...")

roast = st.button("Roast my CV", use_container_width=True)

if roast:
    if not cv_text:
        st.error("Paste your CV first!")
    else:
        with st.spinner("Roasting..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a brutally honest senior tech recruiter with 20 years of experience. Roast the given resume — be funny, harsh, and specific about what's weak. But end with 3 genuine actionable improvements."
                    },
                    {
                        "role": "user",
                        "content": f"Roast this resume:\n\n{cv_text}"
                    }
                ]
            )
            st.markdown(response.choices[0].message.content)