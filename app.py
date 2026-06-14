import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- PERFORMANCE CONFIG ---
st.set_page_config(page_title="Socrates AI: High-Performance Framework", layout="wide", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1E1E1E; color: white; }
    .main { background-color: #F0F2F6; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    
    st.divider()
    menu = ["Module 1: Discovery", "Module 2: Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)

if not gemini_key:
    st.warning("Awaiting API Key...")
    st.stop()

# --- OPTIMIZED CACHING FOR SPEED ---
@st.cache_data(show_spinner=False)
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    return text

# --- FAIL-SAFE NEURAL ENGINE ---
def execute_neural_query(prompt, key):
    models = ["gemini-1.5-flash", "gemini-pro"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        try:
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "❌ Connection Timeout. Please try again."

# --- MODULE 1: DISCOVERY ---
if choice == "Module 1: Discovery":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Math")
        st.button("Core CS")
    with col2:
        st.button("AI & ML")
        st.button("Mechanical AI")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Curriculum Synthesis")
    exam = st.selectbox("Target Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI & ML", "MECH", "MATH"])
    if st.button("Synthesize Roadmap") and branch:
        st.table({"Phase": ["Theory", "Core", "Practice"], "Focus": ["Foundational", f"{branch[0]}", "PYQs"]})

# --- MODULE 4: TEXTBOOK AGENT (SPEED OPTIMIZED) ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 High-Performance Textbook Assistant")
    file = st.file_uploader("Upload PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        # Fast extraction using cache
        pdf_text = extract_pdf_text(file)
        
        query = st.chat_input("Ask a question...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Analyzing..."):
                # Using 100k characters for balance of speed and PhD-level context
                prompt = f"Style: {tone}. Context: {pdf_text[:100000]}. Question: {query}. End with [SOURCE: TEXTBOOK] if found."
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Research Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        ans = execute_neural_query(f"Find 3 research gaps for {topic}.", gemini_key)
        st.write(ans)
