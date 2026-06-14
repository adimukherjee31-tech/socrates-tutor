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

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates AI Tutor", layout="wide", page_icon="🎓")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔑 Setup")
    # THE FIX: Added .strip() to remove accidental spaces from copy-paste
    raw_key = st.text_input("Enter Gemini API Key", type="password")
    api_key = raw_key.strip() 
    
    st.info("Get a free key at: aistudio.google.com")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: Research Agent (RAG)", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# THE SECURITY FIX: Force the key into the environment variables
# This ensures all Google services (LLM + Embeddings) can see it correctly.
os.environ["GOOGLE_API_KEY"] = api_key

# Initialize AI Components
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

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
            with st.spinner("Executing Semantic Indexing..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                chunks = splitter.split_documents(data)
                
                # If this fails, your API key is definitely invalid/expired
                try:
                    st.session_state.db = FAISS.from_documents(chunks, embeddings)
                    st.success("Vector Store Initialized!")
                except Exception as e:
                    st.error(f"Authentication Error: Your Gemini API key is invalid or has expired. Error: {e}")
                finally:
                    os.remove(tmp_path)

        if "db" in st.session_state:
            query = st.chat_input("Ask a question from the book...")
            if query:
                with st.chat_message("user"): st.write(query)
                retriever = st.session_state.db.as_retriever(search_kwargs={"k": 4})
                template = """
                Persona: {tone_style}
                Context: {context}
                Question: {question}
                Answer:"""
                prompt = ChatPromptTemplate.from_template(template)
                chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough(), "tone_style": lambda x: styles[tone]}
                    | prompt | llm | StrOutputParser()
                )
                with st.chat_message("assistant"):
                    response = chain.invoke(query)
                    st.markdown(response)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Research Gap Analysis")
    topic = st.text_input("Enter Topic Name")
    if topic and st.button("Analyze"):
        with st.spinner("Synthesizing..."):
            ans = llm.invoke(f"Identify 3 unique research gaps for '{topic}'.")
            st.write(ans.content)
