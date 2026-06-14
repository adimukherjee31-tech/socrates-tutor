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
    .main { background-color: #F0F2F6; }
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

if not gemini_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# --- HIGH-SPEED PDF EXTRACTION ---
@st.cache_data(show_spinner=False)
def extract_pdf_content(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- THE NEURAL NEGOTIATION LAYER (PhD Level Resilience) ---
def execute_neural_query(prompt, key):
    # We attempt multiple stable endpoints and model aliases to ensure success
    endpoints = [
        "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    ]
    
    for url in endpoints:
        try:
            full_url = f"{url}?key={key}"
            response = requests.post(
                full_url, 
                json={"contents": [{"parts": [{"text": prompt}]}]}, 
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return "❌ NEURAL LINK FAILURE: The system could not negotiate a stable connection with the Gemini Cluster. Verify your key at aistudio.google.com."

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    st.subheader("Interdisciplinary Learning Verticals")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Learn Math")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Synthesis Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH"])
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Roadmap Synthesized for {exam}")
        st.table({"Phase": ["Foundational", "Domain Depth", "Practice"], "Focus": ["Math Logic", f"{branch[0]} Core", "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    st.markdown("##### Framework: Holistic Contextual Synthesis")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        pdf_text = extract_pdf_content(file)
        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Analyzing context..."):
                # Using 30k chars for high speed and stability
                prompt = f"""
                Persona: {tone}
                Task: Answer from context. Use point-wise lists. 
                If found in context, add [SOURCE: TEXTBOOK].
                
                CONTEXT: {pdf_text[:30000]}
                QUESTION: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    if topic and st.button("Generate Gaps"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"Identify 3 novel research gaps for the topic: {topic}.", gemini_key)
            st.write(ans)
