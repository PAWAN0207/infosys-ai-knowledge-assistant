# 🤖 Infosys AI Knowledge Assistant

<p align="center">

<a href="https://infosys-ai-knowledge-assistant-4ovi.onrender.com/docs" target="_blank">
  <img src="https://img.shields.io/badge/FastAPI-API%20Docs-009688?logo=fastapi&logoColor=white" alt="FastAPI API Docs"/>
</a>

<a href="https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/" target="_blank">
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

## 📌 Project Overview

An enterprise-style **Retrieval-Augmented Generation (RAG)** application that enables employees to search internal knowledge documents using natural-language queries.

The system combines:

- 🔐 **Role-Based Access Control (RBAC)**
- 🔎 **Semantic Vector Retrieval**
- 🧠 **Grounded Google Gemini Responses**
- 📚 **Source Citations & Page-Level Traceability**
- 🛡️ **Insufficient-Context Handling**
- 🧪 **Retrieval & Generation Evaluation**

The application is designed around an enterprise knowledge-assistant workflow where users can access only the information permitted for their selected role.

### 🏢 Knowledge Domains

| Domain | Example Content |
|---|---|
| 📘 Engineering | Microservices Architecture |
| 👥 Human Resources | Leave & HR Policies |
| 📋 PMO | Agile Execution Framework |
| 💼 Sales | Cloud Transformation Capabilities |
| 🚨 Delivery Operations | Severity-1 Incident SOP |

---

## 🚀 Live Demo

### 👉 [Open the Live Application](https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/)

**Frontend:** Streamlit Community Cloud  
**Backend:** FastAPI on Render

Try the application by:

1. Selecting an employee designation.
2. Asking a question about the enterprise knowledge base.
3. Reviewing the grounded response.
4. Checking the confidence score.
5. Inspecting source citations.
6. Testing RBAC restrictions with different roles.

---

## ⭐ Key Highlights

| Capability | Implementation |
|---|---|
| 🔎 Semantic Search | ChromaDB + Gemini Embeddings |
| 🔐 Access Control | Department-level RBAC |
| 🧠 LLM | Google Gemini |
| 📚 Grounding | Retrieved document context |
| 📖 Citations | Document + Page + Department metadata |
| ⚡ Backend | FastAPI |
| 🖥️ Frontend | Streamlit |
| 🧪 Evaluation | Retrieval + Generation + Grounding |
| ☁️ Deployment | Streamlit Cloud + Render |
| 🔄 CI | GitHub Actions + Pylint |

---