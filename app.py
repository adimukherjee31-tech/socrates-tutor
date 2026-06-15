import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- 2026 PhD RESEARCH CONFIG ---
st.set_page_config(page_title="Socrates: Pedagogical Framework", layout="wide")

# --- UI STYLING ---
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
    
    if st.button("Check Connection"):
        if not api_key:
            st.error("Please enter a key first.")
        else:
            # Pinging the most stable 2026 beta endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": "hi"}]}]}, timeout=10)
                if res.status_code == 200:
                    st.success("✅ Neural Engine: ONLINE")
                else:
                    st.error(f"❌ API Error {res.status_code}: {res.json()['error']['message']}")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")

    st.divider()
    menu = ["Page 1: Discovery Hub", "Page 2: Exam Roadmaps", "Page 4: Textbook Agent", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key to initialize the Neural Engine.")
    st.stop()

# --- STABLE NEURAL ENGINE ---
def execute_neural_query(prompt, key):
    # Using the v1beta endpoint which is the current 2026 research standard
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Neural Error {response.status_code}: {response.json()['error']['message']}"
    except Exception as e:
        return f"❌ System Error: {str(e)}"

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
    exam = st.selectbox("Select Target Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch = st.multiselect("Select Branch", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Generate Roadmap") and branch:
        st.success(f"Roadmap for {exam} ({', '.join(branch)}) Synthesized")
        st.table({"Phase": ["Foundational", "Domain Depth", "Practice"], "Focus": ["Math Logic", f"{branch[0]} Core", "Paper Review"]})

# --- PAGE 4: TEXTBOOK AGENT ---
elif choice == "Page 4: Textbook Agent":
    st.title("🔍 Intelligent Research Assistant")
    file = st.file_uploader("Upload Pedagogical Source (PDF)", type="pdf")
    tone = st.selectbox("Style", ["Professor Tone", "Munnabhai (Hinglish)", "Simple (ELI5)"])
    
    if file:
        if "pdf_text" not in st.session_state:
            with st.spinner("Analyzing Global Context..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                st.session_state.pdf_text = "".join([page.get_text() for page in doc])
                st.success("Global Context Cached.")

        query = st.chat_input("Ask a question about any concept in the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            with st.spinner("Synthesizing..."):
                # Using 30k chars for high speed and 2026 cloud stability
                prompt = f"""
                Persona: {tone}
                Task: Pedagogical synthesis from context.
                Context: {st.session_state.pdf_text[:30000]}
                Question: {query}
                Rule: If answer is in context, end with [SOURCE: TEXTBOOK].
                """
                response = execute_neural_query(prompt, api_key)
                with st.chat_message("assistant"): st.markdown(response)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Domain")
    if topic and st.button("Generate Gap Synthesis"):
        with st.spinner("Scanning Research Frontiers..."):
            ans = execute_neural_query(f"PhD Level: Identify 3 research gaps for: {topic}.", api_key)
            st.write(ans)
