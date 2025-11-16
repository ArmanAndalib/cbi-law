import streamlit as st
from law_chatbot import PersianLawChatbot

# Set page config with RTL support
st.set_page_config(
    page_title="قوانین بانک مرکزی جمهوری اسلامی ایران", 
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for RTL support
st.markdown("""
<style>
    /* RTL direction for entire app */
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for chat messages */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for user messages */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for assistant messages */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] div {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for sidebar */
    .css-1d391kg {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for input */
    .stTextInput input {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for headers */
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stAlert, .stCaption {
        direction: rtl;
        text-align: right;
    }
    
    /* Fix font for Persian */
    * {
        font-family: 'Tahoma', 'Arial', 'Segoe UI', sans-serif;
    }
    
    /* Better spacing for RTL */
    .stChatMessage {
        padding: 16px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ ربات مشاور")
st.write("سوالات خود در مورد قوانین بانک مرکزی بپرسید")

# Initialize chatbot
@st.cache_resource
def load_chatbot():
    try:
        chatbot = PersianLawChatbot()
        return chatbot
    except Exception as e:
        st.error(f"خطا در راه اندازی ربات: {e}")
        return None

chatbot = load_chatbot()

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Use custom formatting for RTL
        content = f"<div style='direction: rtl; text-align: right;'>{message['content']}</div>"
        st.markdown(content, unsafe_allow_html=True)
        if message.get("sources"):
            sources_text = f"<div style='direction: rtl; text-align: right; font-size: 0.8em; color: #666;'>منابع: {', '.join(message['sources'])}</div>"
            st.markdown(sources_text, unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("سوال خود را اینجا تایپ کنید..."):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        formatted_prompt = f"<div style='direction: rtl; text-align: right;'>{prompt}</div>"
        st.markdown(formatted_prompt, unsafe_allow_html=True)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("در حال پردازش..."):
            if chatbot:
                try:
                    answer, sources = chatbot.ask_question(prompt)
                    
                    # Format answer with RTL
                    formatted_answer = f"<div style='direction: rtl; text-align: right; line-height: 1.6;'>{answer}</div>"
                    st.markdown(formatted_answer, unsafe_allow_html=True)
                    
                    if sources and "یافت نشد" not in answer:
                        sources_text = f"<div style='direction: rtl; text-align: right; font-size: 0.8em; color: #666; margin-top: 10px;'>منابع: {', '.join(sources)}</div>"
                        st.markdown(sources_text, unsafe_allow_html=True)
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    error_msg = f"خطا در پردازش سوال: {e}"
                    formatted_error = f"<div style='direction: rtl; text-align: right; color: red;'>{error_msg}</div>"
                    st.markdown(formatted_error, unsafe_allow_html=True)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "sources": []
                    })
            else:
                error_msg = "ربات راه اندازی نشده است. لطفاً مطمئن شوید که مراحل قبل را به درستی انجام داده اید."
                formatted_error = f"<div style='direction: rtl; text-align: right; color: red;'>{error_msg}</div>"
                st.markdown(formatted_error, unsafe_allow_html=True)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg,
                    "sources": []
                })

# Sidebar with RTL information
with st.sidebar:
    st.header("ℹ️ راهنما")
    
    st.markdown("""
    <div style='direction: rtl; text-align: right;'>
    <h4>نمونه سوالات:</h4>
    <ul style='padding-right: 20px;'>
        <li>مفاد اصلی این قانون چیست؟</li>
        <li>شرایط و ضوابط این قانون چه مواردی هستند؟</li>
        <li>مجازات های پیش بینی شده در این قانون چیست؟</li>
        <li>حقوق تعیین شده در این قانون چه مواردی هستند؟</li>
    </ul>
    
    <h4>توجه:</h4>
    <ul style='padding-right: 20px;'>
        <li>پاسخ ها بر اساس متون قانونی موجود ارائه می‌شوند</li>
        <li>در صورت عدم وجود اطلاعات کافی، ربات صادقانه اعلام می‌کند</li>
        <li>پاسخ ها به زبان فارسی هستند</li>
        <li>متن از راست به چپ نمایش داده می‌شود</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if chatbot and hasattr(chatbot, 'chat_history'):
        st.metric("تعداد سوالات این جلسه", len(chatbot.chat_history))
    
    if chatbot and hasattr(chatbot, 'available_models'):
        st.subheader("مدل های موجود")
        for model in chatbot.available_models[:3]:
            st.text(f"• {model}")

# Add footer with RTL
st.markdown("""
<div style='direction: rtl; text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; color: #666;'>
    <p>ربات مشاور حقوقی فارسی - توسعه یافته برای تحلیل قوانین ایران</p>
</div>
""", unsafe_allow_html=True)