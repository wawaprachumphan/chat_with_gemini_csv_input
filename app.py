import streamlit as st
import pandas as pd
import google.generativeai as genai

# ใช้ secrets ของ Streamlit
genai.configure(api_key=st.secrets["GENAI_API_KEY"])

st.set_page_config(page_title="CSV Q&A with Gemini", layout="wide")
st.title("ถามคำถามจากไฟล์ CSV ด้วย Gemini")

uploaded_file = st.file_uploader("📁 อัปโหลดไฟล์ CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 ข้อมูลในไฟล์")
    st.dataframe(df)

    question = st.text_input("❓ พิมพ์คำถามของคุณที่เกี่ยวข้องกับข้อมูลในตาราง")

    if question:
        with st.spinner("กำลังคิด..."):
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
ข้อมูล CSV:
{df.head(20).to_csv(index=False)}

คำถาม:
{question}

ช่วยตอบคำถามนี้โดยอ้างอิงจากข้อมูลในตารางด้านบน
"""

            response = model.generate_content(prompt)
            st.subheader("💬 คำตอบจาก Gemini")
            st.write(response.text)
