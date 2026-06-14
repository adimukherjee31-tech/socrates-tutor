import streamlit as st
import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
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
try:
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=api_key, temperature=0.3, max_new_tokens=512)
except Exception as e:
    st.error("Connection Error. Please check your Token.")
    st.stop()

# --- PAGE 1: HOME ---
if choice == "Page 1: Home":
    st.title("Socrates Tutor")
    st.subheader("Interdisciplinary Learning Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Subjects")
        st.button("Learn Math")
        st.button("Learn Physics")
        st.button("Learn EEE / ECE")
        st.button("Learn Mechanical Engineering")
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
    exam = st.selectbox("Select Exam", ["GATE", "UGC NET", "IIT JAM", "CUET", "CSIR NET"])
    branch = st.multiselect("Select Branch", ["MECH", "ECE", "DS & AI", "CSE", "MATH", "PHYSICS", "EEE"])
    if st.button("Display Syllabus & Roadmap"):
        st.info(f"Generating Roadmap for {exam}...")
        st.success("✅ Roadmap Generated Successfully")
        st.table({"Phase": ["Foundational", "Core Technical", "Practice"], "Focus": ["Math", f"Branch Topics", "PYQs"], "Status": ["Ready", "Ready", "Soon"]})

# --- PAGE 4: AI READER (STABLE RAG) ---
elif choice == "Page 4: AI Textbook Reader":
    st.title("Intelligent Textbook Assistant")
    uploaded_file = st.file_uploader("Upload Large PDF (Textbook)", type="pdf")
    tone = st.selectbox("Explanation Style", ["Professor Tone", "UGC/GATE Coach", "Corporate Interviewer", "Ivy League Student", "Munnabhai Lingo"])
    
    if uploaded_file:
        # Use session state to avoid re-processing the PDF on every question
        if "vectorstore" not in st.session_state or st.sidebar.button("Re-process PDF"):
            with st.spinner("Analyzing document... (One-time process)"):
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())
                loader = PyMuPDFLoader("temp.pdf")
                data = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                docs = splitter.split_documents(data)
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
                st.success("Document analyzed!")

        query = st.text_input("Ask a question about any concept in the book:")
        if query:
            with st.spinner("Thinking..."):
                # STEP 1: Manually Retrieve chunks
                search_results = st.session_state.vectorstore.similarity_search(query, k=3)
                context_text = "\n\n".join([doc.page_content for doc in search_results])
                
                # STEP 2: Manually Construct Prompt
                final_prompt = f"""
                You are an expert tutor acting in a {tone}. 
                Use the following context from a textbook to answer the question.
                
                Context: {context_text}
                
                Question: {query}
                
                Answer:"""
                
                # STEP 3: Directly call LLM (Bypasses the buggy QA Chain)
                response = llm.invoke(final_prompt)
                st.markdown(f"### Answer:\n {response}")

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Advanced Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    exam_context = st.selectbox("Context", ["CSIR NET", "UGC NET", "GATE"])
    if topic and st.button("Generate Gap Analysis"):
        with st.spinner("Synthesizing..."):
            gap_prompt = f"Act as a PhD Supervisor. Identify 3 research gaps for '{topic}' within '{exam_context}' syllabus."
            analysis = llm.invoke(gap_prompt)
            st.markdown("### 🔍 Gap Analysis Results")
            st.write(analysis)
