import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Neural Framework", layout="wide", page_icon="🎓")

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

# --- CACHED PDF PROCESSING ---
@st.cache_data(show_spinner=False)
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- NEURAL FALLBACK ENGINE ---
def execute_neural_query(prompt, key):
    strategies = [
        {"ver": "v1beta", "mod": "gemini-1.5-flash"},
        {"ver": "v1", "mod": "gemini-pro"},
        {"ver": "v1beta", "mod": "gemini-1.5-pro"}
    ]
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    for strategy in strategies:
        url = f"https://generativelanguage.googleapis.com/{strategy['ver']}/models/{strategy['mod']}:generateContent?key={key}"
        try:
            response = requests.post(url, headers=headers, json=data, timeout=45)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "❌ SYSTEM ERROR: The Neural Engine could not be reached. Verify your Key or Network."

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        st.button("Mathematics")
        st.button("Core Computer Science")
        st.button("AI & Machine Learning")
        st.button("Mechanical Engineering")
    with col2:
        st.write("### 🔗 Intersections")
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Select Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Select Branch", ["CSE", "AI & ML", "MECH", "ECE", "EEE"])
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Optimized Roadmap for {exam} Generated")
        st.table({"Phase": ["Foundational", "Core Domain", "Empirical"], "Focus": ["Mathematical Logic", f"{branch[0]} Core", "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    st.markdown("##### Paradigm: Long-Context Neural Synthesis")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Pedagogical Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        pdf_text = extract_pdf_text(file)
        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing..."):
                prompt = f"""
                Persona: {tone}
                Context: {pdf_text[:40000]}
                Question: {query}
                Rule: Use [SOURCE: TEXTBOOK] if answer is in context.
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Research Domain")
    if topic and st.button("Generate Gap Analysis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"As a PhD supervisor, identify 3 novel research gaps for the topic: {topic}.", gemini_key)
            st.write(ans)
