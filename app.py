import streamlit as st
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates AI Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔑 Setup")
    api_key = st.text_input("Enter HuggingFace Token", type="password")
    st.info("Get it free at: huggingface.co/settings/tokens")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: AI Textbook Reader", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your API Token in the sidebar to begin.")
    st.stop()

# Initialize LLM (Mistral 7B - Cloud API)
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=api_key, temperature=0.3)

# Initialize Cloud Embeddings (Avoids Connection/Torch Errors)
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=api_key, 
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- PAGE 1: HOME ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Pedagogical AI Tutor")
    st.subheader("Interdisciplinary Learning Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Subjects")
        st.button("Learn Math")
        st.button("Learn Physics")
        st.button("Learn EEE / ECE")
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
    branch = st.multiselect("Select Branch", ["MECH", "ECE", "CSE", "MATH", "PHYSICS"])
    if st.button("Generate Roadmap"):
        st.success(f"Roadmap for {exam} Generated")
        st.table({"Phase": ["Basics", "Core", "Practice"], "Topics": ["Foundations", "Syllabus Topics", "PYQs"]})

# --- PAGE 4: AI TEXTBOOK READER (GROUNDED RAG) ---
elif choice == "Page 4: AI Textbook Reader":
    st.title("Intelligent Textbook Assistant")
    uploaded_file = st.file_uploader("Upload Textbook (PDF)", type="pdf")
    tone = st.selectbox("Teaching Style", ["Professor", "Munnabhai (Hinglish)", "Simple"])
    
    styles = {
        "Professor": "Professional Academic Tutor. Use bullet points and exam-style headings.",
        "Munnabhai (Hinglish)": "Munnabhai style. Use Hinglish, call user 'Mammu', use funny life analogies.",
        "Simple": "Explain like I'm 10 years old with simple examples."
    }

    if uploaded_file:
        if "db" not in st.session_state or st.sidebar.button("Re-process PDF"):
            with st.spinner("Analyzing materials..."):
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())
                loader = PyMuPDFLoader("temp.pdf")
                docs = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                chunks = splitter.split_documents(docs)
                st.session_state.db = FAISS.from_documents(chunks, embeddings)
                st.success("Indexing Complete!")

        query = st.chat_input("Ask a question from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            
            with st.spinner("Socrates is thinking..."):
                # Retrieve Context
                context_docs = st.session_state.db.similarity_search(query, k=3)
                context_text = "\n\n".join([d.page_content for d in context_docs])

                # GROUNDING RULES (From your snippet)
                prompt = f"""
                You are Socrates, a pedagogical tutor. Use the provided Context to answer the Question.
                
                GROUNDING RULES:
                1. Search the 'Context' for the answer first. 
                2. If the answer is found in the Context, explain it and MUST append: "[SOURCE: TEXTBOOK]" at the end.
                3. If the answer is NOT found in the Context, answer using your general knowledge but you MUST start the response with: "[SOURCE: GENERAL AI KNOWLEDGE - NOT IN PDF]".
                
                Style/Personality: {styles[tone]}
                Context: {context_text}
                Question: {query}
                
                Answer:"""
                
                response = llm.invoke(prompt)
                with st.chat_message("assistant"):
                    st.markdown(response)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Advanced Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    if topic and st.button("Analyze Gaps"):
        with st.spinner("Synthesizing..."):
            ans = llm.invoke(f"PhD Supervisor: Identify 3 research gaps for '{topic}'.")
            st.markdown("### 🔍 Gap Analysis Results")
            st.write(ans)
