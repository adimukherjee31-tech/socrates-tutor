import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Neural Framework", layout="wide", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1E1E1E; color: white; }
    .main { background-color: #F0F2F6; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔬 Neural Orchestrator")
    raw_key = st.text_input("Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    
    st.divider()
    menu = ["Module 1: Discovery", "Module 2: Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Navigation", menu)
    
    if st.button("Test Connection"):
        if not gemini_key:
            st.error("Enter Key First")
        else:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_key}"
            test_res = requests.post(url, json={"contents": [{"parts": [{"text": "hi"}]}]})
            if test_res.status_code == 200:
                st.success("✅ Neural Engine Online")
            else:
                st.error(f"❌ Error {test_res.status_code}: Check your key at aistudio.google.com")

if not gemini_key:
    st.warning("Awaiting API Key...")
    st.stop()

# --- CACHED PDF PROCESSING ---
@st.cache_data(show_spinner=False)
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- STABLE NEURAL ENGINE ---
def execute_neural_query(prompt, key):
    # Using the single most stable 2026 endpoint alias
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Neural Engine Error {response.status_code}. Please ensure your API Key is unrestricted."
    except Exception as e:
        return f"❌ Network Failure: {str(e)}"

# --- MODULE 1: DISCOVERY ---
if choice == "Module 1: Discovery":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Mathematics")
        st.button("Core Computer Science")
    with col2:
        st.button("AI & Machine Learning")
        st.button("Mechanical Engineering")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI & ML", "MECH", "ECE"])
    if st.button("Synthesize") and branch:
        st.success("Roadmap Synthesized")
        st.table({"Phase": ["Foundational", "Domain", "Empirical"], "Focus": ["Theory", branch[0], "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    st.markdown("##### Paradigm: Long-Context Neural Synthesis")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        pdf_text = extract_pdf_text(file)
        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing..."):
                # Optimized for speed and cost
                prompt = f"""
                Persona: {tone}
                Context: {pdf_text[:30000]}
                Question: {query}
                End with [SOURCE: TEXTBOOK] if found.
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: Gap Analysis ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        ans = execute_neural_query(f"Identify 3 research gaps for {topic}.", gemini_key)
        st.write(ans)
