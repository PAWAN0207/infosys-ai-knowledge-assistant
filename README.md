\# 🤖 Infosys AI Knowledge Assistant



\### Enterprise RAG System with RBAC, Grounded Responses \& Source Citations



An enterprise-style \*\*Retrieval-Augmented Generation (RAG)\*\* application that helps employees search internal knowledge documents using natural language.



The system combines \*\*Google Gemini, LangChain, ChromaDB, Python, and Streamlit\*\* to retrieve relevant document context, generate grounded answers, provide source citations, and enforce department-level \*\*Role-Based Access Control (RBAC)\*\* before document retrieval.



> \*\*Portfolio Project:\*\* This project demonstrates an enterprise knowledge assistant architecture with semantic retrieval, access control, citation grounding, and hallucination guardrails.



\---



\## 🚀 Live Demo



\### 👉 \[Open the Live Application](https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/)



The application is deployed using \*\*Streamlit Community Cloud\*\*.



You can test:



\- 🔎 Enterprise document search

\- 🔐 Role-based access control

\- 📚 Source citations

\- 🧠 Grounded Gemini responses

\- 🛡️ Out-of-domain query protection



\---



\## 🎯 Project Highlights



| Feature | Implementation |

|---|---|

| 🧠 LLM | Google Gemini |

| 🔎 Retrieval | ChromaDB Semantic Search |

| 🔗 RAG Framework | LangChain |

| 📄 PDF Processing | PyMuPDF |

| 🧩 Text Chunking | RecursiveCharacterTextSplitter |

| 🔐 Access Control | Role-Based Department Filtering |

| 📚 Citations | Document + Page Metadata |

| 🛡️ Guardrails | Grounded / Zero-Extrapolation Prompting |

| 🖥️ UI | Streamlit |

| ☁️ Deployment | Streamlit Community Cloud |

| 🐍 Language | Python 3.12 |



\---



\# 📌 Problem Statement



Enterprise employees often need to search through policies, SOPs, technical guides, project manuals, and business documents.



Traditional keyword search can make it difficult to understand natural-language questions and identify the most relevant information.



This project addresses that problem by building an AI-powered knowledge assistant that:



1\. Understands natural-language employee questions.

2\. Searches enterprise documents semantically.

3\. Applies role-based access restrictions.

4\. Generates answers from retrieved document context.

5\. Displays source documents and page numbers.

6\. Avoids unsupported answers when sufficient domain context is unavailable.



\---



\# 💡 Solution



The application uses a \*\*Retrieval-Augmented Generation architecture\*\* instead of sending user questions directly to an LLM.



\### High-Level Workflow



