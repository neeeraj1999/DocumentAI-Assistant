# DocumentAI-Assistant
## 📚 Overview
DocumentAI-Assistant represents a cutting-edge document interaction system that revolutionizes how users engage with PDF documents. Powered by AWS Bedrock's advanced AI capabilities, specifically utilizing Claude V2 for natural language processing and Titan for embeddings, the system implements Retrieval Augmented Generation (RAG) technology to enable intuitive document analysis. When users upload PDFs, the system intelligently processes them by breaking content into meaningful chunks, converting them into vector embeddings, and storing them in a FAISS index within AWS S3. This sophisticated architecture allows users to ask natural language questions about their documents and receive contextually accurate responses.y combining state-of-the-art AI models with efficient vector storage and retrieval mechanisms, DocumentAI-Assistant transforms static PDF documents into interactive knowledge bases, making information extraction and document analysis more accessible and efficient than ever before.

## 🔄 Application Modes

### 💾 Admin Mode
- Handles document processing and vector database creation
- Generates and manages FAISS index files
- Securely stores indexes in S3 for production use
![image](https://github.com/user-attachments/assets/21bea9a5-0a94-405f-b849-b5c1d3cc2b57)
![image](https://github.com/user-attachments/assets/e4e4dea9-f372-46bf-a599-a13c4842ca18)
![image](https://github.com/user-attachments/assets/12f0b201-0ccd-428e-a383-3ef95a846f6d)

### 👤 User Mode
- Provides intuitive chat interface
- Shows indexed file status
- Enables natural language queries
- Delivers context-aware responses using RAG
  ![image](https://github.com/user-attachments/assets/ba798820-21ab-4803-bde4-5530fc28b1c9)

## 🚀 Features

- **PDF Processing**: Efficiently processes and indexes PDF documents
- **Intelligent Querying**: Uses RAG technology to provide accurate, context-aware responses
- **AWS Bedrock Integration**: Leverages Claude for text generation and Titan for embeddings
- **Modern UI**: Clean, responsive interface with custom styling and animations
- **Vector Storage**: FAISS-based vector storage for efficient document retrieval
- **Docker Support**: Containerized deployment for easy scaling and consistency
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

-## Setup and Installation

### Prerequisites

- Docker
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials

### Running the Admin Application

1. Build the Docker image:
   ```
   cd Admin
   docker build -t pdf-reader-admin .
   ```

2. Run the container:
   ```
   docker run -e BUCKET_NAME=your-s3-bucket-name -e AWS_ACCESS_KEY_ID=your-access-key -e AWS_SECRET_ACCESS_KEY=your-secret-key -e AWS_REGION=us-east-1 -p 8083:8083 -it pdf-reader-admin
   ```

3. Access the admin interface at `http://localhost:8083`

### Running the User Application

1. Build the Docker image:
   ```
   cd User
   docker build -t pdf-read-client .
   ```

2. Run the container:
   ```
   docker run -e BUCKET_NAME=your-s3-bucket-name -e AWS_ACCESS_KEY_ID=your-access-key -e AWS_SECRET_ACCESS_KEY=your-secret-key -e AWS_REGION=us-east-1 -p 8084:8084 -it pdf-read-client
   ```

3. Access the user interface at `http://localhost:8084`



