import streamlit as st
import os
import requests
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates AI Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔑 Setup")
    gemini_key = st.text_input("Enter Gemini API Key", type="password")
    hf_token = st.text_input("Enter HuggingFace Token (for Math/Embeddings)", type="password")
    st.info("Get Keys at: aistudio.google.com and huggingface.co/settings/tokens")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: AI Textbook Reader", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not gemini_key or not hf_token:
    st.warning("Please enter both API keys in the sidebar to start.")
    st.stop()

# --- LIGHTWEIGHT AI FUNCTIONS (STABLE) ---
def get_embeddings(texts, token):
    # Uses HuggingFace API for Math - No local torch errors!
    url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json={"inputs": texts})
    return response.json()

class CloudEmbeddings:
    def __init__(self, token): self.token = token
    def embed_documents(self, texts): return get_embeddings(texts, self.token)
    def embed_query(self, text): return get_embeddings([text], self.token)[0]

def call_gemini(prompt, key):
    # Direct API call to Gemini - No Google library errors!
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload)
    return response.json()['candidates'][0]['content']['parts'][0]['text']

# --- PAGE 1: HOME ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Pedagogical AI Tutor")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Subjects")
        st.button("Learn Math")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.write("### 🔗 Intersections")
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmaps")
    exam = st.selectbox("Select Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Select Branch", ["CSE", "AI & ML", "EEE", "ECE", "MECH"])
    if st.button("Generate"):
        st.success(f"Roadmap for {exam} Generated")
        st.table({"Phase": ["Basic", "Core", "PYQ"], "Goal": ["Maths", f"{branch[0] if branch else 'Branch'} Skills", "Exams"]})

# --- PAGE 4: AI READER ---
elif choice == "Page 4: AI Textbook Reader":
    st.title("Intelligent Textbook Assistant")
    file = st.file_uploader("Upload PDF", type="pdf")
    tone = st.selectbox("Style", ["Professor", "Munnabhai", "Simple"])
    
    if file:
        if "db" not in st.session_state:
            with st.spinner("Processing..."):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = splitter.split_text(text)
                
                # Setup Vector DB using our stable cloud math
                embed_engine = CloudEmbeddings(hf_token)
                st.session_state.db = FAISS.from_texts(chunks, embed_engine)
                st.success("Ready!")

        query = st.chat_input("Ask from textbook...")
        if query:
            with st.chat_message("user"): st.write(query)
            context_docs = st.session_state.db.similarity_search(query, k=3)
            context = "\n".join([d.page_content for d in context_docs])
            
            prompt = f"Style: {tone}. Context: {context}. Question: {query}. End with [SOURCE: TEXTBOOK] if found, else start with [SOURCE: AI]."
            answer = call_gemini(prompt, gemini_key)
            with st.chat_message("assistant"): st.markdown(answer)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Research Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        ans = call_gemini(f"List 3 research gaps for {topic}.", gemini_key)
        st.write(ans)