```text

Employee Query

&#x20;     ↓

Employee Designation

&#x20;     ↓

RBAC Department Filter

&#x20;     ↓

ChromaDB Semantic Retrieval

&#x20;     ↓

Relevant Document Chunks

&#x20;     ↓

Grounded Context Builder

&#x20;     ↓

Google Gemini

&#x20;     ↓

Answer + Citation + Confidence + Recommended Action

🏗️ System Architecture

&#x20;                   ┌──────────────────────┐

&#x20;                   │      Employee        │

&#x20;                   │       Query          │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Employee Designation │

&#x20;                   │      Selection       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │        RBAC          │

&#x20;                   │ Department Filtering │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │       ChromaDB       │

&#x20;                   │ Semantic Retrieval   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                        Top 5 Chunks

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │  Grounded Context    │

&#x20;                   │       Builder        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    Google Gemini     │

&#x20;                   │  Grounded Generation │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;             ┌─────────────────────────────────┐

&#x20;             │        Final Response           │

&#x20;             │                                 │

&#x20;             │  • Grounded Answer             │

&#x20;             │  • Confidence Score             │

&#x20;             │  • Recommended Action           │

&#x20;             │  • Source Citation              │

&#x20;             └─────────────────────────────────┘

🔄 RAG Pipeline

1\. Document Ingestion



Enterprise-style PDF documents are organized inside the data/ directory.



data/

├── engineering\_guides/

├── hr\_policies/

├── project\_manuals/

├── sales\_assets/

└── sops/

2\. PDF Text Extraction



PyMuPDFLoader extracts text from PDF documents page by page.



Processing documents page-by-page allows the original page number to be retained for citations.



3\. Text Chunking



The extracted content is divided into smaller chunks using LangChain's:



RecursiveCharacterTextSplitter



Configuration:



Chunk Size    : 1000 characters

Chunk Overlap : 200 characters



The overlap helps preserve contextual information between neighboring chunks.



4\. Metadata Creation



Each chunk receives metadata:



source\_document

page\_number

department

chunk\_id



This metadata is used for:



RBAC filtering

Source citations

Document traceability

5\. Embedding Generation



Document chunks are converted into vector representations using:



gemini-embedding-2-preview

6\. Vector Storage



The generated embeddings, document text, and metadata are stored in:



ChromaDB

7\. Query Retrieval



When an employee submits a question:



User Query

&#x20;   ↓

Determine Employee Designation

&#x20;   ↓

Determine Allowed Departments

&#x20;   ↓

Apply RBAC Filter

&#x20;   ↓

ChromaDB Semantic Search

&#x20;   ↓

Retrieve Top 5 Relevant Chunks

&#x20;   ↓

Build Grounded Context

&#x20;   ↓

Send Context + Query to Gemini

&#x20;   ↓

Generate Structured Response

🔐 Role-Based Access Control



The application implements department-level access control based on employee designation.



The RBAC layer determines which departments a user can access before retrieved content is passed to the generation layer.



Access Matrix

Employee Designation	Permitted Departments

Software Engineer	Engineering, Delivery Operations, PMO

Senior Software Engineer	Engineering, Delivery Operations, PMO

DevOps Lead	Engineering, Delivery Operations

Solutions Architect	Engineering, Delivery Operations, PMO

Engineering Lead	Engineering, Delivery Operations, PMO

Sales Executive	Sales, Human Resources

Business Development Manager	Sales, PMO

Account Manager	Sales

Sales Enablement Lead	Sales, Human Resources, PMO

Delivery Manager	Delivery Operations, PMO, Engineering

PMO Lead	PMO, Delivery Operations, Engineering

Operations Lead	Delivery Operations

HR Associate	Human Resources

HR Operations Lead	Human Resources

Senior Manager	Engineering, Delivery Operations, PMO, Human Resources, Sales

🔒 RBAC Demonstration

Authorized Example



Designation: Software Engineer



Query:



What are the key principles of the Infosys microservices architecture?



The Software Engineer role has access to the Engineering department.



Expected flow:



Query

&#x20;↓

Engineering access permitted

&#x20;↓

Engineering chunks retrieved

&#x20;↓

Grounded Gemini response

&#x20;↓

Source citation displayed

Restricted Example



Designation: HR Associate



Query:



What are the key principles of the Infosys microservices architecture?



The HR Associate role has access only to Human Resources.



The Engineering department is not permitted.



Expected response:



Access Denied /

Insufficient domain context available

for your role clearance.



No Engineering citation should be returned.



Demo limitation: The designation selector simulates employee identity and RBAC for demonstration purposes. A production system would integrate this layer with SSO/OAuth/OIDC and a corporate identity provider.



🛡️ Grounding \& Hallucination Control



The generation layer uses strict grounding instructions to reduce unsupported LLM responses.



The model is instructed to:



Use only the retrieved context.

Avoid external knowledge.

Avoid assumptions.

Avoid unsupported extrapolation.

Return an insufficient-context response when the retrieved documents do not contain the required information.

Map citations to retrieved document metadata.

Grounded Generation Flow

Retrieved Context

&#x20;      +

Employee Query

&#x20;      ↓

Grounded Prompt

&#x20;      ↓

Google Gemini

&#x20;      ↓

Structured Response

📚 Citation System



Each retrieved chunk contains source metadata.



The Streamlit application displays this information through the Citation \& Source Panel.



Example:



Document:

Infosys\_Microservices\_Architecture\_Spec.pdf



Page:

1



Department:

Engineering



Matched Passage:

Relevant retrieved document content



This makes the generated response easier to verify against the original source document.



📄 Knowledge Base



The demonstration knowledge base contains enterprise-style documents across multiple business domains.



Document	Department

Infosys Microservices Architecture Specification	Engineering

Infosys Severity 1 Incident Escalation SOP	Delivery Operations

Infosys Agile Execution Framework Guide	PMO

Infosys Global Leave Policy 2026	Human Resources

Infosys Cloud Transformation Capability Deck	Sales



All source PDFs are stored under:



data/

🧪 Example Test Cases

Test Case 1 — Engineering RAG Query



Designation:



Software Engineer



Query:



What are the key principles of the Infosys microservices architecture?



Expected:



✓ Grounded Answer

✓ Confidence Score

✓ Source Document

✓ Page Number

✓ Matched Passage

Test Case 2 — RBAC Security



Designation:



HR Associate



Query:



What are the key principles of the Infosys microservices architecture?



Expected:



Access Denied /

Insufficient domain context available

for your role clearance.



This demonstrates that the HR role cannot retrieve Engineering documentation.



Test Case 3 — Out-of-Domain Query



Query:



How are you?



Expected behavior:



Insufficient domain context



The application is designed as a grounded enterprise knowledge assistant rather than a general-purpose chatbot.



🛠️ Technology Stack

Programming

Python 3.12

AI / LLM

Google Gemini

Google Generative AI Embeddings

RAG

LangChain

Retrieval-Augmented Generation

Vector Database

ChromaDB

Document Processing

PyMuPDF

RecursiveCharacterTextSplitter

Application

Streamlit

Data Validation

Pydantic

Configuration

python-dotenv

Deployment

GitHub

Streamlit Community Cloud

📁 Project Structure

infosys-ai-knowledge-assistant/

│

├── app.py

├── README.md

├── requirements.txt

├── .env.example

├── .gitignore

│

├── ai\_workflows/

│   ├── citation\_builder/

│   │   ├── \_\_init\_\_.py

│   │   └── citation\_formatter.py

│   │

│   ├── grounded\_synthesis/

│   │   ├── \_\_init\_\_.py

│   │   └── synthesis\_engine.py

│   │

│   ├── query\_classification/

│   │   ├── \_\_init\_\_.py

│   │   └── rbac\_classifier.py

│   │

│   └── rag\_retrieval/

│       ├── \_\_init\_\_.py

│       └── hybrid\_search.py

│

├── ingestion\_pipeline/

│   └── embedding\_jobs/

│       ├── \_\_init\_\_.py

│       └── vector\_indexer.py

│

├── data/

│   ├── engineering\_guides/

│   ├── hr\_policies/

│   ├── project\_manuals/

│   ├── sales\_assets/

│   └── sops/

│

└── frontend/

&#x20;   ├── package.json

&#x20;   └── package-lock.json



vector\_db/ is intentionally excluded from Git because it is generated from the source PDFs.



⚙️ Local Installation

1\. Clone the Repository

git clone https://github.com/PAWAN0207/infosys-ai-knowledge-assistant.git

cd infosys-ai-knowledge-assistant

2\. Create Conda Environment

conda create -n infosys-rag python=3.12

conda activate infosys-rag

3\. Install Dependencies

pip install -r requirements.txt

4\. Configure Environment Variables



Create a .env file in the project root:



GOOGLE\_API\_KEY=your\_gemini\_api\_key\_here



Never commit .env or API keys to GitHub.



📦 Build the Vector Database



Run the ingestion pipeline:



python ingestion\_pipeline/embedding\_jobs/vector\_indexer.py



Pipeline:



PDF Documents

&#x20;     ↓

Text Extraction

&#x20;     ↓

Chunking

&#x20;     ↓

Metadata Creation

&#x20;     ↓

Gemini Embeddings

&#x20;     ↓

ChromaDB

▶️ Run the Application



Start Streamlit:



python -m streamlit run app.py



The application will be available at:



http://localhost:8501

☁️ Deployment



The application is deployed using Streamlit Community Cloud.



Deployment Configuration

Repository:

PAWAN0207/infosys-ai-knowledge-assistant



Branch:

main



Main File:

app.py



Python:

3.12



The Gemini API key is stored securely using Streamlit Secrets instead of being committed to GitHub.



Example:



GOOGLE\_API\_KEY = "your\_gemini\_api\_key"

🔄 Cloud Startup Behavior



When deployed, the application checks whether a usable ChromaDB knowledge base exists.



If the vector database is missing or empty:



PDF Documents

&#x20;     ↓

PyMuPDF

&#x20;     ↓

Text Chunking

&#x20;     ↓

Gemini Embeddings

&#x20;     ↓

ChromaDB

&#x20;     ↓

RAG Application



This allows the deployed application to initialize its knowledge base from the PDF documents.



🔐 Security Considerations

Implemented

Role-based department filtering

Environment-based API key configuration

No API keys stored in the repository

Grounded response instructions

Out-of-domain response handling

Source citation metadata

Production Improvements



For a real enterprise deployment, additional controls would be recommended:



Enterprise SSO

OAuth / OpenID Connect

Corporate identity provider integration

Server-side authorization

Audit logging

Hosted vector database

Document-level permissions

Encryption at rest and in transit

Enterprise secret management

Retrieval monitoring

LLM observability



This repository demonstrates the application architecture and access-control concept. It is not an official Infosys internal production system.



💡 Why RAG Instead of Fine-Tuning?



Enterprise policies, SOPs, technical documents, and manuals can change frequently.



RAG allows the knowledge base to be updated independently:



Updated Document

&#x20;      ↓

Re-index

&#x20;      ↓

Updated Vector Database

&#x20;      ↓

Updated Retrieval Context

&#x20;      ↓

Latest Grounded Answer



The underlying LLM does not need to be retrained whenever a document changes.



🎯 Key Learning Outcomes



This project demonstrates practical experience with:



Retrieval-Augmented Generation

Vector embeddings

Semantic search

ChromaDB

LangChain

Google Gemini

PDF ingestion pipelines

Metadata-driven retrieval

Role-Based Access Control

Prompt grounding

Hallucination mitigation

Structured LLM responses

Citation generation

Streamlit application development

Cloud deployment

Git and GitHub workflows

🚀 Future Enhancements



Potential production-level improvements include:



🔐 Enterprise SSO authentication

👤 Automatic employee identity detection

🔎 Hybrid semantic + keyword retrieval

🧠 Re-ranking models

📊 Retrieval evaluation metrics

🗄️ Hosted vector database

📑 Document version management

🔄 Automated document ingestion

📝 Audit logging

📈 LLM observability

⚙️ CI/CD automation

🛡️ Enterprise secret management

👨‍💼 Admin dashboard

👨‍💻 Author

Pawan Ajay Prasad



Data Analyst | Junior Data Scientist | ML \& GenAI



Core Interests: Python • SQL • Machine Learning • GenAI • RAG • Power BI



GitHub: https://github.com/PAWAN0207

LinkedIn: https://www.linkedin.com/in/pawan-prasad-analyst/

⭐ Live Application

🚀 Launch Infosys AI Knowledge Assistant



Built with Python • LangChain • Google Gemini • ChromaDB • Streamlit

