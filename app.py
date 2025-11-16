import streamlit as st
from law_chatbot import PersianLawChatbot

st.set_page_config(page_title="ربات حقوقی فارسی", page_icon="⚖️")

st.title("⚖️ ربات مشاور حقوقی فارسی")
st.write("سوالات خود در مورد قوانین ایران را بپرسید")

# Initialize chatbot
@st.cache_resource
def load_chatbot():
    return PersianLawChatbot()

chatbot = load_chatbot()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("سوال خود را اینجا تایپ کنید..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("در حال پردازش..."):
            answer, sources = chatbot.ask_question(prompt)
            st.markdown(answer)
            if sources:
                st.caption(f"منابع: {', '.join(set(sources))}")
    
    st.session_state.messages.append({"role": "assistant", "content": answer})