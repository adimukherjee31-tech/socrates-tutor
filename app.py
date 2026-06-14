import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import os

# The rest of your code remains the same...
# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates Tutor", layout="wide")

# Sidebar for API Key (Secure & No-Card)
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter HuggingFace API Token", type="password")
    st.info("Get a free token at huggingface.co")

if not api_key:
    st.warning("Please enter your HuggingFace API key in the sidebar to start.")
    st.stop()

# Initialize LLM (Using Mistral-7B - Free and Powerful)
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=api_key)

# --- NAVIGATION ---
menu = ["Home (Page 1)", "Roadmaps (Page 2)", "Job Titles (Page 3)", "Read a Book (Page 4)", "Research Vision (Page 5)", "Research Gaps (Page 6/7)"]
choice = st.sidebar.selectbox("Navigate Pages", menu)

# --- PAGE 1: SOCRATES TUTOR HOME ---
if choice == "Home (Page 1)":
    st.title("Socrates Tutor")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Learn Math"): st.info("Loading Math Modules...")
        if st.button("Learn Physics"): st.info("Loading Physics Modules...")
        if st.button("Learn EEE/ECE"): st.info("Loading Engineering Modules...")
        
    with col2:
        st.subheader("Interdisciplinary AI")
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Roadmaps (Page 2)":
    st.title("Exam Roadmaps & Syllabus")
    exam = st.selectbox("Select Exam", ["GATE", "IIT JAM", "CUET", "CSIR NET"])
    branch = st.multiselect("Select Branch", ["CS", "AI", "ECE", "MATH", "PHYSICS"])
    
    if st.button("Generate Syllabus"):
        st.write(f"Displaying Roadmap for {exam} - {branch}")
        st.table({"Topic": ["Unit 1: Foundation", "Unit 2: Advanced Concepts"], "Status": ["Available", "Coming Soon"]})

# --- PAGE 4: READ A BOOK (THE AI PART) ---
elif choice == "Read a Book (Page 4)":
    st.title("Interactive Reader (RAG)")
    uploaded_file = st.file_uploader("Upload a PDF Book", type="pdf")
    tone = st.selectbox("Explanation Tone", ["Professor", "Ivy League Student", "GATE Coach", "Corporate Interviewer"])
    
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Simple RAG Logic
        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        
        query = st.text_input("Ask a question about the book:")
        if query:
            qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
            prompt = f"Act as a {tone}. Answer this: {query}"
            response = qa_chain.run(prompt)
            st.markdown(f"### Answer:\n{response}")

# --- PAGE 6 & 7: RESEARCH GAPS ---
elif choice == "Research Gaps (Page 6/7)":
    st.title("Research Gap Analysis")
    topic = st.text_input("Topic Name (e.g., Genetic Algorithms)")
    
    if topic:
        st.subheader(f"Literature Review for {topic}")
        with st.spinner("AI is analyzing research gaps..."):
            gap_prompt = f"Analyze current research gaps and provide a literature review for the topic: {topic}. Format as a list of papers and details."
            result = llm.invoke(gap_prompt)
            st.write(result)
