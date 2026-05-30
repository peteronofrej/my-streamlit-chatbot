import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.title("Peter's Document Chatbot")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type="pdf"
)

if uploaded_file:
    reader = PdfReader(uploaded_file)

    document_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            document_text += text + "\n"

    st.success("PDF uploaded successfully.")

    question = st.chat_input("Ask a question about the document")

    if question:
        with st.chat_message("user"):
            st.write(question)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions based only on the uploaded PDF document."
                },
                {
                    "role": "user",
                    "content": f"""
Here is the document:

{document_text}

Question:
{question}
"""
                }
            ]
        )

        answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(answer)
else:
    st.info("Please upload a PDF document first.")
