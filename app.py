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

if not gemini_key:
    st.warning("Awaiting API Key...")
    st.stop()

# --- CACHED PDF PROCESSING ---
@st.cache_data(show_spinner=False)
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

# --- PHuD-LEVEL NEURAL FALLBACK ENGINE ---
def execute_neural_query(prompt, key):
    # We try different versions and models to ensure zero failure
    # Version v1beta is often required for the latest Flash models
    strategies = [
        {"ver": "v1beta", "mod": "gemini-1.5-flash"},
        {"ver": "v1", "mod": "gemini-pro"},
        {"ver": "v1beta", "mod": "gemini-1.5-pro"}
    ]
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    for strategy in strategies:
        url = f"https://generativelanguage.googleapis.com/{strategy['ver']}/models/{strategy['mod']}:generateContent?key={key}"
        try:
            response = requests.post(url, headers=headers, json=data, timeout=45)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return "❌ SYSTEM ERROR: The Neural Engine could not be reached. Please check your API Key permissions or regional access."

# --- MODULE 1: DISCOVERY ---
if choice == "Module 1: Discovery":
    st.title("🎓 Socrates: Discovery Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Mathematics")
        st.button("Core Computer Science")
    with col2:
        st.button("AI & Machine Learning")
        st.button("Mechanical Intelligence")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Roadmaps":
    st.title("Academic Roadmap Synthesis")
    exam = st.selectbox("Exam", ["GATE", "UGC NET", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Branches", ["CSE", "AI & ML", "MECH", "ECE"])
    if st.button("Synthesize") and branch:
        st.table({"Phase": ["Foundational", "Domain", "Empirical"], "Focus": ["Theory", branch[0], "Paper Review"]})

# --- MODULE 4: TEXTBOOK AGENT ---
elif choice == "Module 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    st.markdown("##### Framework: Long-Context Neural Synthesis")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        pdf_text = extract_pdf_text(file)
        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Executing Neural Synthesis..."):
                # Using 40k characters for ultra-fast, stable 2026 performance
                prompt = f"""
                Persona: {tone}
                Task: Answer using the TEXTBOOK CONTEXT below. 
                Reference specific facts from the context.
                End with [SOURCE: VERIFIED TEXTBOOK] if the answer is found in the text.
                
                TEXTBOOK CONTEXT: {pdf_text[:40000]}
                
                QUESTION: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Re
