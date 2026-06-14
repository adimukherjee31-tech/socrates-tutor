import streamlit as st
import requests
import fitz  # PyMuPDF
import os

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

# --- THE AUTO-NEGOTIATOR (PhD Level Resilience) ---
def call_socrates(prompt, key):
    # This cycles through all possible 2026 endpoints to bypass 404 errors
    attempts = [
        ("v1", "gemini-1.5-flash"),        # Stable Release
        ("v1beta", "gemini-1.5-flash"),   # Beta Release
        ("v1beta", "gemini-1.5-flash-latest"), # Latest Alias
        ("v1", "gemini-pro")               # Pro Fallback
    ]
    
    last_err = ""
    for ver, mod in attempts:
        url = f"https://generativelanguage.googleapis.com/{ver}/models/{mod}:generateContent?key={key}"
        try:
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=25)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                last_err = f"{response.status_code}: {response.text[:100]}"
        except:
            continue
            
    return f"❌ NEURAL ERROR: Could not negotiate connection. Last error: {last_err}. Check your key at aistudio.google.com"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    st.subheader("Interdisciplinary Learning Verticals")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.success("Math Logic Engine: ONLINE")
        if st.button("Learn Core CS"): st.success("CS Systems Engine: ONLINE")
        if st.button("Learn AI & ML"): st.success("Neural Stochastic Engine: ONLINE")
        if st.button("Learn Mechanical Engineering"): st.success("Mech Dynamics Engine: ONLINE")
    with col2:
        st.write("### 🔗 Intersections")
        if st.button("AI & Physics"): st.info("Synthesizing...")
        if st.button("CS & EE"): st.info("Synthesizing...")
        if st.button("AI, CS & ECE"): st.info("Synthesizing...")
        if st.button("Mechanical & AI"): st.info("Synthesizing...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM", "CUET"])
    # Full branch list as requested
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Select Branch", branch_list)
    if st.button("Synthesize Roadmap") and branch:
        st.table({"Phase": ["Theory", "Domain", "Practice"], "Focus": ["Foundational Logic", f"{branch[0]} Architecture", "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        if "pdf_data" not in st.session_state:
            with st.spinner("Extracting Global Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_data = "".join([page.get_text() for page in doc])
                st.success("Textbook Indexed!")

        query = st.chat_input("Ask a question from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Socrates is analyzing..."):
                # Use 20k characters for high stability and speed
                prompt = f"""
                Persona: {tone}
                Task: Answer from context. Use point-wise lists and relevant emojis/stickers.
                Context: {st.session_state.pdf_data[:20000]}
                Question: {query}
                
                If found in context, end with [SOURCE: TEXTBOOK]. 
                If general knowledge, start with [SOURCE: GENERAL AI].
                """
                answer = call_socrates(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(answer)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    if topic and st.button("Analyze Gaps"):
        ans = call_socrates(f"Identify 3 novel research gaps for: {topic}.", gemini_key)
        st.write(ans)
