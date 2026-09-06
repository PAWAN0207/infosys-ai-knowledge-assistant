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
```

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

---

# 🔐 Role-Based Access Control (RBAC)

The application implements **Role-Based Access Control** to restrict document retrieval based on an employee's designation.

Each designation is mapped to one or more permitted departments.

Before document chunks are retrieved from ChromaDB, the system determines the departments that the selected role is allowed to access.

```text
Employee Designation
        |
        v
RBAC Permission Mapping
        |
        v
Allowed Departments
        |
        v
ChromaDB Retrieval Filter
        |
        v
Only Authorized Document Chunks
```

This prevents the generation layer from receiving document context outside the user's permitted departments.

---

## 👥 Access Control Matrix

| Employee Designation | Permitted Departments |
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

---

## 🧩 How RBAC Works

The RBAC logic is implemented in:

```text
ai_workflows/query_classification/rbac_classifier.py
```

The application first obtains the departments allowed for the selected designation.

Conceptually:

```python
allowed_departments = get_allowed_departments(designation)
```

The allowed departments are then used as a filter during ChromaDB retrieval.

```text
User Query
    |
    v
Selected Designation
    |
    v
Allowed Departments
    |
    v
ChromaDB Similarity Search
    |
    v
Authorized Chunks Only
```

---

## ✅ Authorized Access Example

### User Role

```text
Software Engineer
```

### Query

```text
What are the key principles of the Infosys microservices architecture?
```

The Software Engineer role has access to:

```text
Engineering
Delivery Operations
PMO
```

Therefore, Engineering documentation can be retrieved.

```text
Software Engineer
       |
       v
Engineering ✓
       |
       v
Relevant Chunks Retrieved
       |
       v
Grounded Gemini Response
```

---

## 🚫 Restricted Access Example

### User Role

```text
HR Associate
```

### Query

```text
What are the key principles of the Infosys microservices architecture?
```

The HR Associate role has access only to:

```text
Human Resources
```

Engineering documentation is outside the permitted department.

Therefore, Engineering content is not available to the retrieval layer for this role.

```text
HR Associate
       |
       v
Human Resources ✓
Engineering      ✗
       |
       v
No authorized Engineering context
       |
       v
Insufficient Context Response
```

Expected response:

```text
Access Denied /
Insufficient domain context available
for your role clearance.
```

---

# 🛡️ Security & Grounding Model

The project uses multiple controls to keep responses grounded and access-aware.

### 1. 🔐 Department-Level Authorization

Users can retrieve information only from departments associated with their selected designation.

### 2. 📚 Metadata-Based Filtering

Each document chunk contains department metadata.

```text
department
source_document
page_number
chunk_id
```

This metadata enables the retrieval layer to apply department restrictions.

### 3. 🧠 Grounded Generation

Only retrieved document context is passed to the Gemini generation layer.

The model is instructed to avoid unsupported external knowledge and assumptions.

### 4. 📖 Source Traceability

Retrieved chunks retain their document and page metadata so that generated responses can be linked back to their source.

### 5. 🚫 Insufficient-Context Handling

If the permitted knowledge domain does not contain sufficient information, the application returns an insufficient-context response rather than intentionally generating an unsupported answer.

---

# ⚠️ Production Security Considerations

The current application uses a **designation selector to simulate employee identity for demonstration purposes**.

For a production enterprise system, the following controls should be added:

- Enterprise SSO authentication
- OAuth 2.0 / OpenID Connect
- Corporate identity provider integration
- Server-side authorization
- User-to-role mapping from an identity system
- Document-level permissions
- Audit logging
- Secret management
- Encryption in transit and at rest
- Access monitoring

The current RBAC implementation demonstrates the **authorization and retrieval-filtering concept** rather than a complete enterprise authentication system.

> **Important:** This is a portfolio/demo project using enterprise-style sample documentation. It is not an official Infosys internal production application.

---

# 📚 Citation & Grounded Response

A key objective of the application is to ensure that generated answers remain connected to the retrieved enterprise documentation.

The system combines **retrieval, metadata, grounded prompting, and source citations** to provide traceable responses.

---

## 🔎 Where Does the Answer Come From?

The answer is generated from the document chunks retrieved from **ChromaDB**.

The flow is:

```text
Employee Query
      |
      v
