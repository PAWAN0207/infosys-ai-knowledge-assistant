# 🤖 Infosys AI Knowledge Assistant

<p align="center">

<a href="https://infosys-ai-knowledge-assistant-4ovi.onrender.com/docs" target="_blank">
  <img src="https://img.shields.io/badge/FastAPI-API%20Docs-009688?logo=fastapi&logoColor=white" alt="FastAPI API Docs"/>
</a>

<a href="https://infosys-ai-knowledge-assistant-qsjefhgbq7np44rb9v597g.streamlit.app/" target="_blank">
  <img src="https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white" alt="Live Streamlit App"/>
</a>

<a href="https://github.com/PAWAN0207/infosys-ai-knowledge-assistant" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white" alt="GitHub Repository"/>
</a>

<img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12"/>
<img src="https://img.shields.io/badge/LangChain-RAG-1C3C3C" alt="LangChain RAG"/>
<img src="https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?logo=google" alt="Google Gemini"/>
<img src="https://img.shields.io/badge/ChromaDB-Vector%20DB-orange" alt="ChromaDB"/>
<img src="https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions"/>

</p>
---

## 📖 Project Introduction

The **Infosys AI Knowledge Assistant** is an enterprise-style **Retrieval-Augmented Generation (RAG)** application that helps employees retrieve relevant information from internal knowledge documents using natural-language queries.

The system combines **RBAC, semantic search, vector retrieval, Google Gemini, and source citations** to provide secure and grounded responses.

It is designed to work across multiple enterprise domains such as:

- 📘 Engineering
- 👥 Human Resources
- 📋 PMO / Project Management
- 💼 Sales
- 🚨 Delivery Operations

The main objective is to ensure that users receive **relevant, role-authorized, and traceable information** instead of unrestricted responses from a general-purpose LLM.

## 🚀 Live Demo

### 👉 [Open the Live Application](https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/)

The frontend is deployed using **Streamlit Community Cloud** and communicates with the deployed **FastAPI backend** over HTTPS.

### 🔗 Backend API Documentation

