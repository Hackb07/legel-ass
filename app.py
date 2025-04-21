import streamlit as st
import PyPDF2
import os
from groq import Groq

# 🗝️ Set your Groq API key
GROQ_API_KEY = "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"  # 🔐 Replace this with your key
client = Groq(api_key=GROQ_API_KEY)

# 🧠 Function to extract text from uploaded PDF(s)
def extract_text_from_pdfs(uploaded_files):
    full_text = ""
    for pdf in uploaded_files:
        reader = PyPDF2.PdfReader(pdf)
        for page in reader.pages:
            full_text += page.extract_text()
    return full_text

# ✨ Function to call Groq LLaMA3 model
def ask_llama3(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

# 🖼️ Streamlit UI
st.set_page_config(page_title="🧠 Legal Assistant (Groq)", layout="wide")
st.title("⚖️ AI Legal Assistant with Groq 🚀")

uploaded_files = st.file_uploader("📄 Upload legal PDF(s)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Extracting text..."):
        document_text = extract_text_from_pdfs(uploaded_files)

    st.subheader("📃 Document Preview")
    with st.expander("🔍 View Extracted Text"):
        st.write(document_text[:1500] + "...")  # Show first 1500 chars

    if st.button("🧠 Summarize Document"):
        with st.spinner("Summarizing with LLaMA3..."):
            summary = ask_llama3(f"Summarize this legal document:\n\n{document_text}")
            st.success("✅ Summary:")
            st.write(summary)

    st.subheader("💬 Ask a Legal Question")
    user_query = st.text_input("Enter your legal question here")

    if user_query:
        with st.spinner("Answering..."):
            answer = ask_llama3(f"Based on this legal document:\n\n{document_text}\n\nQuestion: {user_query}")
            st.success("✅ Answer:")
            st.write(answer)
