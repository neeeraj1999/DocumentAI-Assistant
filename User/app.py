import boto3
import streamlit as st
import os
import uuid

## s3_client
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

## Bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

## prompt and chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

## Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_client)

folder_path="/tmp/"

def get_unique_id():
    return str(uuid.uuid4())

## load index
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm():
    llm=Bedrock(model_id="anthropic.claude-v2:1", client=bedrock_client,
                model_kwargs={'max_tokens_to_sample': 512})
    return llm

# get_response()
def get_response(llm,vectorstore, question ):
    ## create prompt / template
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer=qa({"query":question})
    return answer['result']


## main method
def main():
    # Set page configuration
    st.set_page_config(
        page_title="PDF Chat Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #e0e0e0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sub-header styling */
    .sub-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #3f51b5;
        margin-top: 1.8rem;
        margin-bottom: 1.2rem;
        padding-left: 10px;
        border-left: 5px solid #3f51b5;
    }
    
    /* Info box styling */
    .info-box {
        background-color: rgba(240, 248, 255, 0.8);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #2196F3;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .info-box h3 {
        color: #1565c0;
        margin-bottom: 10px;
    }
    
    /* Success box styling */
    .success-box {
        background-color: rgba(240, 255, 240, 0.8);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .success-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* File list styling */
    .file-list {
        background-color: #f5f5f5;
        padding: 1.2rem;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    .file-list code {
        display: block;
        padding: 5px 10px;
        margin: 5px 0;
        background-color: rgba(0, 0, 0, 0.05);
        border-radius: 5px;
        transition: all 0.2s ease;
    }
    
    .file-list code:hover {
        background-color: rgba(0, 0, 0, 0.1);
        transform: translateX(5px);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        font-weight: 600;
        padding: 0.6rem 2.5rem;
        border-radius: 30px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #45a049, #2e7d32);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 15px;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Answer box styling */
    .answer-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #9C27B0;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        line-height: 1.6;
        font-size: 16px;
        color: #000000;
        font-weight: 500;
    }
    
    /* Divider styling */
    hr {
        height: 3px;
        background: linear-gradient(to right, transparent, #4CAF50, #2196F3, transparent);
        border: none;
        margin: 30px 0;
    }
    
    /* Spinner styling */
    .stSpinner>div {
        border-color: #4CAF50 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Animation for elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with icon and animation
    st.markdown('<div class="main-header animate-fade-in">📚 Chat with PDF Demo</div>', unsafe_allow_html=True)
    
    # Introduction with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box animate-fade-in">
        <h3>Welcome to the PDF Chat Assistant!</h3>
        <p>This application uses Amazon Bedrock and Retrieval Augmented Generation (RAG) to provide intelligent responses based on the content of your PDF documents.</p>
        <p>Simply type your question below and get accurate answers extracted from your documents.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://img.icons8.com/color/96/000000/pdf.png", width=120)
        st.markdown("<p style='text-align: center; font-weight: 500; color: #666;'>Powered by AWS Bedrock</p>", unsafe_allow_html=True)
    
    # Add a gradient divider
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Load index with progress indicator
    with st.spinner("Loading document index..."):
        load_index()
    
    # Display files in a nicer format
    st.markdown('<div class="sub-header animate-fade-in">📁 Indexed Files</div>', unsafe_allow_html=True)
    
    dir_list = os.listdir(folder_path)
    if dir_list:
        st.markdown('<div class="file-list">', unsafe_allow_html=True)
        for i, file in enumerate(dir_list):
            st.markdown(f"<code>{i}: \"{file}\"</code>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No files found in the index directory.")
    
    # Create index with success message
    try:
        faiss_index = FAISS.load_local(
            index_name="my_faiss",
            folder_path = folder_path,
            embeddings=bedrock_embeddings,
            allow_dangerous_deserialization=True
        )
        st.markdown('<div class="success-box animate-fade-in">✅ Index loaded successfully! You can now ask questions about your PDF.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading index: {str(e)}")
        st.stop()
    
    # Question input with better styling
    st.markdown('<div class="sub-header animate-fade-in">❓ Ask Your Question</div>', unsafe_allow_html=True)
    
    question = st.text_input("", placeholder="Type your question here and press Enter or click 'Ask Question'...", key="question_input")
    
    # Create columns for button alignment
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        ask_button = st.button("Ask Question")
    
    # Response area
    if ask_button and question:
        with st.spinner("🔍 Searching for answers..."):
            llm = get_llm()
            response = get_response(llm, faiss_index, question)
        
        st.markdown('<div class="sub-header animate-fade-in">📝 Answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="answer-box animate-fade-in">{response}</div>', unsafe_allow_html=True)
        st.balloons()
    
    # Footer
    st.markdown('<div class="footer">© 2025 PDF Chat Assistant | Built with Streamlit and AWS Bedrock</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
