import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Chatbot", layout="centered")

st.title("🤖 Chat with Your CSV")

# --- Section 1: Upload Main Dataset ---
st.header("📂 Section 1: Upload Main Dataset (CSV)")
st.caption("Choose your main data CSV file")
main_csv = st.file_uploader("Drag and drop file here", type="csv", key="main_csv")

# --- Section 2: Upload Data Dictionary (Optional) ---
st.header("📖 Section 2: Upload Data Dictionary (Optional)")
st.caption("Upload a data dictionary CSV (optional)")
dictionary_csv = st.file_uploader("Drag and drop file here", type="csv", key="dict_csv")

# --- Checkbox to enable AI analysis ---
analyze = st.checkbox("📊 Analyze CSV with AI")

# --- Chat input ---
user_question = st.text_input("💬 Type your question here...")

# --- AI analysis logic (placeholder) ---
if analyze and user_question and main_csv is not None:
    try:
        df = pd.read_csv(main_csv)
        st.markdown("**🤖 AI Response:**")
        st.write(f"You asked: `{user_question}`")
        st.write("Here's a quick look at your data:")
        st.dataframe(df.head())
        st.info("This is just a placeholder. You can plug in an LLM for real Q&A.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
elif analyze and user_question and main_csv is None:
    st.warning("Please upload your main dataset first.")

# --- Optional: Display uploaded files ---
if main_csv:
    with st.expander("Preview Main Dataset"):
        st.dataframe(pd.read_csv(main_csv).head())

if dictionary_csv:
    with st.expander("Preview Data Dictionary"):
        st.dataframe(pd.read_csv(dictionary_csv).head())
