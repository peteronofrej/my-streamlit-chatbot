import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.set_page_config(page_title="Peter's AI Assistant")

st.title("Peter's AI Assistant")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

@st.cache_data
def load_eacb_document():
    reader = PdfReader("EACB_Position_Paper.pdf")

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


mode = st.radio(
    "What do you want to do?",
    [
        "Ask a general question",
        "Ask about the EACB document"
    ]
)

question = st.chat_input("Type your question here")

if question:

    if mode == "Ask a general question":
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]

    else:
        document_text = load_eacb_document()

        messages = [
            {
                "role": "system",
                "content": f"""
You are an expert assistant helping users understand the EACB document.

Answer the user's question based mainly on the EACB document below.
If the document does not contain enough information, clearly say that.

EACB DOCUMENT:

{document_text}
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]

    with st.chat_message("user"):
        st.write(question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(answer)
