import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 RESEARCH ARCHITECTURE ---
st.set_page_config(page_title="Socrates AI: Neural Framework", layout="wide", page_icon="🎓")

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
    gemini_key = raw_key.strip()
    
    if gemini_key:
        st.success("Neural Heartbeat: OK ✅")
    else:
        st.warning("Neural Heartbeat: OFFLINE ❌")

    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)

if not gemini_key:
    st.info("Awaiting API Key for system initialization...")
    st.stop()

# --- HIGH-SPEED NEURAL ENGINE ---
def execute_query(prompt, key):
    # Uses the stable 2026 production endpoint
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Fallback to beta if stable is congested
            url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            response = requests.post(url_beta, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "❌ Neural Link Failure. Please retry the query."

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Discovery Hub")
    st.subheader("Interdisciplinary Knowledge Verticals")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Learn Mathematics")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Curriculum Synthesis Roadmap")
    exam = st.selectbox("Select Target", ["GATE", "UGC NET", "CSIR NET", "IIT JAM", "CUET"])
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Research Branches", branch_list)
    if st.button("Synthesize Roadmap") and branch:
        st.success(f"Roadmap for {exam} Synthesized")
        st.table({"Phase": ["Theory", "Domain", "Practice"], "Focus": ["Foundational Logic", f"{branch[0]} Core", "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    st.markdown("##### Paradigm: Holistic Contextual Synthesis")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        if "cached_text" not in st.session_state:
            with st.spinner("Indexing Global Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.cached_text = "".join([page.get_text() for page in doc])
                st.success("Context Cached!")

        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing..."):
                prompt = f"""
                Style: {tone}.
                Instruction: Answer using the TEXTBOOK CONTEXT. 
                Use [SOURCE: TEXTBOOK] if found.
                CONTEXT: {st.session_state.cached_text[:30000]}
                QUESTION: {query}
                """
                response = execute_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain")
    if topic and st.button("Generate Gaps"):
        with st.spinner("Scanning SOTA..."):
            ans = execute_query(f"Identify 3 unique research gaps for: {topic}.", gemini_key)
            st.write(ans)
