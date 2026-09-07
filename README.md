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



