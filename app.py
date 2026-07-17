import streamlit as st
import pdfplumber
import json
import time
import re
from io import BytesIO
from groq import Groq

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2.2rem !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #a78bfa !important; font-size: 1rem !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] > div { color: #ffffff !important; }
div[data-testid="metric-container"] * { color: #ffffff !important; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #f0f0f0;
}
div[data-testid="stToolbar"] {
    display: none !important;
    visibility: hidden !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
}
.hero-banner h1 { font-size: 2.8rem; font-weight: 800; color: #fff; margin: 0; letter-spacing: -1px; }
.hero-banner p  { font-size: 1.1rem; color: rgba(255,255,255,0.85); margin: 0.5rem 0 0; }

.free-badge {
    display: inline-block;
    background: linear-gradient(135deg, #48c78e, #06d6a0);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 3px 14px;
    border-radius: 20px;
    margin-left: 10px;
    vertical-align: middle;
}

.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.3); }

.score-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    height: 12px;
    margin: 6px 0 12px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 1s ease;
}

.chip-matched {
    display: inline-block;
    background: rgba(72,199,142,0.2);
    border: 1px solid rgba(72,199,142,0.5);
    color: #48c78e;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px;
}
.chip-missing {
    display: inline-block;
    background: rgba(255,100,100,0.15);
    border: 1px solid rgba(255,100,100,0.4);
    color: #ff6464;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #a78bfa;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid rgba(167,139,250,0.3);
    padding-bottom: 0.4rem;
}

.suggestion-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #667eea;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.92rem;
    color: #ddd;
}

