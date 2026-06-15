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

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Enter Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)

if not gemini_key:
    st.warning("Awaiting API Key for Neural Initialization...")
    st.stop()

# --- HIGH-SPEED PDF EXTRACTION ---
@st.cache_data(show_spinner=False)
def extract_pdf_content(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- NEURAL NEGOTIATION ENGINE (The 404 Fix) ---
def execute_neural_query(prompt, key):
    # This list covers all possible stable and beta endpoints for Gemini Flash/Pro in 2026
    strategies = [
        ("v1", "gemini-1.5-flash"),
        ("v1beta", "gemini-1.5-flash-latest"),
        ("v1", "gemini-1.5-pro"),
        ("v1beta", "gemini-pro")
    ]
    
    last_error = ""
    for ver, mod in strategies:
        url = f"https://generativelanguage.googleapis.com/{ver}/models/{mod}:generateContent?key={key}"
        try:
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                last_error = f"{mod} ({ver}): {response.status_code}"
        except:
            continue
            
    return f"❌ NEURAL LINK ERROR: All endpoints failed. (Last Attempt: {last_error}). Please ensure your Gemini Key is active."

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.toast("Math Logic Engine: Ready")
        if st.button("Learn Core CS"): st.toast("CS Systems Engine: Ready")
        if st.button("Learn AI & ML"): st.toast("AI Models Engine: Ready")
        if st.button("Learn Mechanical Engineering"): st.toast("Mech Dynamics Engine: Ready")
    with col2:
        st.write("### 🔗 Interdisciplinary Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Target Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch = st.multiselect("Select Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Roadmap Generated for {exam}")
        st.table({"Phase": ["Theory", "Specialization", "Practice"], "Focus": ["Mathematical Foundations", f"{branch[0]} Core", "PYQs & Mock Tests"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Pedagogical Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        pdf_text = extract_pdf_content(file)
        query = st.chat_input("Ask any concept query from the book...")
        
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing from Context..."):
                # Using 40,000 characters for chapter-level research depth
                prompt = f"""
                Persona: {tone}
                Task: Grounded synthesis from context. Answer questions comprehensively. 
                Instruction: If found in context, conclude with [SOURCE: TEXTBOOK]. 
                
                CONTEXT: {pdf_text[:40000]}
                QUESTION: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Research Domain")
    if topic and st.button("Synthesize Research Gaps"):
        with st.spinner("Analyzing Frontiers..."):
            ans = execute_neural_query(f"Identify 3 novel research gaps for the topic: {topic}. Provide a brief PhD-level justification for each.", gemini_key)
            st.write(ans)
