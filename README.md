\# 🤖 Infosys AI Knowledge Assistant



> \*\*Enterprise Retrieval-Augmented Generation (RAG) system with role-based access control, grounded responses, and source citations.\*\*



\[!\[Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)

\[!\[Streamlit](https://img.shields.io/badge/Streamlit-1.63-red)](https://streamlit.io/)

\[!\[LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://www.langchain.com/)

\[!\[ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-purple)](https://www.trychroma.com/)

\[!\[Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-orange)](https://ai.google.dev/)



\## 🚀 Live Demo



\### 👉 \[Open Infosys AI Knowledge Assistant](https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/)



The application is publicly deployed using Streamlit Community Cloud.



\---



\## 📌 Project Overview



The \*\*Infosys AI Knowledge Assistant\*\* is an enterprise-style RAG application designed to help employees retrieve information from internal policies, SOPs, architecture guides, project manuals, and sales documentation.



Instead of sending a user query directly to an LLM, the system first retrieves relevant information from a controlled document knowledge base and then generates an answer using only the retrieved context.



The system also applies \*\*Role-Based Access Control (RBAC)\*\* before document retrieval so that users can only retrieve information from departments permitted for their selected designation.



\### Key objectives



\- 🔎 Semantic search across enterprise PDF documents

\- 🧠 Retrieval-Augmented Generation using Google Gemini

\- 🔐 Role-based document access

\- 📚 Citation-backed answers

\- 🛡️ Zero-extrapolation / grounded response behavior

\- 📊 Confidence scoring

\- 💡 Recommended actions for employees

\- 🌐 Interactive Streamlit web interface



\---



\# 🏗️ System Architecture



```text

&#x20;                        ┌─────────────────────┐

&#x20;                        │      Employee       │

&#x20;                        │      Query          │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │ Employee Designation│

&#x20;                        │      / RBAC         │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │  RBAC Department    │

&#x20;                        │      Filter         │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │      ChromaDB       │

&#x20;                        │ Semantic Retrieval  │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                             Top-K Chunks

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │ Grounded Context    │

&#x20;                        │     Builder         │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │   Google Gemini     │

&#x20;                        │    Generation       │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                ┌──────────────────────────────────┐

&#x20;                │ Grounded Answer + Citation +     │

&#x20;                │ Confidence + Recommended Action │

&#x20;                └──────────────────────────────────┘

```



\---



\# 🔄 RAG Workflow



The application follows the following pipeline:



\### 1. Document ingestion



PDF documents are stored under the `data/` directory and organized by business domain.



```text

data/

├── engineering\_guides/

├── hr\_policies/

├── project\_manuals/

├── sales\_assets/

└── sops/

```



\### 2. PDF parsing



`PyMuPDFLoader` extracts text from each PDF page.



\### 3. Text chunking



Documents are split using LangChain's `RecursiveCharacterTextSplitter`.



Configuration:



```text

Chunk size   : 1000 characters

Chunk overlap: 200 characters

```



The overlap helps preserve context between neighboring chunks.



\### 4. Metadata creation



Each chunk receives metadata such as:



```text

source\_document

page\_number

department

chunk\_id

```



This metadata is later used for filtering and citations.



\### 5. Embeddings



Google's Gemini embedding model converts document chunks into numerical vector representations.



```text

gemini-embedding-2-preview

```



\### 6. Vector storage



The generated embeddings and document metadata are stored in \*\*ChromaDB\*\*.



\### 7. Query retrieval



When an employee submits a question:



```text

User Query

&#x20;   ↓

RBAC Department Filter

&#x20;   ↓

ChromaDB Semantic Search

&#x20;   ↓

Top 5 Relevant Chunks

```



\### 8. Grounded generation



The retrieved chunks are passed to Google Gemini with strict grounding instructions.



The model is instructed to:



\- Use only the supplied context

\- Avoid external knowledge

\- Avoid assumptions

\- Return insufficient-context responses when the required information is unavailable

\- Map citations to the retrieved document metadata



\---



\# 🔐 Role-Based Access Control



The application applies department-level access control based on employee designation.



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



\### Example



A \*\*Software Engineer\*\* can access Engineering documentation.



An \*\*HR Associate\*\* can access Human Resources documentation but cannot retrieve Engineering documentation.



For example:



```text

HR Associate

&#x20;    ↓

"What are the principles of microservices architecture?"

&#x20;    ↓

Engineering department not permitted

&#x20;    ↓

Access Denied / Insufficient domain context

```



This prevents unauthorized document retrieval at the application retrieval layer.



> \*\*Note:\*\* The current demo uses a designation selector to simulate employee identity and RBAC. A production system would integrate this layer with an enterprise identity provider such as SSO/OAuth.



\---



\# 📄 Knowledge Base



The demo knowledge base contains enterprise-style PDF documents covering multiple departments.



| Document Category | Department |

|---|---|

| Microservices Architecture Specification | Engineering |

| Severity 1 Incident Escalation SOP | Delivery Operations |

| Agile Execution Framework Guide | PMO |

| Global Leave Policy 2026 | Human Resources |

| Cloud Transformation Capability Deck | Sales |



The PDFs are included in the repository under the `data/` directory.



\---



\# 🧠 Grounding \& Hallucination Control



One of the main design goals is to prevent the LLM from answering using unsupported external knowledge.



The system uses a strict grounding prompt:



```text

Answer using ONLY the verified context provided.



Do NOT use external memory,

general internet knowledge,

or assumptions.



If the retrieved context does not contain

the required information, return an

insufficient-context response.

```



\### Example



Query:



```text

Who is the CEO of Infosys?

```



If the retrieved enterprise documents do not contain that information, the system does not attempt to answer from general model knowledge.



Instead, it returns an insufficient-context response.



\---



\# 📚 Citation System



Every retrieved document chunk contains metadata identifying:



```text

Document

Page Number

Department

Matched Passage

```



The final response displays the source document and page number in the Streamlit citation panel.



Example:



```text

Citation:

Infosys\_Microservices\_Architecture\_Spec.pdf

Page: 1

Department: Engineering

```



This makes the generated response easier to verify against the original source document.



\---



\# 🛠️ Technology Stack



\### AI / RAG



\- Google Gemini

\- LangChain

\- Retrieval-Augmented Generation

\- Google Generative AI Embeddings



\### Vector Database



\- ChromaDB



\### Document Processing



\- PyMuPDF

\- Recursive Character Text Splitter



\### Backend / Application



\- Python

\- Streamlit



\### Data \& Validation



\- Pydantic

\- Python-dotenv



\### Deployment



\- Streamlit Community Cloud

\- GitHub



\---



\# 📁 Project Structure



```text

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

│   │   └── citation\_formatter.py

│   │

│   ├── grounded\_synthesis/

│   │   └── synthesis\_engine.py

│   │

│   ├── query\_classification/

│   │   └── rbac\_classifier.py

│   │

│   └── rag\_retrieval/

│       └── hybrid\_search.py

│

├── ingestion\_pipeline/

│   └── embedding\_jobs/

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

```



> `vector\_db/` is generated locally/deployed at runtime and is intentionally excluded from Git because the application can rebuild the knowledge base from the PDF documents when required.



\---



\# ⚙️ Local Setup



\## 1. Clone the repository



```bash

git clone https://github.com/PAWAN0207/infosys-ai-knowledge-assistant.git

cd infosys-ai-knowledge-assistant

```



\## 2. Create a virtual environment



Using Conda:



```bash

conda create -n infosys-rag python=3.12

conda activate infosys-rag

```



\## 3. Install dependencies



```bash

pip install -r requirements.txt

```



\## 4. Configure Gemini API Key



Create a `.env` file in the project root:



```text

GOOGLE\_API\_KEY=your\_gemini\_api\_key\_here

```



> Never commit your `.env` file or API keys to GitHub.



\## 5. Build the vector database



```bash

python ingestion\_pipeline/embedding\_jobs/vector\_indexer.py

```



This processes the PDFs inside `data/`, generates embeddings, and stores them in ChromaDB.



\## 6. Run the Streamlit application



```bash

python -m streamlit run app.py

```



The application will be available locally at:



```text

http://localhost:8501

```



\---



\# ☁️ Deployment



The application is deployed using \*\*Streamlit Community Cloud\*\*.



\### Deployment configuration



```text

Repository:

PAWAN0207/infosys-ai-knowledge-assistant



Branch:

main



Main file:

app.py



Python:

3.12

```



The Gemini API key is configured through Streamlit Secrets rather than being stored in the GitHub repository.



```toml

GOOGLE\_API\_KEY = "your\_gemini\_api\_key"

```



\### Automatic knowledge-base creation



When deployed, the application checks whether ChromaDB already contains documents.



If the vector database is unavailable or empty:



```text

PDF files

&#x20;  ↓

PDF parsing

&#x20;  ↓

Chunking

&#x20;  ↓

Gemini embeddings

&#x20;  ↓

ChromaDB

```



The application then uses the generated vector database for retrieval.



\---



\# 🧪 Example Test Cases



\## Test 1 — Engineering Access



\*\*Designation:\*\*



```text

Software Engineer

```



\*\*Query:\*\*



```text

What are the key principles of the Infosys microservices architecture?

```



Expected behavior:



```text

Grounded Answer

Confidence Score

Source Citation

Document Page

Matched Passage

```



\---



\## Test 2 — RBAC Restriction



\*\*Designation:\*\*



```text

HR Associate

```



\*\*Query:\*\*



```text

What are the key principles of the Infosys microservices architecture?

```



Expected behavior:



```text

Access Denied /

Insufficient domain context available

for your role clearance.

```



The Engineering document should not be returned to the HR user.



\---



\## Test 3 — Out-of-Domain Query



\*\*Query:\*\*



```text

How are you?

```



Expected behavior:



```text

Insufficient domain context

```



The system should not generate an unrelated conversational answer because the application is designed as a grounded enterprise knowledge assistant.



\---



\# 🎯 Key Features



\- ✅ Enterprise-style RAG architecture

\- ✅ Semantic document retrieval

\- ✅ Gemini-powered response generation

\- ✅ ChromaDB vector search

\- ✅ Role-based department filtering

\- ✅ Source and page-level citations

\- ✅ Grounded response generation

\- ✅ Zero-extrapolation guardrails

\- ✅ Confidence scoring

\- ✅ Recommended actions

\- ✅ Automatic cloud knowledge-base initialization

\- ✅ Streamlit web interface

\- ✅ GitHub + Streamlit Cloud deployment



\---



\# 💡 Why RAG Instead of Fine-Tuning?



Fine-tuning is not ideal for frequently changing enterprise documents.



With RAG:



```text

New / Updated PDF

&#x20;      ↓

Re-index documents

&#x20;      ↓

Updated vectors

&#x20;      ↓

New information becomes retrievable

```



The underlying LLM does not need to be retrained every time an enterprise policy changes.



RAG therefore provides a more practical architecture for document-heavy enterprise knowledge systems.



\---



\# 🚀 Future Improvements



Potential production-level improvements include:



\- Enterprise SSO authentication

\- OAuth / OpenID Connect integration

\- User identity from corporate directory

\- Hosted vector database

\- Hybrid keyword + semantic retrieval

\- Re-ranking models

\- Document version management

\- Automated document ingestion

\- Audit logging

\- Retrieval evaluation metrics

\- LLM observability

\- Role-based admin dashboard

\- Automated CI/CD pipeline

\- Production-grade secrets management



\---



\# 👨‍💻 Author



\*\*Pawan Ajay Prasad\*\*



Data Analyst | Junior Data Scientist | ML \& GenAI



\### Profiles



\- GitHub: https://github.com/PAWAN0207

\- LinkedIn: https://www.linkedin.com/in/pawan-prasad-analyst/



\---



\## 🚀 Live Application



\### \[Launch Infosys AI Knowledge Assistant](https://infosys-ai-knowledge-assistant-qsjefhbgq7np44rb9v597g.streamlit.app/)



Built with Python, LangChain, Google Gemini, ChromaDB, and Streamlit.