.pill-excellent { background: rgba(72,199,142,0.2); color: #48c78e; border: 1px solid #48c78e; border-radius: 12px; padding: 2px 10px; font-size: 0.8rem; font-weight: 600; }
.pill-good      { background: rgba(100,181,246,0.2); color: #64b5f6; border: 1px solid #64b5f6; border-radius: 12px; padding: 2px 10px; font-size: 0.8rem; font-weight: 600; }
.pill-average   { background: rgba(255,183,77,0.2);  color: #ffb74d; border: 1px solid #ffb74d; border-radius: 12px; padding: 2px 10px; font-size: 0.8rem; font-weight: 600; }
.pill-weak      { background: rgba(255,100,100,0.2); color: #ff6464; border: 1px solid #ff6464; border-radius: 12px; padding: 2px 10px; font-size: 0.8rem; font-weight: 600; }

.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

.stTextArea textarea, .stTextInput input {
    background: #ffffff !important;
    border: 1px solid rgba(102,126,234,0.5) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)) !important;
    border: 2px dashed #a78bfa !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.3) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stFileUploader"]:hover {
    background: linear-gradient(135deg, rgba(102,126,234,0.25), rgba(118,75,162,0.25)) !important;
    border-color: #667eea !important;
    box-shadow: 0 6px 25px rgba(102,126,234,0.5) !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #c4b5fd !important;
}
div[data-testid="stFileUploader"] button[kind="secondary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.5) !important;
}
div[data-testid="stFileUploader"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}
div[data-testid="stFileUploader"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    background: rgba(102,126,234,0.2) !important;
    border: 1px solid rgba(102,126,234,0.5) !important;
    border-radius: 10px !important;
    padding: 6px 10px !important;
}
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}
div[data-testid="stFileUploader"] small {
    color: #a78bfa !important;
    font-weight: 600 !important;
}
div[data-testid="stFileUploader"] small {
    color: #c4b5fd !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
section[data-testid="stSidebar"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #c4b5fd !important;
}
button[data-testid="stFileUploaderDeleteBtn"] {
    background: rgba(255,100,100,0.2) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] small {
    color: #a78bfa !important;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="metric-container"] label {
    color: #a78bfa !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] > div {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
}
/* Make Excellent green, Good blue, Average orange, Weak red */
div[data-testid="stMetricValue"] > div {
    color: #ffffff !important;
}
.free-info-box {
    background: rgba(72,199,142,0.1);
    border: 1px solid rgba(72,199,142,0.4);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #a0f0c0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file) -> str:
    text = ""
    try:
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.warning(f"Could not parse {uploaded_file.name}: {e}")
    return text.strip()


def analyze_resumes_with_groq(resumes: dict, job_description: str, api_key: str) -> dict:
    client = Groq(api_key=api_key)

    resume_block = ""
    for idx, (name, text) in enumerate(resumes.items(), 1):
        resume_block += f"\n\n--- RESUME {idx}: {name} ---\n{text[:3000]}"

    prompt = f"""You are an expert HR analyst and technical recruiter.
Analyze the following resumes against the job description and return a structured JSON response.

JOB DESCRIPTION:
{job_description}

RESUMES:
{resume_block}

Return ONLY a valid JSON object. No markdown, no backticks, no extra text. Pure JSON only.
Use this exact structure:
{{
  "ranked_candidates": [
    {{
      "rank": 1,
      "name": "Resume filename or Candidate N",
      "overall_score": 85,
      "match_level": "Excellent",
      "matched_skills": ["Python", "Machine Learning"],
      "missing_skills": ["Kubernetes", "AWS"],
      "experience_match": "4 years – strong match",
      "education_match": "B.Tech CS – meets requirements",
      "strengths": ["Strong ML background", "Relevant project experience"],
      "improvement_suggestions": [
        "Add certifications in AWS/GCP to close cloud skills gap",
        "Quantify achievements with metrics",
        "Add a professional summary tailored to the role"
      ]
    }}
  ],
  "summary": "Brief overall summary of the candidate pool",
  "top_recommendation": "Name of best candidate and why in 1-2 sentences"
}}

Rules:
- match_level must be one of: Excellent, Good, Average, Weak
- overall_score is 0-100
- Rank all {len(resumes)} resumes from best to worst
- Return ONLY the JSON object, nothing else
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=4096,
    )

    raw = chat_completion.choices[0].message.content.strip()

    # Clean markdown fences if any
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    return json.loads(raw)


def score_color(score: int) -> str:
    if score >= 80: return "#48c78e"
    if score >= 60: return "#64b5f6"
    if score >= 40: return "#ffb74d"
    return "#ff6464"

def pill_class(match_level: str) -> str:
    mapping = {"Excellent": "pill-excellent", "Good": "pill-good",
               "Average": "pill-average", "Weak": "pill-weak"}
    return mapping.get(match_level, "pill-average")

def rank_emoji(rank: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
api_key = "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"

with st.sidebar:
    st.markdown("## 📤 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Drop 3–5 PDF resumes here",
        type=["pdf"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        count = len(uploaded_files)
        color = "#48c78e" if 3 <= count <= 5 else "#ff6464"
        st.markdown(
            f"<p style='color:{color}; font-weight:600;'>"
            f"{'✅' if 3<=count<=5 else '⚠️'} {count} file(s) "
            f"{'(Ready!)' if 3<=count<=5 else '(Need 3–5 PDFs)'}</p>",
            unsafe_allow_html=True
        )
        for f in uploaded_files:
            st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(102,126,234,0.3),rgba(118,75,162,0.3));
border:1px solid #a78bfa; border-radius:10px; padding:8px 12px; margin:4px 0;">
<span style="color:#ffffff; font-weight:700; font-size:0.88rem;">📄 {f.name}</span>
</div>""", unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown("### ℹ️ How it works")
#     st.markdown("""
# 1. Enter your **FREE Groq API Key**
# 2. Upload **3–5 PDF** resumes
# 3. Paste the **Job Description**
# 4. Click **Analyze** and get:
#    - 📊 Skill match scores
#    - 🏆 Ranked leaderboard
#    - 💡 Improvement tips
# """)


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="stars"></div>
  <div class="hero-content">
    <div class="ai-icon">🎯</div>
    <h1>AI Resume Analyzer</h1>
    <div class="tag-line">
      <span class="tag">🧠 LLaMA 3 AI</span>
      <span class="tag">🎯 Skill Matching</span>
      <span class="tag">🏆 Smart Ranking</span>
    </div>
    <p>Upload resumes · Get instant AI analysis · Find the best candidate</p>
  </div>
</div>

<style>
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 24px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    overflow: hidden;
    border: 1px solid rgba(167,139,250,0.3);
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(102,126,234,0.15) 0%, transparent 60%);
    animation: pulse 4s ease-in-out infinite;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #a78bfa, #f64f59, #667eea);
    background-size: 200%;
    animation: shimmer 3s linear infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
@keyframes shimmer {
    0% { background-position: 0%; }
    100% { background-position: 200%; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-content {
    position: relative;
    z-index: 2;
    animation: fadeInUp 0.8s ease;
}
.ai-icon {
    font-size: 4rem;
    animation: float 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}
.hero-banner h1 {
    font-size: 3rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0.3rem 0;
    letter-spacing: -1px;
}
.tag-line {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 1rem 0;
}
.tag {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.5);
    color: #ffffff;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
}
.tag:hover {
    background: rgba(102,126,234,0.3);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102,126,234,0.4);
}
.hero-banner p {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.8rem;
    letter-spacing: 0.5px;
}
header[data-testid="stHeader"] {
    background: #0f0c29 !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">📋 Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    label="",
    height=200,
    placeholder="Paste the full job description here — include role, responsibilities, required skills, education, and experience...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🚀  Analyze Resumes with AI", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ANALYSIS
# ─────────────────────────────────────────────
if analyze_btn:
    errors = []
    if not api_key:
        errors.append("❌ Please enter your Groq API key in the sidebar.")
    if not uploaded_files or not (3 <= len(uploaded_files) <= 5):
        errors.append("❌ Please upload between 3 and 5 PDF resumes.")
    if not job_description.strip():
        errors.append("❌ Please enter a job description.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        with st.spinner("📄 Reading PDF resumes..."):
            resumes = {}
            progress = st.progress(0)
            for i, f in enumerate(uploaded_files):
                f.seek(0)
                text = extract_text_from_pdf(f)
                resumes[f.name] = text if text else f"[Could not extract text from {f.name}]"
                progress.progress((i + 1) / len(uploaded_files))
            time.sleep(0.3)
            progress.empty()

        with st.spinner("⚡AI is analyzing resumes...Please wait"):
            try:
                result = analyze_resumes_with_groq(resumes, job_description, api_key)
            except json.JSONDecodeError as e:
                st.error(f"❌ Could not parse AI response. Please try again. ({e})")
                st.stop()
            except Exception as ex:
                st.error(f"❌ API Error: {ex}")
                st.stop()

        st.success("✅ Analysis complete!")
        st.markdown("---")

        candidates = result.get("ranked_candidates", [])
        avg_score  = int(sum(c["overall_score"] for c in candidates) / len(candidates)) if candidates else 0
        top_cand   = candidates[0] if candidates else {}

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📊 Candidates Analyzed", len(candidates))
        m2.metric("🏆 Top Score",  f"{top_cand.get('overall_score', 0)}%")
        m3.metric("📈 Avg Score",  f"{avg_score}%")
        m4.metric("⭐ Best Match", top_cand.get("match_level", "—"))

        st.markdown("<br>", unsafe_allow_html=True)

        top_rec = result.get("top_recommendation", "")
        if top_rec:
            st.markdown(f"""
            <div class="card" style="border-left:4px solid #fda085; background:rgba(253,160,133,0.08);">
                <div class="section-title" style="color:#fda085;">🏆 Top Recommendation</div>
                <p style="font-size:1.05rem; color:#fff; margin:0;">{top_rec}</p>
            </div>""", unsafe_allow_html=True)

        pool_summary = result.get("summary", "")
        if pool_summary:
            st.markdown(f"""
            <div class="card">
                <div class="section-title">📝 Candidate Pool Summary</div>
                <p style="color:#ccc; margin:0;">{pool_summary}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title" style="font-size:1.6rem;">🏅 Ranked Candidates</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for cand in sorted(candidates, key=lambda x: x["rank"]):
            rank      = cand.get("rank", "?")
            name      = cand.get("name", "Candidate")
            score     = cand.get("overall_score", 0)
            level     = cand.get("match_level", "Average")
            matched   = cand.get("matched_skills", [])
            missing   = cand.get("missing_skills", [])
            strengths = cand.get("strengths", [])
            suggest   = cand.get("improvement_suggestions", [])
            exp_match = cand.get("experience_match", "")
            edu_match = cand.get("education_match", "")
            bar_color = score_color(score)

            matched_html  = "".join(f'<span class="chip-matched">{s}</span>' for s in matched)
            missing_html  = "".join(f'<span class="chip-missing">{s}</span>' for s in missing)
            strength_html = "".join(f'<div class="suggestion-item">✅ {s}</div>' for s in strengths)
            suggest_html  = "".join(f'<div class="suggestion-item">💡 {s}</div>' for s in suggest)

            st.markdown(f"""
<div class="card">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.8rem;">
    <div>
      <span style="font-size:1.3rem; font-weight:700; color:#fff;">{rank_emoji(rank)}  {name}</span>
      &nbsp;&nbsp;
      <span class="{pill_class(level)}">{level}</span>
    </div>
    <div style="text-align:right;">
      <span style="font-size:2rem; font-weight:800; color:{bar_color};">{score}%</span>
    </div>
  </div>
  <div class="score-bar-bg">
    <div class="score-bar-fill" style="width:{score}%; background:linear-gradient(90deg,{bar_color}aa,{bar_color});"></div>
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin:0.8rem 0; color:#bbb; font-size:0.88rem;">
    <div>🎓 {edu_match}</div>
    <div>💼 {exp_match}</div>
  </div>
  <div style="margin-bottom:0.6rem;">
    <div style="font-size:0.85rem; font-weight:600; color:#a0f0a0; margin-bottom:4px;">✅ Matched Skills</div>
    {matched_html if matched_html else '<span style="color:#888;font-size:0.85rem;">None identified</span>'}
  </div>
  <div style="margin-bottom:1rem;">
    <div style="font-size:0.85rem; font-weight:600; color:#f09090; margin-bottom:4px;">❌ Missing Skills</div>
    {missing_html if missing_html else '<span style="color:#888;font-size:0.85rem;">None — full match!</span>'}
  </div>
</div>
""", unsafe_allow_html=True)

            with st.expander(f"📂 View Full Analysis – {name}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**💪 Key Strengths**")
                    st.markdown(strength_html, unsafe_allow_html=True)
                with c2:
                    st.markdown("**🔧 Improvement Suggestions**")
                    st.markdown(suggest_html, unsafe_allow_html=True)

        # st.markdown("---")
        # st.download_button(
        #     label="⬇️  Download Full Analysis (JSON)",
        #     data=json.dumps(result, indent=2),
        #     file_name="resume_analysis.json",
        #     mime="application/json",
        # )

st.markdown("""
<br><hr style="border-color:rgba(255,255,255,0.08);">
<p style="text-align:center; color:#555; font-size:0.82rem;">
  AI Resume Analyzer
</p>
""", unsafe_allow_html=True)
