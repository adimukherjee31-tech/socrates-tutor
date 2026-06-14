import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Pedagogical Framework", layout="wide", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1E1E1E; color: white; font-weight: bold; }
    .main { background-color: #F0F2F6; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    st.info("Paradigm: Holistic Contextual Synthesis (2026 Standard)")
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Synthesis Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Active Module", menu)

if not gemini_key:
    st.warning("Awaiting API Key for Neural Initialization...")
    st.stop()

# --- STABLE NEURAL ENGINE (v1 Endpoint) ---
def execute_neural_query(prompt, key):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=45)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = res_json.get('error', {}).get('message', 'API Error')
            return f"❌ NEURAL ERROR {response.status_code}: {error_msg}"
    except Exception as e:
        return f"❌ TRANSPORT FAILURE: {str(e)}"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Interdisciplinary Learning Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.toast("Logic Engine: Math Ready")
        if st.button("Learn Core CS"): st.toast("Logic Engine: CS Ready")
        if st.button("Learn AI & ML"): st.toast("Logic Engine: AI Ready")
        if st.button("Learn Mechanical Engineering"): st.toast("Logic Engine: Mech Ready")
    with col2:
        st.write("### 🔗 Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing Intersection...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing Intersection...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing Intersection...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing Intersection...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Synthesis Roadmaps":
    st.title("Curriculum Synthesis Roadmap")
    exam = st.selectbox("Academic Target", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branches = st.multiselect("Core Research Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Academic Roadmap"):
        if branches:
            st.success(f"Roadmap for {exam} ({', '.join(branches)}) Synthesized")
            st.table({"Phase": ["Theory", "Domain", "Practice"], "Focus": ["Math", f"{branches[0]} Core", "PYQs"]})
        else:
            st.warning("Please select at least one branch.")

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Holistic Textbook Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Pedagogical Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        if "pdf_text" not in st.session_state:
            with st.spinner("Extracting Global Semantic Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_text = "".join([page.get_text() for page in doc])
                st.success("Global Context Cached.")

    query = st.chat_input("Input research/conceptual query...")
    if query:
        if "pdf_text" not in st.session_state:
            st.error("Please upload a PDF first!")
        else:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Socrates is analyzing..."):
                prompt = f"""
                Persona: {tone}
                Task: Pedagogical synthesis from context. Use point-wise lists and stickers/emojis as requested.
                
                Protocol:
                1. Use the [TEXTBOOK CONTEXT] provided below.
                2. If answer found: End with [SOURCE: VERIFIED TEXTBOOK].
                3. If extrapolated: Start with [SOURCE: PARAMETRIC AI KNOWLEDGE].
                
                TEXTBOOK CONTEXT: {st.session_state.pdf_text[:300000]}
                
                USER QUERY: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain")
    if topic and st.button("Generate Gap Synthesis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"Identify 3 novel research gaps for: {topic}.", gemini_key)
            st.write(ans)
