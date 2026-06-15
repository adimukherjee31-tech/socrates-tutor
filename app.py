import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 PhD RESEARCH CONFIG ---
st.set_page_config(page_title="Socrates: Pedagogical AI", layout="wide", page_icon="🎓")

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
    api_key = raw_key.strip()
    
    st.divider()
    menu = ["Page 1: Discovery Hub", "Page 2: Exam Roadmaps", "Page 4: Textbook Agent", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key to initialize the Neural Engine.")
    st.stop()

# --- THE NEURAL RESILIENCE LAYER (The Fix) ---
def execute_neural_query(prompt, key):
    # This list covers all possible 2026 stable and beta endpoints
    # It tries the most likely ones first
    configurations = [
        ("v1", "gemini-1.5-flash"),
        ("v1beta", "gemini-1.5-flash-latest"),
        ("v1", "gemini-pro"),
        ("v1beta", "gemini-1.5-pro")
    ]
    
    last_error = ""
    for version, model in configurations:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={key}"
        try:
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                last_error = f"{model} ({version}): {response.status_code}"
        except:
            continue
            
    return f"❌ NEURAL LINK ERROR: All endpoints failed. (Last Attempt: {last_error}). Please verify your API Key permissions at aistudio.google.com."

# --- PAGE 1: DISCOVERY HUB ---
if choice == "Page 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        st.button("Learn Math")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.write("### 🔗 Intersections")
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Target Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM", "CUET"])
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Research Branches", branch_list)
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Roadmap for {exam} Synthesized")
        st.table({"Phase": ["Theory", "Domain", "Practice"], "Focus": ["Foundational Logic", f"{branch[0]} Core", "Paper Review"]})

# --- PAGE 4: TEXTBOOK AGENT ---
elif choice == "Page 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        if "pdf_text" not in st.session_state:
            with st.spinner("Extracting Global Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_text = "".join([page.get_text() for page in doc])
                st.success("Global Context Cached.")

        query = st.chat_input("Ask a conceptual query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing..."):
                prompt = f"""
                Persona: {tone}.
                Instruction: Answer from context. Use [SOURCE: TEXTBOOK] if found.
                CONTEXT: {st.session_state.pdf_text[:30000]}
                QUESTION: {query}
                """
                response = execute_neural_query(prompt, api_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain")
    if topic and st.button("Generate Gap Synthesis"):
        ans = execute_neural_query(f"Identify 3 unique research gaps for: {topic}.", api_key)
        st.write(ans)
