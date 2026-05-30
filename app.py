import streamlit as st
from openai import OpenAI

st.title("Peter's AI Chatbot")

api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password"
)

if api_key:

    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(
            message["content"]
        )

    prompt = st.chat_input("Ask me something")

    if prompt:

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        st.chat_message("user").write(prompt)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.chat_message("assistant").write(answer)