👉 [Open FastAPI Swagger Docs](https://infosys-ai-knowledge-assistant-4ovi.onrender.com/docs)

The Swagger interface allows you to test the available API endpoints directly.

### What You Can Test

- 🔎 Semantic document search
- 🔐 Role-based access control
- 📚 Source document citations
- 🧠 Grounded Gemini responses
- 📊 Confidence score
- 💡 Recommended action
- 🛡️ Insufficient-context handling
- 🚫 Restricted department access

---

## 📌 Project Overview

The **Infosys AI Knowledge Assistant** is an enterprise-style RAG application designed to help employees retrieve information from internal knowledge documents using natural-language queries.

The system works with enterprise knowledge across multiple business domains:

- 📘 Technical Engineering Guides
- 👥 Human Resources Policies
- 📋 PMO / Project Management Documents
- 💼 Sales & Business Development Documents
- 🚨 Delivery Operations SOPs

Instead of directly asking an LLM to answer a question using its general knowledge, the application first retrieves relevant information from the authorized enterprise knowledge base.

The retrieved document context is then provided to **Google Gemini** to generate a grounded response.

### High-Level Workflow

```text
Employee Query
      ↓
Role & Permission Check
      ↓
Authorized Document Retrieval
      ↓
Relevant Context
      ↓
Grounded Gemini Response
      ↓
Answer + Citations
```

## ✨ Key Features

### 🔎 Semantic Search

Users can search enterprise knowledge documents using natural-language questions instead of relying only on exact keyword matching.

The system uses vector embeddings and **ChromaDB similarity search** to retrieve semantically relevant document chunks.

---

### 🔐 Role-Based Access Control

The application maps employee designations to permitted business departments.

RBAC is applied during document retrieval so that only authorized document chunks are available to the generation layer.

```text
Employee Designation
        ↓
Permission Mapping
        ↓
Allowed Departments
        ↓
ChromaDB Retrieval Filter
        ↓
Authorized Document Context
```
---

### 🧠 Grounded Gemini Responses

Google Gemini generates responses using the retrieved document context.

The generation workflow instructs the model to:

- Use the supplied document context
- Avoid unsupported assumptions
- Avoid relying on external knowledge
- Avoid extrapolating beyond the retrieved information
- Return an insufficient-context response when the available context is not enough

---

### 📚 Source Citations

Retrieved document chunks contain metadata including:

```text
Source Document
Page Number
Department
Chunk ID
```
---

### 🛡️ Insufficient-Context Handling

The application is designed as an enterprise knowledge assistant rather than a general-purpose chatbot.

When sufficient authorized context is not available, the system can return an insufficient-context response instead of intentionally generating an unsupported answer.

Example:

```text
Access Denied /
Insufficient domain context available
for your role clearance.
```

---

### 📊 Confidence Score

The structured response includes a confidence score representing the model's assessment of the available retrieved context.

---

### 💡 Recommended Action

The application can provide a recommended next action along with the generated response.

This helps turn the retrieved information into a more actionable response.

---

### 🖥️ Interactive Streamlit Interface

The Streamlit frontend allows users to:

1. Select an employee designation.
2. Enter a natural-language query.
3. Submit the query to the FastAPI backend.
4. View the generated response.
5. Review the confidence score.
6. Review the recommended action.
7. Inspect source document citations.

---

### 🔗 FastAPI Backend

The RAG functionality is exposed through a FastAPI backend.

The backend provides:

```text
GET  /health
POST /query
GET  /docs
```
The Streamlit frontend communicates with the FastAPI service over HTTPS.

---

### 🧪 Evaluation Framework

The project includes dedicated evaluation scripts for:

- Retrieval quality
- RBAC behavior
- Generation quality
- Expected keyword/fact coverage
- Citation presence
- Expected source document
- Grounding behavior

Evaluation datasets and scripts are available in the `evaluation/` directory.

---
## 🏗️ System Architecture

The application follows a layered architecture where the Streamlit frontend communicates with the FastAPI backend, while the RAG engine handles authorization, retrieval, grounding, and response generation.

```text
                    ┌─────────────────────────┐
                    │        User / Employee  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Streamlit Frontend    │
                    │  Interactive Web UI      │
                    └────────────┬────────────┘
                                 │ HTTPS
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │      /query /health     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       RBAC Layer        │
                    │ Role → Departments      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   RAG Retrieval Engine  │
                    │  LangChain + ChromaDB   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Authorized Context    │
                    │ Document Chunks +       │
                    │ Metadata + Citations    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Google Gemini      │
                    │   Grounded Generation   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Answer + Citations +    │
                    │ Confidence + Action     │
                    └─────────────────────────┘
```
### Deployment Architecture

```text
Browser
   │
   ▼
Streamlit Community Cloud
   │
   │ HTTPS
   ▼
Render FastAPI Service
   │
   ▼
RBAC + RAG Engine
   │
   ├── ChromaDB
   │
   └── Google Gemini
```
### Architecture Principles

- **Separation of concerns** between frontend, API, RBAC, retrieval, and generation.
- **Role-aware retrieval** before the LLM receives document context.
- **Grounded generation** using retrieved enterprise documents.
- **Source traceability** through document and page metadata.
- **API-based communication** between the Streamlit frontend and FastAPI backend.

---

## 🔄 RAG Pipeline

The application follows a structured **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant enterprise information and generate grounded responses.

### Step-by-Step RAG Workflow

```text
User Query
    ↓
Query + Employee Designation
    ↓
RBAC Permission Mapping
    ↓
Allowed Department Filter
    ↓
Query Embedding
    ↓
ChromaDB Similarity Search
    ↓
Top-K Relevant Document Chunks
    ↓
Retrieval Validation
    ↓
Citation Context Builder
    ↓
Grounded Gemini Generation
    ↓
Structured Response
    ↓
Answer + Citations + Confidence + Recommended Action
```
### 1️⃣ Document Ingestion

Enterprise PDF documents are loaded using **PyMuPDF** and divided into smaller chunks using a recursive text splitter.

Each chunk is enriched with metadata such as:

```text
Source Document
Page Number
Department
Chunk ID
```
---

### 2️⃣ Embedding Generation

The document chunks are converted into vector embeddings using the **Google Gemini embedding model**.

These embeddings allow the system to perform semantic similarity search rather than relying only on keyword matching.

---

### 3️⃣ Vector Storage

The generated embeddings and document chunks are stored in **ChromaDB**, which acts as the vector database for the application.

```text
PDF Documents
      ↓
Text Chunks
      ↓
Gemini Embeddings
      ↓
ChromaDB
```
---

### 4️⃣ Role-Aware Retrieval

Before retrieving documents, the employee's designation is mapped to the departments they are authorized to access.

The ChromaDB retrieval is then filtered using the permitted departments.

```text
Designation
     ↓
RBAC Permission Matrix
     ↓
Allowed Departments
     ↓
Filtered ChromaDB Search
```
---
### 5️⃣ Context Construction

The retrieved document chunks are combined into a structured context block.

The context includes source metadata so that the final response can provide traceable citations.
---

### 6️⃣ Grounded Generation

The authorized context is passed to **Google Gemini** with instructions to generate the response using only the supplied enterprise context.

The generation layer is instructed to avoid unsupported assumptions and return an insufficient-context response when the retrieved information is not enough.

---

### 7️⃣ Structured Response

The final response follows a structured schema containing:

```text
Answer
Citations
Confidence Score
Recommended Action
```
## 🔐 Role-Based Access Control (RBAC)

The application implements **Role-Based Access Control (RBAC)** to ensure that employees can retrieve information only from departments authorized for their designation.

### RBAC Workflow

```text
Employee Designation
        ↓
Permission Matrix
        ↓
Allowed Departments
        ↓
ChromaDB Metadata Filter
        ↓
Authorized Document Chunks
        ↓
Gemini Generation
```
### Department-Level Permissions

The system defines permissions based on employee designation.

| Designation | Authorized Departments |
|---|---|
| Software Engineer | Engineering, Delivery Operations, PMO |
| Senior Software Engineer | Engineering, Delivery Operations, PMO |
| DevOps Lead | Engineering, Delivery Operations |
| Solutions Architect | Engineering, Delivery Operations, PMO |
| Engineering Lead | Engineering, Delivery Operations, PMO |
| Sales Executive | Sales, Human Resources |
| Business Development Manager | Sales, PMO |
| Account Manager | Sales |
| Sales Enablement Lead | Sales, Human Resources, PMO |
| Delivery Manager | Delivery Operations, PMO, Engineering |
| PMO Lead | PMO, Delivery Operations, Engineering |
| Operations Lead | Delivery Operations |
| HR Associate | Human Resources |
| HR Operations Lead | Human Resources |
| Senior Manager | Engineering, Delivery Operations, PMO, Human Resources, Sales |

### 🔒 Retrieval-Level Enforcement

RBAC is enforced **before the document context reaches the LLM**.

The user's designation is converted into a list of permitted departments, and the vector retrieval layer uses this information to restrict the searchable document context.

```python
allowed_departments = QueryRBACClassifier.get_allowed_departments(
    designation
)
```

The retrieval layer then applies the department restriction during ChromaDB similarity search.

### 🚫 Unauthorized Access

If a user attempts to access information outside their authorized domain, the system can return:

```text
Access Denied /
Insufficient domain context available
for your role clearance.
```
---
## 📚 Citation & Grounding

The system is designed to keep generated responses connected to the retrieved enterprise documents.

### 🔗 Source Traceability

Each retrieved document chunk contains metadata that can be used to identify the source of the information.

The citation metadata includes:

```text
Source Document
Page Number
Department
Chunk ID
```
This allows users to trace an answer back to the relevant enterprise document and page.

---

### 🧠 Grounded Response Generation

The retrieved and authorized context is provided to **Google Gemini** as the basis for response generation.

The generation instructions emphasize:

- Use only the supplied enterprise context.
- Do not introduce unsupported facts.
- Do not rely on external knowledge.
- Do not extrapolate beyond the retrieved information.
- Return an insufficient-context response when the available context is not enough.

---

### 🛡️ Context-Aware Answering

The system does not treat every query as a general knowledge question.

Instead, the response depends on:

```text
User Query
     ↓
User Role
     ↓
Authorized Retrieval
     ↓
Retrieved Context
     ↓
Grounded Generation
     ↓
Cited Response
```
This approach improves **traceability and response reliability** for enterprise knowledge queries.

---

### 📌 Citation Example

A generated response can reference information using the retrieved document metadata:

```text
Source: Infosys_Microservices_Architecture_Spec.pdf
Page: 2
Department: Engineering
```
The citation information is returned as part of the structured response and displayed by the application.

---

### ⚠️ Grounding Boundary

If the retrieved authorized context does not contain enough information to answer a question, the system is designed to avoid intentionally fabricating an answer.

Instead, it can return:

```text
Access Denied /
Insufficient domain context available
for your role clearance.
```
---
## 🧪 Evaluation & Testing

The project includes a dedicated evaluation framework to measure **retrieval quality, RBAC behavior, generation quality, citation accuracy, and grounding behavior**.

### 📊 Evaluation Components

The evaluation framework covers three major areas:

```text
Evaluation Framework
        │
        ├── Retrieval Evaluation
        │
        ├── Generation Evaluation
        │
        └── Grounding Evaluation
```
---

### 🔎 Retrieval Evaluation

The retrieval evaluation tests whether the correct enterprise document and department are retrieved for a given query.

The evaluation dataset contains:

- 20 authorized RAG test cases
- 5 RBAC denial test cases
- Multiple enterprise departments
- Expected documents and answer keywords

The following metrics are calculated:

| Metric | Description |
|---|---|
| Hit@1 | Expected document appears as the top result |
| Hit@3 | Expected document appears within top 3 results |
| Hit@5 | Expected document appears within top 5 results |
| MRR | Mean Reciprocal Rank of the expected result |
| Department Match Rate | Retrieved department matches the expected department |
| RBAC Pass Rate | Authorization behavior matches expectations |

---

### ✅ Retrieval Evaluation Results

The production RBAC configuration was evaluated against the retrieval test dataset.

```text
Overall Pass Rate:        100.00%
Hit@1:                    100.00%
Hit@3:                    100.00%
Hit@5:                    100.00%
Mean Reciprocal Rank:     1.0000
Department Match Rate:   100.00%
RBAC Pass Rate:           100.00%

Passed: 25 / 25
```

Average retrieval latency was approximately **1.21 seconds** across the evaluation run.

---

### 🧠 Generation Evaluation

The generation evaluator tests the complete RAG generation workflow using the production `EnterpriseGroundedEngine`.

It evaluates:

- Expected keyword coverage
- Citation presence
- Expected source document citation
- RBAC denial behavior
- Confidence score
- Generation latency

The generation evaluation dataset contains **5 test cases** covering authorized queries and an RBAC denial scenario.

### ✅ Generation Evaluation Results

```text
Overall Pass Rate:                 100.00%
Authorized Generation Pass Rate:   100.00%
Expected Keyword Coverage:         100.00%
Citation Presence Rate:            100.00%
Expected Document Citation Rate:   100.00%
RBAC Generation Pass Rate:         100.00%

Passed: 5 / 5
```

Average generation latency was approximately **19.6 seconds** for the evaluation run.

---

### 🛡️ Grounding Evaluation

A separate grounding evaluator checks whether generated responses contain the expected facts from the authorized retrieved context.

It evaluates:

- Expected fact coverage
- Citation presence
- Expected source document
- RBAC denial behavior
- Confidence score
- Generation latency

The grounding evaluation framework is implemented and can be executed independently.

> **Evaluation Note:** The full grounding run was affected by the Gemini free-tier request quota. Three successfully executed cases achieved 100% expected fact coverage with citations and the expected source document.

Therefore, the project does **not** claim a 100% grounding benchmark from the quota-limited run.

---

### 🧪 Evaluation Files

The evaluation framework is organized under:

```text
evaluation/
├── evaluation_dataset.json
├── generation_evaluation_dataset.json
├── grounding_evaluation_dataset.json
├── evaluate_rag.py
├── evaluate_generation.py
└── evaluate_grounding.py
```
---

## 🛠️ Technology Stack

The project uses a combination of modern AI, backend, vector database, and deployment technologies.

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python 3.12 | Core application development |
| Frontend | Streamlit | Interactive user interface |
| Backend | FastAPI | REST API and backend service |
| RAG Framework | LangChain | Retrieval and generation workflow |
| LLM | Google Gemini | Grounded response generation |
| Embeddings | Google Gemini Embeddings | Document and query vectorization |
| Vector Database | ChromaDB | Semantic vector storage and retrieval |
| Document Processing | PyMuPDF | PDF document loading |
| Text Splitting | Recursive Character Text Splitter | Document chunking |
| Data Validation | Pydantic | Structured request/response schemas |
| API Server | Uvicorn | FastAPI application server |
| HTTP Client | Requests | Streamlit → FastAPI communication |
| Environment Management | python-dotenv | Environment variable loading |
| Version Control | Git + GitHub | Source code management |
| CI | GitHub Actions | Automated code quality checks |
| Frontend Deployment | Streamlit Community Cloud | Live web application |
| Backend Deployment | Render | FastAPI deployment |

### 🔧 Core AI Components

```text
Google Gemini
     │
     ├── Gemini Embeddings
     │
     └── Gemini LLM
              │
              ▼
         LangChain RAG
              │
              ▼
           ChromaDB
```
----
## 📁 Project Structure

The project is organized into separate modules for the frontend, API, RAG engine, document ingestion, RBAC, and evaluation.

```text
infosys-ai-knowledge-assistant/
│
├── ai_workflows/
│   ├── grounded_synthesis/
│   │   └── synthesis_engine.py
│   │
│   └── query_classification/
│       └── rbac_classifier.py
│
├── data/
│   ├── engineering_guides/
│   ├── hr_policies/
│   ├── project_manuals/
│   ├── sales_assets/
│   └── sops/
│
├── ingestion_pipeline/
│   └── embedding_jobs/
│       └── vector_indexer.py
│
├── evaluation/
│   ├── evaluation_dataset.json
│   ├── generation_evaluation_dataset.json
│   ├── grounding_evaluation_dataset.json
│   ├── evaluate_rag.py
│   ├── evaluate_generation.py
│   └── evaluate_grounding.py
│
├── app.py
├── api.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── vector_db/
```
### 📂 Directory Responsibilities

| Directory / File | Responsibility |
|---|---|
| `app.py` | Streamlit frontend |
| `api.py` | FastAPI backend and API endpoints |
| `ai_workflows/` | Core RAG and RBAC logic |
| `grounded_synthesis/` | Grounded response generation |
| `query_classification/` | Role and department authorization |
| `ingestion_pipeline/` | PDF processing and vector indexing |
| `data/` | Enterprise knowledge documents |
| `evaluation/` | Retrieval, generation, and grounding evaluation |
| `vector_db/` | Local ChromaDB persistence |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `.gitignore` | Files excluded from Git |

---

## 🧩 Core Components

The application is divided into modular components, with each component responsible for a specific part of the RAG workflow.

### 🖥️ Streamlit Frontend

**File:** `app.py`

The Streamlit application provides the user-facing interface.

Responsibilities include:

- Employee designation selection
- Natural-language query input
- FastAPI API communication
- Response display
- Confidence score display
- Recommended action display
- Source citation display
- API connection status

---

### 🔗 FastAPI Backend

**File:** `api.py`

The FastAPI service acts as the backend API layer between the frontend and the RAG engine.

Main endpoints:

```text
GET  /health
POST /query
GET  /docs
```
### 🔗 API Responsibilities

The FastAPI layer is responsible for connecting the Streamlit frontend with the RAG workflow.

```text
Streamlit UI
      ↓
FastAPI /query
      ↓
EnterpriseGroundedEngine
      ↓
RAG Processing
      ↓
Structured Response
      ↓
FastAPI
      ↓
Streamlit UI
```
### 🧠 Enterprise Grounded Engine

**File:** `ai_workflows/grounded_synthesis/synthesis_engine.py`

The `EnterpriseGroundedEngine` handles the main RAG workflow.

Its responsibilities include:

- Query embedding
- Role-aware document retrieval
- ChromaDB similarity search
- Retrieval validation
- Context construction
- Grounded Gemini generation
- Structured response generation
- Citation handling

---

### 🔐 RBAC Classifier

**File:** `ai_workflows/query_classification/rbac_classifier.py`

The `QueryRBACClassifier` maps employee designations to the departments they are authorized to access.

Example:

```text
Software Engineer
        ↓
Engineering
Delivery Operations
PMO
```
The resulting department list is used to restrict ChromaDB retrieval.

---

### 📚 Vector Indexer

**File:** `ingestion_pipeline/embedding_jobs/vector_indexer.py`

The vector indexer creates the ChromaDB knowledge base from enterprise PDF documents.

The indexing workflow is:

```text
PDF Documents
      ↓
PyMuPDF Loading
      ↓
Recursive Text Splitting
      ↓
Metadata Enrichment
      ↓
Gemini Embeddings
      ↓
ChromaDB
```
---

### 🧪 Evaluation Modules

**Directory:** `evaluation/`

The evaluation framework contains separate modules for measuring different parts of the RAG system.

```text
evaluate_rag.py
        ↓
Retrieval + RBAC Evaluation

evaluate_generation.py
        ↓
Generation + Citation Evaluation

evaluate_grounding.py
        ↓
Fact Coverage + Grounding Evaluation
```
---

### 🔄 Component Interaction

The major components work together as follows:

```text
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
RBAC Classifier
 ↓
ChromaDB Retrieval
 ↓
Context Builder
 ↓
Google Gemini
 ↓
Structured Response
 ↓
Citations + Confidence + Recommended Action
```
---
## ⚙️ Installation & Setup

### Prerequisites

- Python 3.12+
- Conda
- Git
- Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/PAWAN0207/infosys-ai-knowledge-assistant.git
cd infosys-ai-knowledge-assistant
```
### 2. Create the Environment
```
conda create -n infosys-rag python=3.12 -y
conda activate infosys-rag
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Configure Environment Variables
```
GOOGLE_API_KEY=your_gemini_api_key
```
> **Security:** Never commit `.env` or expose API keys. Use `.env.example` as the configuration template.

### 5. Verify Installation

```bash
python --version
pip check
```

### Why this version is better

- **Crisp** — recruiter ko unnecessary dependency list nahi dikhani.
- **Industry-standard flow** — Prerequisites → Clone → Environment → Dependencies → Configuration → Verification.
- **Security-conscious** — API key handling clearly mentioned.
- **Reproducible** — exact commands available.

---
