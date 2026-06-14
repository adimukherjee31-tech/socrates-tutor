import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# --- RESEARCH FRAMEWORK CONFIG ---
st.set_page_config(page_title="Socrates AI: Pedagogical Framework", layout="wide", page_icon="🎓")

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
    raw_key = st.text_input("Gemini API Key", type="password")
    gemini_key = raw_key.strip() 
    st.info("Paradigm: Holistic Contextual Synthesis (2026 Standard)")
    
    st.divider()
    menu = ["Module 1: Discovery Hub", "Module 2: Synthesis Roadmaps", "Module 4: Textbook Agent", "Module 6: Gap Analysis"]
    choice = st.selectbox("Active Module", menu)

if not gemini_key:
    st.warning("Awaiting API Key for Neural Initialization...")
    st.stop()

# --- STABLE NEURAL ENGINE (v1 Endpoint) ---
def execute_neural_query(prompt, key):
    # THE FIX: Switched from v1beta to v1 (Stable 2026 Endpoint)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=45)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = res_json.get('error', {}).get('message', 'API Error')
            return f"❌ NEURAL ERROR {response.status_code}: {error_msg}"
    except Exception as e:
        return f"❌ TRANSPORT FAILURE: {str(e)}"

# --- MODULE 1: DISCOVERY HUB ---
if choice == "Module 1: Discovery Hub":
    st.title("🎓 Socrates: Interdisciplinary Learning Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Disciplines")
        if st.button("Learn Math"): st.toast("Logic Engine: Math Ready")
        if st.button("Learn Core CS"): st.toast("Logic Engine: CS Ready")
        if st.button("Learn AI & ML"): st.toast("Logic Engine: AI Ready")
        if st.button("Learn Mechanical Engineering"): st.toast("Logic Engine: Mech Ready")
    with col2:
        st.write("### 🔗 Intersections")
        if st.button("AI & Physics Intersection"): st.toast("Synthesizing...")
        if st.button("CS & EE Intersection"): st.toast("Synthesizing...")
        if st.button("AI, CS & ECE Intersection"): st.toast("Synthesizing...")
        if st.button("Mechanical & AI Intersection"): st.toast("Synthesizing...")

# --- MODULE 2: ROADMAPS ---
elif choice == "Module 2: Synthesis Roadmaps":
    st.title("Curriculum Synthesis Roadmap")
    exam = st.selectbox("Academic Target", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branches = st.multiselect("Core Research Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Synthesize Academic Roadmap"):
        if branches:
