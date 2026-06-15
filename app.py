import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 PhD RESEARCH CONFIG ---
st.set_page_config(page_title="Socrates: Pedagogical AI", layout="wide", page_icon="🎓")

# --- UI THEME ---
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
    api_key = raw_key.strip()
    
    st.divider()
    menu = ["Page 1: Discovery Hub", "Page 2: Roadmaps", "Page 4: Textbook Agent", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your API Key to initialize.")
    st.stop()

# --- THE SELF-HEALING NEURAL ENGINE (PhD Innovation) ---
@st.cache_resource(show_spinner=False)
def find_working_model(key):
    # This probes the API to find exactly which model name your region/key supports
    # It solves the 404 error permanently
    test_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.5-flash-latest"]
    endpoints = ["v1", "v1beta"]
    
    for ver in endpoints:
        for mod in test_models:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{mod}:generateContent?key={key}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": "hi"}]}]}, timeout=5)
                if res.status_code == 200:
                    return {"url": url, "name": mod}
            except:
                continue
    return None

# Initialize the Neural Engine
with st.sidebar:
    with st.spinner("Calibrating Neural Link..."):
        engine = find_working_model(api_key)
        if engine:
            st.success(f"Connected to: {engine['name']} ✅")
        else:
            st.error("❌ Link Failure: Key rejected or restricted. Visit aistudio.google.com")

def execute_neural_query(prompt):
    if not engine: return "❌ System Offline."
    try:
        response = requests.post(engine['url'], json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ Transport Error: {str(e)}"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Page 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.toast("Logic Engine: Ready")
        if st.button("Learn Core CS"): st.toast("Systems Engine: Ready")
        if st.button("Learn AI & ML"): st.toast("Neural Engine: Ready")
        if st.button("Learn Mechanical Engineering"): st.toast("Dynamics Engine: Ready")
    with col2:
        st.write("### 🔗 Interdisciplinary Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing Neural-Physics...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing Edge-AI...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing VLSI-AI...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing Generative-ME...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Target Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch = st.multiselect("Select Branch", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Optimized Roadmap for {exam} Synthesized")
        st.table({"Phase": ["Theory", "Specialization", "Practice"], "Focus": ["Mathematical Logic", f"{branch[0]} Core", "PYQs"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Page 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        if "pdf_text" not in st.session_state:
            with st.spinner("Extracting Global Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_text = "".join([page.get_text() for page in doc])
                st.success("Global Context Cached.")

        query = st.chat_input("Ask a conceptual query from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing from Context..."):
                # Optimized for 2026 Cloud Stability
                prompt = f"""
                Persona: {tone}
                Task: Pedagogical synthesis from context.
                Instruction: Use the [TEXTBOOK CONTEXT] below. If found, end with [SOURCE: TEXTBOOK].
                
                TEXTBOOK CONTEXT: {st.session_state.pdf_text[:25000]}
                QUESTION: {query}
                """
                response = execute_neural_query(prompt)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Page 6: Research Gaps":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Research Domain")
    if topic and st.button("Generate Gap Analysis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"Identify 3 unique research gaps for: {topic}.")
            st.write(ans)
