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
    # CHANGED: Now asking specifically for Gemini Key
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at: aistudio.google.com")
    
    st.divider()
    menu = ["Page 1: Home", "Page 2: Exam Roadmaps", "Page 4: AI Textbook Reader", "Page 6: Research Gaps"]
    choice = st.selectbox("Navigation", menu)

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# Initialize Gemini Brain and Math (Embeddings)
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    # This uses Google's servers for embeddings, NO MORE Hugging Face connection errors!
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# --- PAGE 1: HOME ---
if choice == "Page 1: Home":
    st.title("🎓 Socrates: Pedagogical AI Tutor")
    st.subheader("Interdisciplinary Learning Hub")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 📚 Core Subjects")
        st.button("Learn Math")
        st.button("Learn Core CS")  # Added per request
        st.button("Learn AI & ML")  # Added per request
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
    
    # Updated Branch List
    branch_list = ["CSE", "AI & ML", "EEE", "ECE", "MECH", "MATH", "PHYSICS"]
    branch = st.multiselect("Select Branch(es)", branch_list)
    
    if st.button("Generate Roadmap"):
        if branch:
            st.success(f"Roadmap for {exam} ({', '.join(branch)}) Generated")
            st.table({
                "Phase": ["Foundational", "Core Technical", "Practice"], 
                "Focus": ["Engineering Mathematics", f"{branch[0]} Core Subjects", "PYQs & Mock Tests"], 
                "Status": ["Ready", "Ready", "Coming Soon"]
            })
        else:
            st.warning("Please select at least one branch.")

# --- PAGE 4: AI TEXTBOOK READER (STABLE GEMINI VERSION) ---
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
        if "vector_db" not in st.session_state or st.sidebar.button("Refresh PDF Data"):
            with st.spinner("Socrates is analyzing the textbook with Gemini..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                
                loader = PyMuPDFLoader(tmp_path)
                data = loader.load()
                
                splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
                chunks = splitter.split_documents(data)
                
                # USING GOOGLE EMBEDDINGS - Very fast and stable
                st.session_state.vector_db = FAISS.from_documents(chunks, embeddings)
                os.remove(tmp_path)
                st.success("Textbook ready!")

        query = st.chat_input("Ask Socrates a question from the book...")
        if query:
            with st.chat_message("user"): st.write(query)
            
            with st.spinner("Thinking..."):
                docs = st.session_state.vector_db.similarity_search(query, k=4)
                context_text = "\n\n".join([d.page_content for d in docs])

                prompt = f"""
                You are Socrates, a pedagogical tutor. Use the provided Context to answer the Question.
                
                GROUNDING RULES:
                1. Search the 'Context' for the answer first. 
                2. If the answer is found in the Context, explain it and MUST append: "[SOURCE: TEXTBOOK]" at the end.
                3. If the answer is NOT found in the Context, answer using your general knowledge but you MUST start the response with: "[SOURCE: GENERAL AI KNOWLEDGE - NOT IN PDF]".
                
                Style: {styles[tone]}
                Context: {context_text}
                Question: {query}
                
                Answer:"""
                
                response = llm.invoke(prompt)
                with st.chat_message("assistant"):
                    st.markdown(response.content)

# --- PAGE 6: RESEARCH GAPS ---
elif choice == "Page 6: Research Gaps":
    st.title("Advanced Research Gap Analysis")
    topic = st.text_input("Enter Research Topic")
    if topic and st.button("Analyze Gaps"):
        with st.spinner("Scanning for research frontiers..."):
            ans = llm.invoke(f"PhD Supervisor: Identify 3 unique research gaps for '{topic}'. Format as a literature review summary.")
            st.markdown("### 🔍 Analysis Result")
            st.write(ans.content)
