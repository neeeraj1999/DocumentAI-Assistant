# DocumentAI-Assistant

PDF Agent Prime is an intelligent document assistant powered by AWS Bedrock and RAG (Retrieval Augmented Generation) technology. It enables users to have natural conversations with their PDF documents, extracting relevant information through an intuitive chat interface.

## 🚀 Features

- **PDF Processing**: Efficiently processes and indexes PDF documents
- **Intelligent Querying**: Uses RAG technology to provide accurate, context-aware responses
- **AWS Bedrock Integration**: Leverages Claude for text generation and Titan for embeddings
- **Modern UI**: Clean, responsive interface with custom styling and animations
- **Vector Storage**: FAISS-based vector storage for efficient document retrieval
- **Real-time Responses**: Quick and accurate answers from your documents

## 🛠️ Technology Stack

- **Backend**:
  - Python
  - AWS Bedrock (Claude, Titan)
  - LangChain
  - FAISS Vector Store
  - Boto3 (AWS SDK)

- **Frontend**:
  - Streamlit
  - Custom CSS
  - Responsive Design

## 📋 Prerequisites

- Python 3
- AWS Account with Bedrock access
- Required environment variables:
  - `BUCKET_NAME`: AWS S3 bucket name for storing indexes

## 🔧 Installation

1. Clone the repository:
