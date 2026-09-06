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

---

# 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation architecture where access control is applied before document context is sent to the LLM.

```text
+-------------------+
|     Employee      |
|      Query        |
+---------+---------+
          |
          v
+-------------------+
| Employee          |
| Designation       |
+---------+---------+
          |
          v
+-------------------+
| RBAC Department   |
|     Filter        |
+---------+---------+
          |
          v
+-------------------+
|     ChromaDB      |
| Semantic Retrieval|
+---------+---------+
          |
          v
+-------------------+
| Relevant Document |
|      Chunks       |
+---------+---------+
          |
          v
+-------------------+
| Grounded Context  |
|      Builder      |
+---------+---------+
          |
          v
+-------------------+
|   Google Gemini   |
|  Response Engine  |
+---------+---------+
          |
          v
+-----------------------------+
|       Final Response        |
|                             |
|  Answer                     |
|  Confidence Score           |
|  Recommended Action         |
|  Source Citation            |
+-----------------------------+

---

# 🔄 RAG Pipeline

The RAG pipeline converts enterprise PDF documents into searchable vector representations and uses them to answer employee questions with relevant context.

## 1. 📄 Document Ingestion

The source documents are stored inside the `data/` directory and organized by business domain.

```text
data/
├── engineering_guides/
├── hr_policies/
├── project_manuals/
├── sales_assets/
└── sops/
```

The ingestion pipeline automatically discovers PDF files from these directories.

---

## 2. 📖 PDF Text Extraction

The application uses **PyMuPDFLoader** to extract text from each PDF.

Documents are processed page by page so that the original page number can be preserved for source citations.

```text
PDF
 ↓
PyMuPDFLoader
 ↓
Page-wise Text
```

---

## 3. ✂️ Text Chunking

The extracted text is split into smaller chunks using LangChain's:

```text
RecursiveCharacterTextSplitter
```

Configuration:

```text
Chunk Size    : 1000 characters
Chunk Overlap : 200 characters
```

The overlap helps maintain contextual information between neighboring chunks.

```text
Large Document
      |
      v
+-------------+
|   Chunk 1   |
+-------------+
      |
      v
+-------------+
|   Chunk 2   |
+-------------+
      |
      v
+-------------+
|   Chunk 3   |
+-------------+
```

---

## 4. 🏷️ Metadata Creation

Every document chunk is stored together with metadata.

```text
source_document
page_number
department
chunk_id
```

Example:

```text
source_document : Infosys_Microservices_Architecture_Spec.pdf
page_number     : 1
department      : Engineering
chunk_id        : ..._p1_c0
```

This metadata enables:

- 🔐 Department-level filtering
- 📚 Source citations
- 📄 Page-level traceability
- 🔎 Document identification

---

## 5. 🧠 Embedding Generation

Each text chunk is converted into a numerical vector representation using Google's embedding model:

```text
gemini-embedding-2-preview
```

Conceptually:

```text
Text Chunk
    |
    v
Embedding Model
    |
    v
Vector Representation
```

Semantically similar pieces of text are represented by vectors that are close to each other in the embedding space.

---

## 6. 🗄️ Vector Storage with ChromaDB

The generated embeddings, text chunks, and metadata are stored in **ChromaDB**.

```text
+---------------------------+
|         ChromaDB          |
+---------------------------+
| Text Chunk                |
| Embedding Vector          |
| Source Document           |
| Page Number               |
| Department                |
| Chunk ID                  |
+---------------------------+
```

The vector database is used during question answering to perform semantic similarity search.

---

## 7. 🔎 Semantic Retrieval

When an employee submits a question, the system searches ChromaDB for the most relevant document chunks.

The application retrieves the **top 5 relevant chunks** while applying the employee's department permissions.

```text
Employee Query
      |
      v
Query Embedding
      |
      v
RBAC Department Filter
      |
      v
ChromaDB Similarity Search
      |
      v
Top 5 Relevant Chunks
```

---

## 8. 🛡️ Grounded Context Construction

The retrieved chunks are combined into a structured context block.

Only this retrieved context is provided to the generation layer.

```text
Retrieved Chunks
       |
       v
Context Builder
       |
       v
Grounded Context
```

The system instructs the LLM to avoid using unsupported external knowledge.

---

## 9. 🤖 Response Generation

The grounded context and employee query are sent to **Google Gemini**.

The model generates a structured response containing:

```text
Answer
Confidence Score
Citations
Recommended Action
```

```text
Grounded Context
       +
Employee Query
       |
       v
Google Gemini
       |
       v
Structured Response
```

---

## 🔗 Complete Pipeline

```text
+-------------------+
|   Enterprise PDFs |
+---------+---------+
          |
          v
+-------------------+
|  PyMuPDFLoader    |
+---------+---------+
          |
          v
+-------------------+
|  Text Chunking    |
|  1000 / 200       |
+---------+---------+
          |
          v
+-------------------+
| Metadata Creation |
+---------+---------+
          |
          v
+-------------------+
| Gemini Embeddings |
+---------+---------+
          |
          v
+-------------------+
|     ChromaDB      |
+---------+---------+
          |
          | User Query
          v
+-------------------+
|   RBAC Filtering  |
+---------+---------+
          |
          v
+-------------------+
| Semantic Retrieval|
|    Top 5 Chunks   |
+---------+---------+
          |
          v
+-------------------+
| Grounded Context  |
+---------+---------+
          |
          v
+-------------------+
|   Google Gemini   |
+---------+---------+
          |
          v
+-------------------+
|  Final Response   |
|   + Citations     |
+-------------------+
```