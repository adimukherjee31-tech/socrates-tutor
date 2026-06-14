import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 RESEARCH CONFIG ---
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

# --- STABLE NEURAL ENGINE (60s Timeout) ---
def execute_neural_query(prompt, key):
    # Stable v1 endpoint for 2026 Production Standards
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
    try:
        # Increased timeout to 60s for Long-Context processing
        response = requests.post(
            url, 
            json={"contents": [{"parts": [{"text": prompt}]}]}, 
            timeout=60 
        )
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Neural Error: {response.status_code}. Try a shorter query."
    except Exception as e:
        return f"❌ Transport Failure: System is overloaded. Please try again in 10 seconds."

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
    st.markdown("##### Framework: Long-Context Semantic Synthesis")
    file = st.file_uploader("Upload Pedagogical PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple"])
    
    if file:
        pdf_text = extract_pdf_text(file)
        query = st.chat_input("Ask a concept query...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing from Global Context..."):
                # Using 50k chars for high speed + high research fidelity
                prompt = f"""
                Persona: {tone}
                Instruction: Answer using the TEXTBOOK CONTEXT provided. 
                Use [SOURCE: TEXTBOOK] if found.
                
                TEXTBOOK CONTEXT: {pdf_text[:50000]}
                
                QUESTION: {query}
                """
                response = execute_neural_query(prompt, gemini_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Module 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Research Domain")
    if topic and st.button("Generate Gaps"):
        with st.spinner("Analyzing SOTA..."):
            ans = execute_neural_query(f"Identify 3 novel research gaps for: {topic}.", gemini_key)
            st.write(ans)
