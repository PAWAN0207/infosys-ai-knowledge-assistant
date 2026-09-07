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