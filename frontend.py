import streamlit as st
from mentor import explain_topic, generate_problem, give_hint, evaluate_code
from sheet_db import save_to_sheet

# Page configuration (ONLY ONCE and must be first Streamlit command)
st.set_page_config(
    page_title="AI Coding Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 AI Coding Lab")
st.subheader("Adaptive DSA Learning Assistant")

# -----------------------
# Session State Variables
# -----------------------
if "menu" not in st.session_state:
    st.session_state.menu = "Explain Topic"

if "result" not in st.session_state:
    st.session_state.result = ""

if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

if "code_text" not in st.session_state:
    st.session_state.code_text = ""

if "hint_result" not in st.session_state:
    st.session_state.hint_result = ""

# -----------------------
# Sidebar Menu
# -----------------------
menu = st.sidebar.selectbox(
    "Choose Mode",
    ["Explain Topic", "Generate Problem", "Get Hint", "Evaluate Code"],
    index=["Explain Topic", "Generate Problem", "Get Hint", "Evaluate Code"].index(st.session_state.menu),
)

st.session_state.menu = menu


# =======================
# EXPLAIN TOPIC
# =======================
if menu == "Explain Topic":
    topic = st.text_input("Enter DSA Topic")

    if st.button("Explain"):
        if topic:
            with st.spinner("Teaching..."):
                st.session_state.result = explain_topic(topic)

    if st.session_state.result:
        st.write(st.session_state.result)


# =======================
# GENERATE PROBLEM
# =======================
elif menu == "Generate Problem":
    topic = st.text_input("Enter Topic for Problem")
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate"):
        if topic:
            with st.spinner("Creating problem..."):
                problem = generate_problem(f"{difficulty} {topic}")
                st.session_state.result = problem
                st.session_state.problem_text = problem
                st.session_state.hint_result = ""

    if st.session_state.problem_text:
        st.text_area("Problem", st.session_state.problem_text, height=300)

        # Get Hint Inline
        if st.button("Get Hint for this problem"):
            with st.spinner("Thinking..."):
                st.session_state.hint_result = give_hint(st.session_state.problem_text)

        if st.session_state.hint_result:
            st.write("💡 Hint:")
            st.write(st.session_state.hint_result)

        # Code Submission
        st.write("💻 Submit Your Code")
        code_input = st.text_area("Paste Your Solution Here", height=200)

        if st.button("Check Code"):
            if code_input:
                with st.spinner("Checking code..."):
                    eval_result = evaluate_code(
                        st.session_state.problem_text,
                        code_input
                    )

                st.write("✅ Evaluation Result:")
                st.write(eval_result)

                # ✅ SAVE TO GOOGLE SHEET
                save_to_sheet(
                    topic,
                    difficulty,
                    st.session_state.problem_text,
                    eval_result
                )


# =======================
# GET HINT (Standalone)
# =======================
elif menu == "Get Hint":
    problem = st.text_area("Paste Problem", height=300)

    if st.button("Get Hint"):
        if problem:
            with st.spinner("Thinking..."):
                st.session_state.result = give_hint(problem)

    if st.session_state.result:
        st.write(st.session_state.result)


# =======================
# EVALUATE CODE (Standalone)
# =======================
elif menu == "Evaluate Code":
    problem = st.text_area("Paste Problem", height=200)
    code = st.text_area("Paste Your Code", height=200)

    if st.button("Evaluate"):
        if problem and code:
            with st.spinner("Checking code..."):
                eval_result = evaluate_code(problem, code)

            st.write("✅ Evaluation Result:")
            st.write(eval_result)

            # Save to Google Sheet
            save_to_sheet(
                "Manual Evaluation",
                "N/A",
                problem,
                eval_result
            )