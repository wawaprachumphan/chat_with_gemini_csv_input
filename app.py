import streamlit as st
import pandas as pd
import textwrap
import google.generativeai as genai

# Configure API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Helper function to format markdown
def to_markdown(text):
    text = text.replace('•', ' *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Streamlit UI
st.title("🧠 Gemini Data Analyst Dashboard")
st.markdown("Upload your dataset, ask questions, and get answers with Gemini!")

uploaded_file = st.file_uploader("📤 Upload your transaction CSV", type=["csv"])
data_dict_file = st.file_uploader("📤 Upload your data dictionary CSV", type=["csv"])

if uploaded_file and data_dict_file:
    df = pd.read_csv(uploaded_file)
    data_dict_df = pd.read_csv(data_dict_file)

    st.subheader("📊 Sample Data")
    st.dataframe(df.head(5))

    data_dict_text = '\n'.join(
        '- ' + row['column_name'] + ': ' + row['data_type'] + '. ' + row['description']
        for _, row in data_dict_df.iterrows()
    )

    user_question = st.text_input("❓ Ask a question about the data:")
    
    if user_question:
        with st.spinner("Gemini is analyzing your question..."):

            prompt = f"""
You are a helpful Python code generator.
Your goal is to write Python code snippets based on the user's question
and the provided DataFrame information.

Here's the context:
**User Question:**
{user_question}
**DataFrame Name:**
df
**DataFrame Details:**
{data_dict_text}
**Sample Data (Top 2 Rows):**
{df.head(2).to_string(index=False)}
**Instructions:**
1. Write Python code that addresses the user's question by querying or manipulating the DataFrame.
2. Use the `exec()` function to execute the generated code.
3. Do not import pandas.
4. Change date column type to datetime if needed.
5. Store the result in a variable named ANSWER.
6. Assume the DataFrame is already loaded and named `df`.
7. Keep code concise and focused on answering the question.
"""

            response = model.generate_content(prompt)
            code_response = response.text.strip().replace("```python", "").replace("```", "")

            try:
                # Check if a 'date' column exists, and convert to datetime if necessary
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')

                # Execute Gemini-generated code with pd and df available
                local_vars = {"df": df, "pd": pd}
                exec(code_response, {}, local_vars)

                # Retrieve the result from local_vars
                ANSWER = local_vars.get("ANSWER", "No result found")

                st.subheader("🔍 Answer")
                st.write(ANSWER)

                # Explanation prompt for Gemini
                explanation_prompt = f"""
The user asked: "{user_question}"  
Here is the result: {ANSWER}  
Please summarize and interpret this result in simple terms. Include the following:
1. A summary of the result (what it means in plain language).
2. An analysis of the customer's persona based on the question (what can we infer about them based on their request).
"""

                explanation_response = model.generate_content(explanation_prompt)
                st.subheader("📘 Explanation and Analysis")
                st.markdown(to_markdown(explanation_response.text))

            except Exception as e:
                st.error(f"❌ Error executing code: {e}")
