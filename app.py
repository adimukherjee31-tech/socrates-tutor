import streamlit as st
import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader  # Faster for big books
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(page_title="Socrates Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔑 Setup")
    api_key = st.text_input("HuggingFace Token", type="password")
    st.info("Get it free at: huggingface.co/settings/tokens")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: AI Textbook Reader", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your API Token in the sidebar to begin.")
    st.stop()

# Initialize AI Brain
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=api_key, temperature=0.3)

# --- PAGE 1: INTERDISCIPLINARY HOME ---
if choice == "Page 1: Home":
    st.title("Socrates Tutor")
    st.subheader("Interdisciplinary Learning Hub")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Subjects")
        st.button("Learn Math")
        st.button("Learn Physics")
        st.button("Learn EEE / ECE")
        st.button("Learn Mechanical Engineering")  # Added per request
        st.button("Learn AI & ML")

    with col2:
        st.write("### 🔗 Intersections")
        st.button("AI & Physics Intersection")
        st.button("CS & EE Intersection")
        st.button("AI, CS & ECE Intersection")
        st.button("Mechanical & AI Intersection")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Academic Roadmaps")
    # Added UGC NET to the list
    exam = st.selectbox("Select Exam", ["GATE", "UGC NET", "IIT JAM", "CUET", "CSIR NET"])
    branch = st.multiselect("Select Branch", ["MECH", "ECE", "DS & AI", "CSE", "MATH", "PHYSICS", "EEE"])
    
    if st.button("Display Syllabus & Roadmap"):
        st.info(f"Generating Roadmap for {exam} ({', '.join(branch)})...")
        # Structure showing the roadmap logic
        st.success("✅ Roadmap Generated Successfully")
        st.table({
            "Phase": ["Foundational", "Core Technical", "Advanced/Practice"],
            "Focus": ["Math & Aptitude", f"Standard {branch[0]} Subjects", "Previous Papers & AI Analysis"],
            "Status": ["Ready", "Ready", "Coming Soon"]
        })

# --- PAGE 4: BIG TEXTBOOK READER (RAG) ---
elif choice == "Page 4: AI Textbook Reader":
    st.title("Intelligent Textbook Assistant")
    st.write("Optimized for large textbooks and academic papers.")
    
    uploaded_file = st.file_uploader("Upload Large PDF (Textbook)", type="pdf")
    tone = st.selectbox("Explanation Style", ["Professor Tone", "UGC/GATE Coach", "Corporate Interviewer", "Ivy League Student"])
    
    if uploaded_file:
        with st.spinner("Analyzing large document... this may take a moment."):
            with open("big_book.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Using PyMuPDFLoader for speed on large files
            loader = PyMuPDFLoader("big_book.pdf")
            data = loader.load()
            
            # Smart chunking for better context retrieval
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
            docs = text_splitter.split_documents(data)
            
            if len(docs) > 0:
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                # Using a local FAISS index
                vectorstore = FAISS.from_documents(docs, embeddings)
                
                query = st.text_input("Ask a question about any concept in the book:")
                if query:
                    # Retrieval QA Chain
                    qa = RetrievalQA.from_chain_type(
                        llm=llm, 
                        chain_type="stuff", 
                        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
                    )
                    prompt = f"System: Act as a {tone}. User Question: {query}"
                    response = qa.invoke(prompt)
                    st.markdown(f"### Answer:\n {response['result']}")
            else:
                st.error("Document analysis failed. Ensure the PDF has searchable text.")

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Advanced Research Gap Analysis")
    topic = st.text_input("Enter Topic Name (e.g., Genetic Algorithms in Thermal Systems)")
    exam_context = st.selectbox("Identify gaps based on which syllabus?", ["CSIR NET", "UGC NET", "GATE", "IIT JAM"])
    
    if topic:
        if st.button("Generate Gap Analysis"):
            with st.spinner("Synthesizing current research trends..."):
                gap_prompt = f"""
                Act as a PhD Research Supervisor. 
                Perform a research gap analysis on the topic: '{topic}' 
                considering the current {exam_context} curriculum and recent academic literature.
                Identify 3 specific research gaps, a list of potential literature review papers, and a suggested research vision.
                """
                analysis = llm.invoke(gap_prompt)
                
                st.markdown("### 🔍 Gap Analysis Results")
                st.write(analysis)
                
                st.divider()
                st.info("💡 Tip: Use these gaps to frame your PhD Problem Statement.")
