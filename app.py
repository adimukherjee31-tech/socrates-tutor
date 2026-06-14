import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- ARCHITECTURAL CONFIG ---
st.set_page_config(page_title="Socrates: PhD Research Framework", layout="wide", page_icon="🔬")

# --- SIDEBAR: SYSTEM PARAMETERS ---
with st.sidebar:
    st.title("🔬 Research Setup")
    gemini_key = st.text_input("Gemini API Key (LLM & Embeddings)", type="password")
    st.info("Uses Google Generative AI for SOTA Semantic Retrieval.")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: Research Agent (RAG)", "Page 6: Gap Analysis"]
    choice = st.selectbox("Orchestration Modules", menu)

if not gemini_key:
    st.warning("Enter API Key to initialize the Neural Engine.")
    st.stop()

# --- NEURAL ENGINE INITIALIZATION ---
# Using Gemini 1.5 Flash for high-speed, long-context research reasoning
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_key)

# --- MODULE 1: INTERDISCIPLINARY DISCOVERY ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Interdisciplinary AI Tutor")
    st.subheader("PhD Framework for Cross-Domain Pedagogy")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Foundational Verticals")
        st.button("Learn Math")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.write("### 🔗 Interdisciplinary Intersections")
        st.button("AI & Physics (Neural ODEs)")
        st.button("CS & EE (Edge AI)")
        st.button("AI, CS & ECE (VLSI Optimization)")
        st.button("ME & AI (Generative Design)")

# --- MODULE 2: ROADMAPS & CURRICULUM ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Curriculum Roadmaps")
    exam = st.selectbox("Standardized Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM"])
    branch = st.multiselect("Research Branches", ["CSE", "AI & ML", "EEE", "ECE", "MECH"])
    if st.button("Synthesize Roadmap"):
        st.success(f"Optimized Roadmap for {exam} Generated.")
        st.table({"Phase": ["Abstract Reasoning", "Domain Depth", "Empirical Practice"], "Focus": ["Foundational Theory", f"{branch if branch else 'General'} Core", "Heuristic Benchmarking"]})

# --- MODULE 4: THE RESEARCH AGENT (RAG PIPELINE) ---
elif choice == "Page 4: Research Agent (RAG)":
    st.title("🔍 Advanced Research Agent (RAG)")
    st.markdown("This module implements **Retrieval-Augmented Generation** for massive literature analysis.")
    
    file = st.file_uploader("Upload Dissertation/Textbook (PDF)", type="pdf")
    tone = st.selectbox("Linguistic Persona", ["Professor (Formal)", "Munnabhai (Colloquial)", "Simplified"])
    
    if file:
        if "vector_store" not in st.session_state:
            with st.spinner("Executing Semantic Chunking & Vectorization..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                
                # High-performance PDF parsing
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                
                # PhD Depth: Recursive Semantic Splitting to maintain hierarchical context
                splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
                chunks = splitter.split_documents(data)
                
                # Building the Vector DB
                st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
                os.remove(tmp_path)
                st.success("Vector Space successfully populated.")

        query = st.chat_input("Input research query...")
        if query:
            # RETRIEVAL LOGIC
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
            
            # PROMPT ARCHITECTURE
            template = """
            Persona: {tone}
            Task: Synthesize an answer based ONLY on the following Context. 
            Verification: If answer is in context, conclude with [SOURCE: DOCUMENT]. 
            Else, use parametric knowledge and start with [SOURCE: PARAMETRIC AI].
            
            Context: {context}
            Query: {question}
            
            Synthesized Answer:
            """
            prompt = ChatPromptTemplate.from_template(template)
            
            # LCEL CHAIN (LangChain Expression Language)
            chain = (
                {"context": retriever, "question": RunnablePassthrough(), "tone": lambda x: tone}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            with st.chat_message("assistant"):
                response = chain.invoke(query)
                st.markdown(response)

# --- MODULE 6: GAP ANALYSIS ---
elif choice == "Page 6: Gap Analysis":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Research Domain")
    if topic and st.button("Synthesize Research Gaps"):
        with st.spinner("Analyzing current SOTA..."):
            prompt = f"As a PhD Supervisor, perform a critical literature review and identify 3 novel research gaps for: {topic}."
            ans = llm.invoke(prompt)
            st.markdown("### Critical Synthesis Result:")
            st.write(ans.content)
