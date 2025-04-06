import streamlit as st
import pandas as pd
import textwrap
import google.generativeai as genai

# Configure API Key for Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Helper function to format markdown
def to_markdown(text):
    text = text.replace('•', ' *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Streamlit UI
st.title("🧠 Gemini Data Chatbot")
st.markdown("Upload your dataset, ask questions, and get answers from the data!")

# File uploader to upload CSV
uploaded_file = st.file_uploader("📤 Upload your transaction CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Sample Data")
    st.dataframe(df.head(5))  # Show the first few rows of the uploaded data

    # Create data dictionary text for context
    data_dict_text = "\n".join(
        "- " + col + ": " + str(df[col].dtype) + ". This column contains " + str(df[col].nunique()) + " unique values."
        for col in df.columns
    )

    # Chatbot state to store conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    # User input for asking a question
    user_question = st.text_input("❓ Ask a question about the data:")

    if user_question:
        with st.spinner("Gemini is analyzing your question..."):

            # Add user question to conversation history
            st.session_state['conversation_history'].append(f"You: {user_question}")
            
            # Create the prompt with conversation history
            conversation_text = "\n".join(st.session_state['conversation_history'])
            prompt = f"""
You are a helpful Python code generator. You will respond to questions about a dataset.
Please consider the following context:

**User Question:**
{user_question}

**DataFrame Details:**
{data_dict_text}

**Conversation History:**
{conversation_text}

**Instructions:**
1. Respond to the user's question based on the dataset and the conversation history.
2. If you need to generate code to answer the question, be concise and clear.
3. Provide a plain language explanation if needed.

Use the information above to generate the response.
"""

            # Get response from Gemini
            response = model.generate_content(prompt)
            answer = response.text.strip()

            # Add Gemini response to conversation history
            st.session_state['conversation_history'].append(f"Gemini: {answer}")
            
            # Show the full conversation
            st.subheader("💬 Conversation History")
            for msg in st.session_state['conversation_history']:
                st.write(msg)

            # Optionally explain the results using another prompt to Gemini
            explanation_prompt = f"""
The user asked: "{user_question}"
Here is the result: {answer}
Please summarize and interpret this result in simple terms.
"""

            explanation_response = model.generate_content(explanation_prompt)
            st.subheader("📘 Explanation")
            st.markdown(to_markdown(explanation_response.text))
