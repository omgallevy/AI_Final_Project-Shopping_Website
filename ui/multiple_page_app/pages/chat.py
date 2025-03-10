import pandas as pd
import streamlit as st
import os
from openai import OpenAI
from api import api
from styles import sidebar, custom_css


def render_chat_interface():
    if "df" not in st.session_state:
        inventory_items = api.get_all_items()
        st.session_state.df = pd.DataFrame(inventory_items, columns=['item_id', 'item_name', 'price', 'quantity'])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"name": "assistant", "content": "Hello! I’m your shopping assistant. How can I help you today?", "avatar": "🫀"}
        ]
        os.environ["OPENAI_API_KEY"] = ""
        st.session_state.client = OpenAI()
        st.session_state.conversation = [
            {"role": "system",
             "content": f"You are an assistant for a shopping site. Here’s the current stock: {st.session_state.df}. Users may ask questions about the stock or general inquiries, but you should only provide answers related to available items. If an item has a quantity of 0, make sure to let the user know."
            }
        ]

    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    st.markdown(custom_css("assets/BG03.png"), unsafe_allow_html=True)
    st.title("✨AI Shopping Assistant")
    st.header("Welcome to Your Smart Shopping Experience")

    user_input = st.chat_input(placeholder="Type your question here...")

    if user_input:
        if st.session_state.question_count < 5:
            st.session_state.chat_history.append({"name": "user", "content": user_input, "avatar": "💛"})
            st.session_state.conversation.append({"role": "user", "content": user_input})

            ai_response = st.session_state.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.conversation,
                temperature=1,
                max_tokens=300
            )

            response_content = ai_response.choices[0].message.content
            st.session_state.conversation.append({"role": "assistant", "content": response_content})
            st.session_state.chat_history.append({"name": "assistant", "content": response_content, "avatar": "🫀"})
            st.session_state.question_count += 1
        else:
            st.session_state.chat_history.append(
                {"name": "assistant", "content": "Sorry, you can only ask up to 5 questions.", "avatar": "🫀"}
            )

    for message in st.session_state.chat_history:
        st.chat_message(name=message.get("name"), avatar=message.get("avatar")).markdown(message.get("content"))