ChromaDB Semantic Search
      |
      v
Relevant Document Chunks
      |
      v
Grounded Context
      |
      v
Google Gemini
      |
      v
Final Answer
```

Google Gemini is responsible for generating the response, but the response is grounded using the retrieved document context.

---

## 📄 Where Are the Source PDFs?

The source PDFs are stored inside the project's `data/` directory.

```text
data/
├── engineering_guides/
├── hr_policies/
├── project_manuals/
├── sales_assets/
└── sops/
```

These documents are processed by the ingestion pipeline before they become searchable through ChromaDB.

---

## 🏷️ How Are Sources Tracked?

During ingestion, each document chunk receives metadata.

```text
source_document
page_number
department
chunk_id
```

For example:

```text
source_document : Infosys_Microservices_Architecture_Spec.pdf
page_number     : 1
department      : Engineering
chunk_id        : document_p1_c0
```

This metadata travels with the retrieved chunk and can be used to identify the original source.

---

## 📌 Citation Generation

After retrieval, the application passes the document content and its metadata into the grounded response workflow.

The response can contain citation information such as:

```text
Document:
Infosys_Microservices_Architecture_Spec.pdf

Page:
1

Department:
Engineering
```

The Streamlit interface displays this information in the **Citation & Source Panel**.

This provides users with a clear connection between the generated response and the underlying source document.

---

## 🛡️ Grounded Response Behavior

The generation layer uses explicit grounding instructions.

The model is instructed to:

1. Use only the supplied document context.
2. Avoid external knowledge.
3. Avoid unsupported assumptions.
4. Avoid extrapolating beyond the retrieved information.
5. Return an insufficient-context response when the available context is not enough.
6. Map citations to the retrieved document metadata.

Conceptually:

```text
+----------------------+
|    Employee Query    |
+----------+-----------+
           |
           v
+----------------------+
|  Retrieved Chunks    |
|      from ChromaDB  |
+----------+-----------+
           |
           v
+----------------------+
|   Grounded Prompt    |
+----------+-----------+
           |
           v
+----------------------+
|    Google Gemini     |
+----------+-----------+
           |
           v
+----------------------+
|   Structured Output  |
+----------------------+
           |
           +------------------+
           |                  |
           v                  v
       Answer             Citations
           |
           +------------------+
           |
           v
    Confidence Score
           |
           v
   Recommended Action
```

---

# 🚫 Insufficient Context Handling

The application is designed to avoid behaving like a general-purpose chatbot.

If the retrieved context does not contain sufficient information to answer the employee's question, the system can return:

```text
Access Denied /
Insufficient domain context available
for your role clearance.
```

This is particularly important when combined with RBAC.

For example, an HR user asking an Engineering question should not receive Engineering information simply because the LLM knows about the topic from its general training.

---

# 🧪 Example: Grounded Answer

### Employee Designation

```text
Software Engineer
```

### Query

```text
What are the key principles of the Infosys microservices architecture?
```

### Retrieval

```text
Software Engineer
       |
       v
Allowed Departments
       |
       v
Engineering
       |
       v
ChromaDB
       |
       v
Relevant Engineering Chunks
```

### Generation

```text
Retrieved Engineering Context
             +
          User Query
             |
             v
       Google Gemini
             |
             v
      Grounded Response
```

### Result

```text
Answer
Confidence Score
Recommended Action
Source Document
Page Number
```

---

# 🎯 Why Citations Matter

Citation-backed responses are important for enterprise applications because users need to understand **where an answer came from**.

The citation layer provides:

- 📄 Source document identification
- 📑 Page-level traceability
- 🔐 Department context
- 🔎 Retrieval transparency
- 🧠 Better trust in generated responses

This makes the system more suitable for enterprise knowledge discovery than a basic standalone chatbot.