# 🧠 AI Coding Lab – DSA AI Mentor

An AI-powered Data Structures & Algorithms learning assistant built using **LangGraph**, **Groq (Llama 3.1)**, and **Streamlit**.

This platform helps users understand DSA concepts, generate practice problems, receive guided hints, evaluate code solutions, and track progress using cloud-based storage.

---

## 🚀 Features

### 📘 Concept Explanation

- Step-by-step explanation of DSA topics
- Simple examples
- Time & space complexity discussion

### 🧠 Problem Generation

- LeetCode-style problems
- Difficulty levels: Easy / Medium / Hard
- Topic-based generation

### 💡 Guided Hints

- Progressive hints
- Encourages logical thinking
- Does not reveal full solution immediately

### 🧪 Code Evaluation

- Checks correctness
- Reviews time complexity
- Suggests optimizations

### 📊 Cloud Progress Tracking

- Stores user activity in Google Sheets
- Tracks topic, difficulty, and evaluation results

---

## 🏗 Tech Stack

- **Python**
- **Streamlit** – Interactive Web UI
- **LangGraph** – Agent orchestration
- **Groq (Llama 3.1)** – Fast AI inference
- **Google Sheets API** – Cloud persistence
- **gspread & google-auth** – Sheets integration

---

## 📂 Project Structure

```
dsa-ai-mentor/
│
├── frontend.py          # Streamlit UI
├── mentor.py            # AI logic & prompts
├── sheet_db.py          # Google Sheets integration
├── requirements.txt
├── .env
├── credentials.json
└── README.md
```

---

## 🔐 Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/dsa-ai-mentor.git
cd dsa-ai-mentor
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Add Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Add Google Service Account

Place your `credentials.json` file in the project root.

Make sure:

- Google Sheets API is enabled
- The sheet is shared with your service account email

### 6️⃣ Run Application

```
streamlit run frontend.py
```

App will open at:

```
http://localhost:8501
```

---

## 🎯 Resume Description

Developed an AI-powered adaptive DSA learning platform using LangGraph and Groq (Llama 3.1), featuring dynamic problem generation, guided hinting, real-time code evaluation, and cloud-based progress tracking via Google Sheets integration.

---

## 🚀 Future Enhancements

- Adaptive difficulty engine
- User authentication system
- Real analytics dashboard
- Local database support
- Multi-model support

---

## 📜 License

This project is built for educational and portfolio purposes.
