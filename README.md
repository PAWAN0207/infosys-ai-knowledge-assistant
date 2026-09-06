# 🤖 Infosys AI Knowledge Assistant

### Enterprise RAG System with RBAC, Grounded Responses & Source Citations

An enterprise-style **Retrieval-Augmented Generation (RAG)** application that helps employees search internal knowledge documents using natural language.

Built with **Python, LangChain, Google Gemini, ChromaDB, and Streamlit**.

---

## 🚀 Live Demo

### 👉 [Open the Live Application](https://infosys-ai-knowledge-assistant-qsjefhgbq7np44rb9v597g.streamlit.app/)

The application is deployed using **Streamlit Community Cloud**.

### What you can test

- 🔎 Semantic document search
- 🔐 Role-based access control
- 📚 Source document citations
- 🧠 Grounded Gemini responses
- 🛡️ Out-of-domain query handling

---

# 📌 Project Overview

The **Infosys AI Knowledge Assistant** is an enterprise-style RAG application designed to help employees retrieve information from internal knowledge documents using natural-language queries.

The system works with different types of enterprise documentation, including:

- 📘 Technical architecture guides
- 👥 HR policies
- 📋 Project manuals
- 💼 Sales documents
- 🚨 Operational SOPs

Instead of directly asking an LLM to answer a question from its general knowledge, the application first retrieves relevant information from the enterprise knowledge base.

The retrieved information is then provided to Google Gemini as grounded context for generating the final response.

This architecture helps improve:

- 🎯 Answer relevance
- 📚 Source traceability
- 🔐 Access control
- 🛡️ Grounded response behavior
- 🔎 Enterprise document discovery

---

# ✨ Key Features

### 🔎 Semantic Search

Search enterprise documents using natural-language questions instead of relying only on exact keyword matching.

### 🔐 Role-Based Access Control

Employee designations are mapped to permitted departments.

The system applies the department filter during document retrieval.

### 🧠 Grounded AI Responses

Google Gemini generates responses using the retrieved document context.

The system is instructed not to rely on unsupported external knowledge.

### 📚 Source Citations

Every retrieved document chunk contains metadata such as:

- Document name
- Page number
- Department
- Chunk ID

This information is displayed in the Citation & Source Panel.

### 🛡️ Insufficient-Context Protection

If relevant information is not available within the user's permitted knowledge domain, the system returns an insufficient-context response instead of generating an unsupported answer.

### 📊 Confidence Score

The generated response includes a confidence score representing the model's assessment of the available context.

### 💡 Recommended Action

The application provides a recommended next action along with the generated response.

### 🖥️ Interactive Streamlit Interface

Employees can select their designation, submit a natural-language query, and view the grounded answer together with its source information.