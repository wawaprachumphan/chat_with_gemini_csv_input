import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="CSV Chatbot", layout="centered")
st.title("🤖 Chat with Your CSV")

# Section 1: Upload Main Dataset
st.header("📂 Section 1: Upload Main Dataset (CSV)")
main_csv = st.file_uploader("Upload your main CSV file", type="csv", key="main_csv")

# Section 2: Upload Data Dictionary
st.header("📖 Section 2: Upload Data Dictionary (Optional)")
dictionary_csv = st.file_uploader("Upload a data dictionary CSV (optional)", type="csv", key="dict_csv")

# Enable AI
analyze = st.checkbox("📊 Analyze CSV with AI")

# Chat input
user_question = st.text_input("💬 Type your question here...")

if analyze and user_question and main_csv is not None:
    try:
        df = pd.read_csv(main_csv)
        prompt = f"""You are a data analyst. Answer the user's question based on the dataset below.

        Dataset (first few rows):
        {df.head(10).to_csv(index=False)}

        User Question:
        {user_question}
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        st.markdown("**🤖 AI Response:**")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
elif analyze and user_question and main_csv is None:
    st.warning("Please upload your main dataset first.")

# Optional previews
if main_csv:
    with st.expander("Preview Main Dataset"):
        st.dataframe(pd.read_csv(main_csv).head())

if dictionary_csv:
    with st.expander("Preview Data Dictionary"):
        st.dataframe(pd.read_csv(dictionary_csv).head())
