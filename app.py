import streamlit as st
import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter

st.set_page_config(page_title="Socrates Tutor", layout="wide")

# Sidebar for API Key
with st.sidebar:
    st.title("🔑 Setup")
    api_key = st.text_input("HuggingFace Token", type="password")
    st.info("Get it free at: huggingface.co/settings/tokens")

if not api_key:
    st.warning("Enter your API Token to begin.")
    st.stop()

# Initialize AI
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=api_key, temperature=0.5)

# Navigation
menu = ["Page 1: Home", "Page 2: Roadmaps", "Page 4: AI Reader (RAG)", "Page 6: Research Gaps"]
choice = st.sidebar.selectbox("Go to:", menu)

if choice == "Page 1: Home":
    st.title("Socrates Tutor")
    st.write("### Interdisciplinary Learning Hub")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Learn Math")
        st.button("Learn Physics")
    with col2:
        st.button("AI & CS Intersection")
        st.button("EEE & ECE Intersection")

elif choice == "Page 2: Roadmaps":
    st.title("Exam Roadmaps")
    exam = st.selectbox("Select Exam", ["GATE", "IIT JAM", "CUET", "CSIR NET"])
    st.write(f"Generating roadmap for {exam}...")
    st.image("https://via.placeholder.com/600x300.png?text=Syllabus+Visualization") # Placeholder for UI

elif choice == "Page 4: AI Reader (RAG)":
    st.title("AI Document Reader")
    uploaded_file = st.file_uploader("Upload Paper/Book (PDF)", type="pdf")
    tone = st.selectbox("Explanation Tone", ["Professor", "GATE Coach", "Industry Expert"])
    
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Theory: This is the RAG Pipeline
        loader = PyPDFLoader("temp.pdf")
        pages = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(pages)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        
        query = st.text_input("Ask a question from the PDF:")
        if query:
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
            response = qa.invoke(f"In the tone of a {tone}, answer: {query}")
            st.markdown(f"**AI Response:** {response['result']}")

elif choice == "Page 6: Research Gaps":
    st.title("Research Gap Analysis")
    topic = st.text_input("Enter Topic (e.g. Genetic Algorithms)")
    if st.button("Analyze Gaps"):
        with st.spinner("Searching literature..."):
            ans = llm.invoke(f"Identify 3 major research gaps for the topic: {topic}. Format as a list.")
            st.write(ans)
