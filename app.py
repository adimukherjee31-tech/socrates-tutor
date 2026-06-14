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

# --- SIDEBAR: SYSTEM ORCHESTRATION ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    gemini_key = st.text_input("Gemini 1.5 SOTA API Key", type="password")
    st.info("Environment: Python 3.14 \nParadigm: Holistic Contextual Synthesis")
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Synthesis Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Active Module", menu)

if not gemini_key:
    st.warning("Awaiting API Key for Neural Initialization...")
    st.stop()

# --- STABLE NEURAL CALL (Direct 2026 Standard) ---
def execute_neural_query(prompt, key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "CRITICAL ERROR: Neural Link Failed. Verify API Credentials."

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Interdisciplinary Learning Hub")
    st.subheader("Pedagogical Discovery Verticals")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Mathematics"): st.toast("Initializing Logic Engine...")
        if st.button("Learn Core CS"): st.toast("Initializing Systems Engine...")
        if st.button("Learn AI & ML"): st.toast("Initializing Stochastic Engine...")
        if st.button("Learn Mechanical Engineering"): st.toast("Initializing Dynamics Engine...")
    with col2:
        st.write("### 🔗 Interdisciplinary Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing Neural-Physics...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing Edge Intelligence...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing VLSI-AI...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing Generative Design...")

# --- MODULE 2: SYNTHESIS ROADMAPS ---
elif choice == "Module 2: Synthesis Roadmaps":
    st.title("Curriculum Synthesis Roadmap")
    exam = st.selectbox("Academic Target", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    # Branches updated per 2026 CSE/AI requirements
    branches = st.multiselect("Core Research Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Academic Roadmap"):
        if branches:
            st.success(f"Optimized Roadmap for {exam} ({', '.join(branches)})")
            st.table({
                "Phase": ["Foundational Theory", "Domain Specialization", "Empirical Evaluation"], 
                "Focus": ["Mathematical Logic & Probability", f"{branches[0]} SOTA Architecture", "Benchmarking & Paper Review"]
            })

# --- MODULE 4: TEXTBOOK AGENT (THE INNOVATION) ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Holistic Textbook Assistant")
    st.markdown("##### Research Paradigm: Direct High-Fidelity Context Injection")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Pedagogical Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        if "pdf_content" not in st.session_state:
            with st.spinner("Extracting Global Semantic Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_content = "".join([page.get_text() for page in doc])
                st.success("Global Context Cached.")

        query = st.chat_input("Input research/conceptual query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Analyzing Global Context..."):
                # 2026 GROUNDING PROMPT
                prompt = f"""
                Persona: {tone}
                Goal: Pedagogy-first synthesis from provided context.
                
                Protocol:
                1. Use the [TEXTBOOK CONTEXT] to answer. 
                2. If answer found: Conclude with [SOURCE: VERIFIED TEXTBOOK].
                3. If answer extrapolated: Start with [SOURCE: PARAMETRIC AI KNOWLEDGE].
                
                TEXTBOOK CONTEXT: {st.session_state.pdf_text[:450000]}
                
                USER QUERY: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain (e.g., Federated Learning in IoT)")
    if topic and st.button("Generate Gap Synthesis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"Identify 3 novel research gaps and a problem statement for: {topic}.", gemini_key)
            st.write(ans)
