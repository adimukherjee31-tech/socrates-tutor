import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# NEW MODULAR IMPORTS (The Fix)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates AI Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔑 Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at: aistudio.google.com")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: Research Agent (RAG)", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# Initialize AI Components
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# Helper function for RAG formatting
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

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
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmaps")
    exam = st.selectbox("Select Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Select Branch(es)", branch_list)
    if st.button("Generate Roadmap"):
        if branch:
            st.success(f"Roadmap for {exam} Generated")
            st.table({"Phase": ["Foundational", "Core", "Practice"], "Focus": ["Math", f"{branch[0]} Core", "PYQs"]})

# --- PAGE 4: RESEARCH AGENT (RAG) ---
elif choice == "Page 4: Research Agent (RAG)":
    st.title("🔍 Advanced Research Agent (RAG)")
    file = st.file_uploader("Upload Textbook (PDF)", type="pdf")
    tone = st.selectbox("Teaching Style", ["Professor", "Munnabhai (Hinglish)", "Simple"])
    
    styles = {
        "Professor": "Professional Academic Tutor. Use bullet points.",
        "Munnabhai (Hinglish)": "Munnabhai style. Use Hinglish and funny analogies.",
        "Simple": "Explain like I'm 10 years old."
    }

    if file:
        if "db" not in st.session_state or st.sidebar.button("Refresh PDF"):
            with st.spinner("Executing Semantic Chunking..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                chunks = splitter.split_documents(data)
                st.session_state.db = FAISS.from_documents(chunks, embeddings)
                os.remove(tmp_path)
                st.success("Vector Store Initialized!")

        query = st.chat_input("Ask a question from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            
            # RETRIEVER SETUP
            retriever = st.session_state.db.as_retriever(search_kwargs={"k": 4})
            
            # PROMPT TEMPLATE (PhD GROUNDING LOGIC)
            template = """
            Persona: {tone_style}
            Task: Use the provided Context to answer the Question.
            
            GROUNDING RULES:
            1. If answer is found in Context, explain it and add [SOURCE: TEXTBOOK].
            2. If NOT in Context, answer from general knowledge and add [SOURCE: GENERAL AI].
            
            Context: {context}
            Question: {question}
            
            Answer:"""
            
            prompt = ChatPromptTemplate.from_template(template)
            
            # THE MODULAR LCEL CHAIN
            chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough(), "tone_style": lambda x: styles[tone]}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            with st.chat_message("assistant"):
                response = chain.invoke(query)
                st.markdown(response)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    if topic and st.button("Analyze"):
        with st.spinner("Synthesizing research frontiers..."):
            ans = llm.invoke(f"PhD Level Analysis: Identify 3 unique research gaps for '{topic}'.")
            st.write(ans.content)
