import streamlit as st
from langgraph_database_backend import chatbot, retriver_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# ******************** Utility Functions ********************

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():
    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

    if thread_id not in st.session_state['thread_titles']:
        thread_number = len(st.session_state['thread_titles']) + 1
        st.session_state['thread_titles'][thread_id] = (
            f"Thread {thread_number}"
        )


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )

    return state.values.get('messages', [])


def get_recent_user_message(messages):
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content

    return "New conversation"


# ******************** Session Setup ********************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retriver_all_threads()

if 'thread_titles' not in st.session_state:
    st.session_state['thread_titles'] = {}

# Ensure existing database threads have display titles.
for thread_id in st.session_state['chat_threads']:
    add_thread(thread_id)

add_thread(st.session_state['thread_id'])


# ******************** Sidebar UI ********************

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:

    messages = load_conversation(thread_id)

    recent_message = get_recent_user_message(messages)

    thread_title = st.session_state['thread_titles'][thread_id]

    # Keep the sidebar labels short.
    recent_message = recent_message.replace("\n", " ")

    if len(recent_message) > 25:
        recent_message = recent_message[:25] + "..."

    button_label = f"{thread_title}: {recent_message}"

    if st.sidebar.button(
        button_label,
        key=f"thread_{thread_id}"
    ):
        st.session_state['thread_id'] = thread_id

        st.session_state['message_history'] = [
            {
                'role': (
                    'user'
                    if isinstance(msg, HumanMessage)
                    else 'assistant'
                ),
                'content': msg.content
            }
            for msg in messages
            if isinstance(msg, (HumanMessage, AIMessage))
            and isinstance(msg.content, str)
        ]

        st.rerun()


# ******************** Main Chat UI ********************

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


user_input = st.chat_input("Type here...")


if user_input:

    # Display user message.
    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        }
    }

    # Stream the AI response.
    with st.chat_message("assistant"):

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):

                if (
                    isinstance(message_chunk, AIMessage)
                    and isinstance(message_chunk.content, str)
                ):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # Save assistant response in Streamlit session history.
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_message
    })

    # Refresh so the latest user input appears in the sidebar.
    st.rerun()