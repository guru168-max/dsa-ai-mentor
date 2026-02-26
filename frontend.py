import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from mentor import explain_topic, generate_problem, evaluate_code
from database import create_user, authenticate_user, save_submission

st.set_page_config(
    page_title="AI Coding Lab",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SESSION ----------------
defaults = {
    "problem_text": "",
    "user": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- LOGIN ----------------
if not st.session_state.user:

    st.title("🔐 AI Coding Lab - Login / Register")

    mode = st.radio("Choose Mode", ["Login", "Register"], horizontal=True)

    with st.form("auth_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(
            "Create Account" if mode == "Register" else "Login"
        )

        if submit:
            if not username or not password:
                st.error("Fill all fields")
                st.stop()

            if mode == "Register":
                if create_user(username, password):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username exists.")
            else:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"👤 {st.session_state.user[1]}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

menu = st.sidebar.radio(
    "📚 Navigation",
    ["Explain Topic", "Generate Problem",
     "Dashboard", "My History", "Daily Tasks"]
)

st.title("🧠 AI Coding Lab")
st.divider()

# =================================================
# EXPLAIN
# =================================================
if menu == "Explain Topic":

    topic = st.text_input("Enter Topic")

    if st.button("Explain") and topic:
        with st.spinner("Explaining..."):
            explanation = explain_topic(topic)
            st.success(explanation)

# =================================================
# GENERATE PROBLEM
# =================================================
elif menu == "Generate Problem":

    topic = st.text_input("Enter Topic")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate") and topic:
        problem = generate_problem(f"{difficulty} {topic}")
        st.session_state.problem_text = problem

    if st.session_state.problem_text:

        st.text_area("Problem", st.session_state.problem_text, height=200)

        code = st.text_area("Your Code")

        if st.button("Check Code") and code:

            result = evaluate_code(st.session_state.problem_text, code)
            st.success(result)

            is_correct = 1 if "correct" in result.lower() else 0

            save_submission(
                st.session_state.user[0],
                topic,
                difficulty,
                "Auto",
                st.session_state.problem_text,
                code,
                result,
                is_correct
            )

# =================================================
# DASHBOARD (IMPROVED)
# =================================================
elif menu == "Dashboard":

    st.header("📊 Performance Overview")

    conn = sqlite3.connect("dsa_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*),
        SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END)
        FROM submissions
        WHERE user_id=?
    """, (st.session_state.user[0],))

    row = cursor.fetchone()
    conn.close()

    total = row[0] if row and row[0] else 0
    correct = row[1] if row and row[1] else 0
    wrong = total - correct
    accuracy = (correct / total * 100) if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 Total Attempts", total)
    col2.metric("✅ Correct", correct)
    col3.metric("❌ Wrong", wrong)
    col4.metric("🎯 Accuracy", f"{accuracy:.2f}%")

    st.divider()
    st.subheader("Progress to Expert Level 🚀")
    progress = min(correct / 15, 1.0)
    st.progress(progress)

    if correct < 7:
        st.info("Beginner Level")
    elif correct < 15:
        st.warning("Intermediate Level")
    else:
        st.success("🔥 Expert Level")

    chart_data = pd.DataFrame({
        "Status": ["Correct", "Wrong"],
        "Count": [correct, wrong]
    })

    st.subheader("Performance Breakdown")
    st.bar_chart(chart_data.set_index("Status"))

# =================================================
# MY HISTORY (IMPROVED)
# =================================================
elif menu == "My History":

    st.header("📜 Submission History")

    conn = sqlite3.connect("dsa_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, difficulty, timestamp, is_correct
        FROM submissions
        WHERE user_id=?
        ORDER BY timestamp DESC
    """, (st.session_state.user[0],))

    rows = cursor.fetchall()
    conn.close()

    if rows:
        df = pd.DataFrame(
            rows,
            columns=["Topic", "Difficulty", "Time", "Correct"]
        )

        df["Result"] = df["Correct"].apply(
            lambda x: "✅ Correct" if x == 1 else "❌ Wrong"
        )

        df = df.drop(columns=["Correct"])

        st.dataframe(df, use_container_width=True)
        st.success(f"Total Submissions: {len(df)}")

    else:
        st.info("No submissions yet. Start solving problems! 🚀")

# =================================================
# DAILY TASKS (PROFESSIONAL)
# =================================================
elif menu == "Daily Tasks":

    st.header("📅 Daily Practice Tasks")

    conn = sqlite3.connect("dsa_ai.db")
    cursor = conn.cursor()

    with st.expander("➕ Add New Task"):

        col1, col2 = st.columns(2)
        topic = col1.text_input("Topic")
        pattern = col2.text_input("Pattern")

        problem = st.text_area("Problem Statement")
        approach = st.text_area("Approach / Intuition")

        if st.button("Add Task"):
            if topic and problem:
                cursor.execute("""
                    INSERT INTO daily_tasks
                    (user_id, topic, pattern, intuition, completed)
                    VALUES (?, ?, ?, ?, 0)
                """, (
                    st.session_state.user[0],
                    topic,
                    pattern,
                    problem + "||" + approach
                ))
                conn.commit()
                st.success("Task Added Successfully ✅")
                st.rerun()
            else:
                st.error("Topic and Problem are required!")

    st.divider()

    cursor.execute("""
        SELECT id, topic, pattern, intuition, completed
        FROM daily_tasks
        WHERE user_id=? AND date=DATE('now')
        ORDER BY id DESC
    """, (st.session_state.user[0],))

    tasks = cursor.fetchall()

    if not tasks:
        st.info("No tasks added for today. Add one above 🚀")

    for t in tasks:
        id_, topic, pattern, data, done = t
        parts = data.split("||")

        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(f"🧠 {topic}")
                st.write(f"**Pattern:** {pattern}")
                st.write(f"**Problem:** {parts[0]}")

                if len(parts) > 1 and parts[1].strip():
                    st.write(f"**Approach:** {parts[1]}")

            with col2:
                status = "✅ Done" if done else "⏳ Pending"
                st.markdown(f"### {status}")

                checked = st.checkbox(
                    "Mark Done",
                    value=bool(done),
                    key=f"task_{id_}"
                )

                if checked != bool(done):
                    cursor.execute(
                        "UPDATE daily_tasks SET completed=? WHERE id=?",
                        (1 if checked else 0, id_)
                    )
                    conn.commit()
                    st.success("Updated!")
                    st.rerun()

        st.divider()

    conn.close()
