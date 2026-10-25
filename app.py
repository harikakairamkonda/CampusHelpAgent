import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# -----------------------------
# Campus FAQ knowledge base
# -----------------------------
campus_faqs = {
    "attendance": {
        "keywords": ["attendance", "percentage", "absent"],
        "answer": (
            "Attendance requirements depend on your college rules. "
            "Please check the official academic regulations or contact "
            "your college office for the required percentage."
        )
    },
    "exams": {
        "keywords": ["exam", "examination", "timetable", "hall ticket"],
        "answer": (
            "For examination dates, timetables, and hall tickets, "
            "check your college's official examination notices."
        )
    },
    "assignments": {
        "keywords": ["assignment", "submission", "deadline", "homework"],
        "answer": (
            "Check with your subject faculty or official learning "
            "platform for assignment deadlines and submission rules."
        )
    },
    "library": {
        "keywords": ["library", "book", "borrow", "return"],
        "answer": (
            "For library hours, book borrowing limits, and return dates, "
            "please check your college library regulations."
        )
    },
    "holidays": {
        "keywords": ["holiday", "holidays", "vacation"],
        "answer": (
            "Please check the official academic calendar or college "
            "announcements for holiday information."
        )
    }
}

# -----------------------------
# Find an answer
# -----------------------------
def answer_question(question: str) -> str:
    question = question.lower().strip()

    for details in campus_faqs.values():
        if any(keyword in question for keyword in details["keywords"]):
            return details["answer"]

    return (
        "Sorry, I couldn't find that information in my FAQ data. "
        "Please contact your college office."
    )

# -----------------------------
# LangGraph agent
# -----------------------------
class CampusState(TypedDict):
    question: str
    answer: str

def campus_help_node(state: CampusState):
    return {
        "answer": answer_question(state["question"])
    }

builder = StateGraph(CampusState)
builder.add_node("campus_help", campus_help_node)
builder.add_edge(START, "campus_help")
builder.add_edge("campus_help", END)

campus_agent = builder.compile()

def ask_campus(question: str) -> str:
    result = campus_agent.invoke({
        "question": question,
        "answer": ""
    })
    return result["answer"]

# -----------------------------
# Streamlit web application
# -----------------------------
st.set_page_config(
    page_title="CampusHelp Agent",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 CampusHelp Agent")
st.write(
    "Ask questions about college information, including attendance, "
    "exams, assignments, library rules, and holidays."
)

with st.sidebar:
    st.subheader("Topics you can ask about")
    st.markdown(
        "- Attendance\n"
        "- Examination timetable\n"
        "- Assignments\n"
        "- Library\n"
        "- Holidays"
    )
    st.caption("Answers are based on sample FAQs, not verified college policies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Type your college question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    answer = ask_campus(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
