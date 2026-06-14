import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- ARCHITECTURAL CONFIG ---
st.set_page_config(page_title="Socrates AI: Research Framework", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔬 Neural Engine Setup")
    raw_key = st.text_input("Enter Gemini API Key", type="password")
    api_key = raw_key.strip() 
    st.info("Using Gemini 1.5 Flash + Text-Embedding-004 (SOTA)")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: Research Agent (RAG)", "Page 6: Gap Analysis"]
    choice = st.selectbox("Orchestration Modules", menu)

if not api_key:
    st.warning("Initialize System with API Key.")
    st.stop()

# Force key into environment for sub-services
os.environ["GOOGLE_API_KEY"] = api_key

# --- COMPONENT INITIALIZATION ---
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    # THE FIX: Using text-embedding-004, the newest SOTA model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
except Exception as e:
    st.error(f"Initialization Failed: {e}")
    st.stop()

# Helper for Context Injection
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- PAGE 1: INTERDISCIPLINARY HOME ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Pedagogical AI Tutor")
    st.subheader("PhD Framework for Interdisciplinary Knowledge Transfer")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Verticals")
        st.button("Learn Math")
        st.button("Learn Core CS")
        st.button("Learn AI & ML")
        st.button("Learn Mechanical Engineering")
    with col2:
        st.write("### 🔗 Intersections")
        st.button("Neural-Physics Intersection")
        st.button("Embedded AI (CS/ECE)")
        st.button("Mechanical Intelligence")

# --- PAGE 2: ROADMAPS ---
elif choice == "Page 2: Exam Roadmaps":
    st.title("Curriculum Roadmaps")
    exam = st.selectbox("Standardized Exam", ["UGC NET", "GATE", "CSIR NET", "IIT JAM", "CUET"])
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Research Branches", branch_list)
    if st.button("Synthesize Roadmap"):
        if branch:
            st.success(f"Roadmap Generated for {exam}")
            st.table({"Phase": ["Abstract Theory", "Domain Depth", "Practice"], "Topic": ["Math/Logic", f"{branch[0]} Core", "PYQs"]})

# --- PAGE 4: RESEARCH AGENT (RAG PIPELINE) ---
elif choice == "Page 4: Research Agent (RAG)":
    st.title("🔍 Advanced Research Agent (RAG)")
    st.markdown("Implementing **Retrieval-Augmented Generation** for grounded pedagogy.")
    
    file = st.file_uploader("Upload Academic PDF (Textbook/Thesis)", type="pdf")
    tone = st.selectbox("Linguistic Persona", ["Professor (Formal)", "Munnabhai (Colloquial)", "Simplified"])
    
    styles = {
        "Professor (Formal)": "Academic expert. Use rigorous terminology and bullet points.",
        "Munnabhai (Colloquial)": "Munnabhai style. Use Hinglish analogies (Mammu, Circuit) to explain complex logic.",
        "Simplified": "Explain like I'm 10 years old."
    }

    if file:
        if "db" not in st.session_state or st.sidebar.button("Re-index Vector Space"):
            with st.spinner("Executing Recursive Semantic Chunking..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                # PhD Depth: Small overlap (15%) to maintain context continuity
                splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                chunks = splitter.split_documents(data)
                
                try:
                    st.session_state.db = FAISS.from_documents(chunks, embeddings)
                    st.success("Vector Database Online.")
                except Exception as e:
                    st.error(f"Vectorization Error: {e}. Ensure API key has 'Generative AI' permissions.")
                finally:
                    os.remove(tmp_path)

        if "db" in st.session_state:
            query = st.chat_input("Enter concept query...")
            if query:
                with st.chat_message("user"): st.write(query)
                
                # RETRIEVAL LOGIC
                retriever = st.session_state.db.as_retriever(search_kwargs={"k": 4})
                
                # LCEL PROMPT TEMPLATE
                template = """
                Persona: {tone_style}
                Context: {context}
                Question: {question}
                
                Instruction: If answer is in Context, add [SOURCE: TEXTBOOK]. Else, answer from parametric memory and add [SOURCE: GENERAL AI].
                
                Response:"""
                prompt = ChatPromptTemplate.from_template(template)
                
                # MODULAR LCEL CHAIN
                chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough(), "tone_style": lambda x: styles[tone]}
                    | prompt | llm | StrOutputParser()
                )
                
                with st.chat_message("assistant"):
                    st.markdown(chain.invoke(query))

# --- PAGE 6: GAP ANALYSIS ---
elif choice == "Page 6: Research Gaps":
    st.title("🔬 Automated Research Gap Analysis")
    topic = st.text_input("Enter Specialized Research Topic")
    if topic and st.button("Synthesize Gaps"):
        with st.spinner("Analyzing current SOTA..."):
            ans = llm.invoke(f"PhD Supervisor: Identify 3 distinct research gaps for '{topic}'. Highlight interdisciplinary potential.")
            st.write(ans.content)
