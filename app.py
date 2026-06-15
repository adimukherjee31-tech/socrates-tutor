import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Neural Framework", layout="wide", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1E1E1E; color: white; font-weight: bold; }
    .main { background-color: #F8F9FA; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Enter Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Synthesis Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)
    
    st.divider()
    debug_mode = st.checkbox("Show Neural Diagnostics")

if not gemini_key:
    st.warning("Awaiting API Key for Neural Initialization...")
    st.stop()

# --- HIGH-SPEED PDF EXTRACTION ---
@st.cache_data(show_spinner=False)
def extract_pdf_content(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- STABLE 2026 NEURAL ENGINE ---
def execute_neural_query(prompt, key):
    # Using the most robust universal endpoint for 2026
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            if debug_mode:
                st.sidebar.error(f"RAW API ERROR: {res_json}")
            return f"❌ NEURAL LINK ERROR {response.status_code}: {res_json.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"❌ TRANSPORT FAILURE: {str(e)}"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.toast("Math Logic Engine: ONLINE")
        if st.button("Learn Core CS"): st.toast("CS Systems Engine: ONLINE")
        if st.button("Learn AI & ML"): st.toast("Neural Stochastic Engine: ONLINE")
        if st.button("Learn Mechanical Engineering"): st.toast("Mech Dynamics Engine: ONLINE")
    with col2:
        st.write("### 🔗 Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Synthesis Roadmaps":
    st.title("Curriculum Synthesis Roadmap")
    exam = st.selectbox("Academic Target", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branches = st.multiselect("Core Research Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Roadmap"):
        if branches:
            st.success(f"Roadmap for {exam} Synthesized")
            st.table({"Phase": ["Foundational", "Domain Depth", "Empirical"], "Focus": ["Mathematical Logic", f"{branches[0]} Core", "Paper Review"]})
        else:
            st.warning("Please select a branch.")

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Holistic Textbook Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Pedagogical Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        pdf_text = extract_pdf_content(file)
        query = st.chat_input("Input research/conceptual query...")
        
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Analyzing Global Context..."):
                # Balanced context for speed/stability
                prompt = f"""
                Persona: {tone}
                Task: Answer from context. Use point-wise lists. 
                Context: {pdf_text[:40000]}
                Question: {query}
                Rule: If answer found, add [SOURCE: TEXTBOOK].
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain")
    if topic and st.button("Generate Gap Synthesis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"Identify 3 unique research gaps for: {topic}.", gemini_key)
            st.write(ans)
