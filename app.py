import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates AI Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔑 Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at: aistudio.google.com")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: AI Textbook Reader", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# Initialize Components
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- PAGE 1: HOME ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Pedagogical AI Tutor")
    st.subheader("Interdisciplinary Learning Hub")
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
        st.button("Mechanical & AI Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmaps")
    exam = st.selectbox("Select Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch = st.multiselect("Select Branch", ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"])
    if st.button("Generate Roadmap"):
        if branch:
            st.success(f"Roadmap for {exam} Generated")
            st.table({"Phase": ["Foundational", "Core", "Practice"], "Topics": ["Math", f"{branch[0]} Core", "PYQs"]})

# --- PAGE 4: AI READER (RAG) ---
elif choice == "Page 4: AI Textbook Reader":
    st.title("Intelligent Textbook Assistant")
    uploaded_file = st.file_uploader("Upload Textbook (PDF)", type="pdf")
    tone = st.selectbox("Teaching Style", ["Professor", "Munnabhai (Hinglish)", "Simple"])
    
    if uploaded_file:
        if "db" not in st.session_state or st.sidebar.button("Reload PDF"):
            with st.spinner("Analyzing textbook..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                chunks = splitter.split_documents(data)
                st.session_state.db = FAISS.from_documents(chunks, embeddings)
                os.remove(tmp_path)
                st.success("Ready!")

        query = st.chat_input("Ask a question from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            docs = st.session_state.db.similarity_search(query, k=4)
            context = "\n\n".join([d.page_content for d in docs])
            
            prompt = f"""You are Socrates, a tutor. Context: {context}. Question: {query}. 
            If answer is in context, end with [SOURCE: TEXTBOOK]. 
            Else, start with [SOURCE: GENERAL AI]. Style: {tone}"""
            
            response = llm.invoke(prompt)
            with st.chat_message("assistant"): st.markdown(response.content)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Research Gap Analysis")
    topic = st.text_input("Enter Topic")
    if topic and st.button("Analyze"):
        ans = llm.invoke(f"Identify 3 research gaps for '{topic}'.")
        st.write(ans.content)
