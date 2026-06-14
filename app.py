import streamlit as st
import requests
import fitz  # PyMuPDF
import json

# --- RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Neural Framework", layout="wide", page_icon="🎓")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Enter Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)

if not gemini_key:
    st.warning("Please enter your API Key to initialize.")
    st.stop()

# --- STABLE 2026 NEURAL CALL ---
def call_socrates(prompt, key):
    # This is the most stable 2026 endpoint for the Flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Neural Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ System Error: {str(e)}"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.success("Math Logic Online")
        if st.button("Learn Core CS"): st.success("CS Systems Online")
        if st.button("Learn AI & ML"): st.success("Neural Stochastic Online")
        if st.button("Learn Mechanical Engineering"): st.success("Mechanical Dynamics Online")
    with col2:
        st.write("### 🔗 Interdisciplinary Intersections")
        if st.button("AI & Physics"): st.info("Synthesizing...")
        if st.button("CS & EE"): st.info("Synthesizing...")
        if st.button("AI, CS & ECE"): st.info("Synthesizing...")
        if st.button("Mechanical & AI"): st.info("Synthesizing...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI & ML", "MECH", "ECE", "EEE"])
    if st.button("Synthesize Roadmap") and branch:
        st.table({"Phase": ["Theory", "Core", "Practice"], "Focus": ["Math Logic", f"{branch[0]} Architecture", "PYQ Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        if "pdf_data" not in st.session_state:
            with st.spinner("Indexing Textbook..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_data = "".join([page.get_text() for page in doc])
                st.success("Context Cached!")

        query = st.chat_input("Ask about Chapter 2 or any concept...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Socrates is thinking..."):
                # Using 20,000 characters for maximum reliability and speed
                context = st.session_state.pdf_data[:20000]
                prompt = f"""
                Persona: {tone}
                Task: Answer from context. Use point-wise lists and emojis/stickers.
                Context: {context}
                Question: {query}
                Rule: If answer is in context, add [SOURCE: TEXTBOOK].
                """
                answer = call_socrates(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(answer)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Research Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        ans = call_socrates(f"Identify 3 novel research gaps for: {topic}.", gemini_key)
        st.write(ans)
