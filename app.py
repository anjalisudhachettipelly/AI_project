from ollama import chat
import streamlit as st
from datetime import date
st.set_page_config(
    page_title="Smart Task Assistant",
    page_icon="🧠"
)

st.title("🧠 Smart Task Assistant")

st.write(
    "AI-Based Smart Task Prioritization and Productivity System"
)
# AI Personality / System Prompt
personality = """
You are a productivity assistant.
Analyze the user's tasks based on importance and deadline.
When the user asks which task has the highest priority, answer in exactly ONE sentence.
Mention only the task name and a short reason.
Do not give explanations, lists, or extra details.
"""

# Session State
if "history" not in st.session_state:

    st.session_state.history = [
        {
            "role": "system",
            "content": personality
        }
    ]


if "tasks" not in st.session_state:

    st.session_state.tasks = []


# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    st.header("⚙️ Task Controls")

    task_name = st.text_input(
        "Task Name"
    )

    importance = st.selectbox(
        "Importance",
        ["High", "Medium", "Low"]
    )

    deadline = st.date_input(
        "Deadline",
        min_value=date.today()
    )

    if st.button("➕ Add Task"):

        if task_name:

            task = {
                "name": task_name,
                "importance": importance,
                "deadline": deadline
            }

            st.session_state.tasks.append(task)

            st.success("Task added successfully!")

        else:

            st.warning("Enter a task name.")


    st.divider()


    if st.button("🗑️ Clear Tasks"):

        st.session_state.tasks = []

        st.success("Tasks cleared!")


    if st.button("🔄 Clear Chat"):

        st.session_state.history = [
            {
                "role": "system",
                "content": personality
            }
        ]

        st.rerun()


    if st.button("👨‍🏫 Strict Mode"):

        st.session_state.history[0]["content"] = personality_2

        st.success("Strict mode activated!")


# -------------------------------
# Display Tasks
# -------------------------------

st.header("📋 My Tasks")


if len(st.session_state.tasks) == 0:

    st.info("No tasks added yet.")

else:

    for i, task in enumerate(st.session_state.tasks):

        st.write(
            f"**{i + 1}. {task['name']}**"
        )

        st.write(
            f"Importance: {task['importance']} | "
            f"Deadline: {task['deadline']}"
        )


# -------------------------------
# Notifications
# -------------------------------

st.header("🔔 Notifications")


today = date.today()

if len(st.session_state.tasks) == 0:

    st.info("No notifications.")

else:

    notification_found = False

    for task in st.session_state.tasks:

        days_left = (
            task["deadline"] - today
        ).days


        if days_left < 0:

            st.error(
                f"🚨 {task['name']} is overdue!"
            )

            notification_found = True


        elif days_left == 0:

            st.warning(
                f"🔔 {task['name']} is due today!"
            )

            notification_found = True


        elif days_left == 1:

            st.warning(
                f"🔔 {task['name']} is due tomorrow!"
            )

            notification_found = True


    if not notification_found:

        st.success("No urgent notifications.")


# -------------------------------
# Chatbot Introduction
# -------------------------------

st.header("💬 AI Productivity Assistant")

with st.chat_message("assistant"):

    st.write(
        "Hello! 👋 I'm your Smart Task Assistant. "
        "Add your tasks and ask me which task you should complete first."
    )


# -------------------------------
# Display Chat History
# -------------------------------

for msg in st.session_state.history[1:]:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])


# -------------------------------
# Chat Input
# -------------------------------

question = st.chat_input(
    "Ask me about your tasks..."
)


# -------------------------------
# AI Response
# -------------------------------

if question:

    # Add user question
    st.session_state.history.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.write(question)


    # Create task information
    task_information = ""

    for task in st.session_state.tasks:

        task_information += (
            f"Task: {task['name']}, "
            f"Importance: {task['importance']}, "
            f"Deadline: {task['deadline']}\n"
        )
    # Give tasks to AI
    ai_prompt = f"""
The user's current tasks are:

{task_information}

User's question:
{question}

Analyze the tasks and provide the best priority recommendation.
"""
    try:
        with st.spinner("Thinking..."):
            response = chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "system",
                        "content": st.session_state.history[0]["content"]
                    },
                    {
                        "role": "user",
                        "content": ai_prompt
                    }
                ]
            )
        reply = response["message"]["content"]
        # Store AI response
        st.session_state.history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )
        with st.chat_message("assistant"):

            st.write(reply)

    except Exception as e:

        st.error(
            "Ollama is not working. "
            "Please make sure Ollama is running and try again."
        )