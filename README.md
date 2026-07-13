# 🎯 AI Resume Analyzer — AIML Project

> **Project 5 · Resume Analyzer (Small Batch)**  
> Analyzes 3–5 resumes against a job description using **Claude (Anthropic API)**  
> Outputs: Skill Match Analysis · Ranked Leaderboard · Improvement Suggestions

---

## 📸 Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Upload 3–5 real resume PDFs |
| 🤖 AI Analysis | Claude reads & scores each resume |
| 📊 Skill Match | Matched vs missing skills per candidate |
| 🏆 Ranking | Candidates ranked by overall fit score |
| 💡 Suggestions | Personalised improvement tips |
| ⬇️ Export | Download full results as JSON |

---

## ⚙️ Setup Instructions (Step by Step)

### Step 1 — Clone / Download the Project

Place the project folder (e.g., `resume_analyzer/`) anywhere on your PC.

### Step 2 — Install Python (if not done)

Download Python 3.10+ from https://www.python.org/downloads/  
During install ✅ check **"Add Python to PATH"**

### Step 3 — Open VS Code Terminal

```
cd path/to/resume_analyzer
```

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Get Your Free Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up (free tier available)
3. Go to **API Keys** → Create new key
4. Copy the key (starts with `sk-ant-...`)

> ⚠️ Never commit your API key to GitHub!

### Step 6 — Run the App

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

---

## 🖥️ How to Use

1. **Enter API Key** in the left sidebar
2. **Upload 3–5 PDF resumes** (drag & drop)
3. **Paste the Job Description** in the main text box
4. Click **🚀 Analyze Resumes with AI**
5. View results:
   - Summary metrics at the top
   - Ranked candidate cards with score bars
   - Expand each card for full analysis
6. **Download JSON** for your report

---

## 📁 Project Structure

```
resume_analyzer/
│
├── app.py               ← Main Streamlit application
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## 🧪 Sample Test Data

You can test with any 3–5 PDF resumes. Use a job description like:

```
We are looking for a Machine Learning Engineer with:
- 2+ years experience in Python and ML frameworks (TensorFlow, PyTorch)
- Familiarity with NLP and computer vision
- Experience with cloud platforms (AWS/GCP)
- B.Tech/M.Tech in CS or related field
- Strong knowledge of data structures and algorithms
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI Framework | Streamlit |
| AI Engine | Claude 3.5 Sonnet (Anthropic) |
| PDF Parser | pdfplumber |
| Language | Python 3.10+ |

---

## 👨‍💻 Made for AIML Project — Resume Analyzer (Batch 5)
