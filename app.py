import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# 1. IMMEDIATE CONFIG (Must be first)
st.set_page_config(page_title="Socrates AI", layout="wide")

# 2. LIGHTWEIGHT THEME
st.markdown("<style>.stButton>button{width:100%;height:3em;font-weight:bold;}</style>", unsafe_allow_html=True)

# 3. SYSTEM STATE
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# 4. SIDEBAR SETUP
with st.sidebar:
    st.title("🔬 Neural Engine")
    key = st.text_input("Enter Gemini API Key", type="password").strip()
    st.divider()
    page = st.radio("Navigation", ["Home", "Roadmaps", "Textbook AI", "Research Gaps"])
    
    if key:
        st.success("System: Ready ✅")
    else:
        st.warning("System: Awaiting Key 🔑")

# 5. BRAIN FUNCTION (API DIRECT)
def ask_ai(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "❌ Engine error. Please retry."

# 6. APP MODULES
if not key:
    st.info("🎓 Welcome to Socrates AI. Please enter your API key in the sidebar to begin your research session.")
    st.stop()

if page == "Home":
    st.title("🎓 Socrates: Discovery Hub")
    c1, c2 = st.columns(2)
    with c1:
        st.button("Mathematics")
        st.button("Core CS")
        st.button("AI & ML")
        st.button("Mechanical Engineering")
    with c2:
        st.button("AI + Physics")
        st.button("CS + EE")
        st.button("AI + ECE")
        st.button("Mech + AI")

elif page == "Roadmaps":
    st.title("📋 Curriculum Synthesis")
    exam = st.selectbox("Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI", "EEE", "ECE", "MECH"])
    if st.button("Generate") and branch:
        st.table({"Phase": ["Theory", "Domain", "Empirical"], "Focus": ["Math", branch[0], "Paper Review"]})

elif page == "Textbook AI":
    st.title("🔍 Textbook Agent")
    file = st.file_uploader("Upload PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor", "Munnabhai", "Simple"])
    
    if file:
        if not st.session_state.pdf_text:
            with st.spinner("Reading..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_text = "".join([page.get_text() for page in doc])
        
        query = st.chat_input("Ask a question...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Analyzing..."):
                # 30k context for maximum speed in 2026 environment
                prompt = f"Tone: {tone}. Context: {st.session_state.pdf_text[:30000]}. Question: {query}. End with [SOURCE: TEXTBOOK]."
                res = ask_ai(prompt, key)
                with st.chat_message("assistant"): st.markdown(res)

elif page == "Research Gaps":
    st.title("🔬 Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        with st.spinner("Scanning..."):
            res = ask_ai(f"Identify 3 research gaps for: {topic}", key)
            st.write(res)
