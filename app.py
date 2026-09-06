import os
import sys
import platform
import asyncio

# Fix for Windows asyncio ConnectionResetError
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
from dotenv import load_dotenv

from ai_workflows.grounded_synthesis.synthesis_engine import (
    EnterpriseGroundedEngine
)
from ai_workflows.query_classification.rbac_classifier import (
    ROLE_PERMISSIONS
)
from ingestion_pipeline.embedding_jobs.vector_indexer import (
    EnterprisePDFIndexer
)

# Load environment variables
load_dotenv()


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Infosys AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Infosys AI Knowledge Assistant")
st.caption(
    "Enterprise RAG platform for internal knowledge, "
    "citation-backed discovery, and secure role-based access."
)


# ---------------------------------------------------------
# Environment Configuration
# ---------------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error(
        "Google API key is not configured. "
        "Please add GOOGLE_API_KEY to your environment or Streamlit Secrets."
    )
    st.stop()


# ---------------------------------------------------------
# Vector Database Setup
# ---------------------------------------------------------

@st.cache_resource
def setup_vector_database():
    """
    Check whether ChromaDB exists and contains documents.

    If the database is missing or empty, automatically build it
    from the PDF documents available inside the data/ directory.
    """

    vector_db_path = os.path.join(
        PROJECT_ROOT,
        "vector_db"
    )

    data_path = os.path.join(
        PROJECT_ROOT,
        "data"
    )

    # -----------------------------------------------------
    # Check existing ChromaDB
    # -----------------------------------------------------

    try:
        from langchain_chroma import Chroma
        from langchain_google_genai import (
            GoogleGenerativeAIEmbeddings
        )

        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2-preview",
            google_api_key=GOOGLE_API_KEY
        )

        db = Chroma(
            persist_directory=vector_db_path,
            embedding_function=embeddings
        )

        document_count = db._collection.count()

        if document_count > 0:
            return vector_db_path

    except Exception:
        # If DB doesn't exist or cannot be opened,
        # create it below.
        pass

    # -----------------------------------------------------
    # Build Vector Database from PDFs
    # -----------------------------------------------------

    st.info(
        "🔄 First-time setup: Building the knowledge base "
        "from PDF documents..."
    )

    indexer = EnterprisePDFIndexer(
        data_root_path=data_path,
        vector_db_path=vector_db_path,
        google_api_key=GOOGLE_API_KEY
    )

    indexer.process_and_index()

    return vector_db_path


# ---------------------------------------------------------
# Initialize Vector Database
# ---------------------------------------------------------

try:

    vector_db_path = setup_vector_database()

except Exception as e:

    st.error(
        f"❌ Failed to initialize the knowledge base.\n\n"
        f"Error: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# Initialize Grounded RAG Engine
# ---------------------------------------------------------

@st.cache_resource
def load_engine(vector_db_path):

    return EnterpriseGroundedEngine(
        vector_db_path=vector_db_path,
        google_api_key=GOOGLE_API_KEY
    )


try:

    engine = load_engine(vector_db_path)

except Exception as e:

    st.error(
        f"❌ Failed to initialize the RAG engine.\n\n"
        f"Error: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# Sidebar - User Identity & RBAC
# ---------------------------------------------------------

with st.sidebar:

    st.header("👤 User Session Identity")

    designation_list = list(
        ROLE_PERMISSIONS.keys()
    )

    user_designation = st.selectbox(
        "Select Your Employee Designation:",
        options=designation_list,
        index=0
    )

    st.markdown("---")

    st.header("⚙️ System Status")

    st.success(
        "Vector DB: Persistent Chroma Connected"
    )

    st.info(
        "Grounding Model: Gemini 3.6 Flash (T=0.0)"
    )

    # Show current user's allowed departments
    allowed_departments = ROLE_PERMISSIONS.get(
        user_designation,
        []
    )

    st.markdown("---")

    st.subheader("🔐 Access Clearance")

    for department in allowed_departments:

        st.write(f"✅ {department}")


# ---------------------------------------------------------
# Main Query Workspace
# ---------------------------------------------------------

col1, col2 = st.columns(
    [1.2, 0.8]
)


# ---------------------------------------------------------
# Query Section
# ---------------------------------------------------------

with col1:

    st.subheader(
        "💬 Employee Query Workspace"
    )

    user_query = st.text_input(
        "Ask a question across SOPs, policies, guides, or manuals:",
        placeholder=(
            "e.g., What is the response SLA "
            "for Severity 1 incidents?"
        )
    )

    submit_btn = st.button(
        "Submit Query",
        type="primary",
        use_container_width=True
    )

    if submit_btn and user_query.strip():

        with st.spinner(
            f"Retrieving grounded context "
            f"for '{user_designation}'..."
        ):

            response = engine.generate_response(
                query=user_query,
                designation=user_designation
            )

        # ---------------------------------------------
        # Grounded Answer
        # ---------------------------------------------

        st.markdown(
            "### 📝 Grounded Answer"
        )

        st.write(
            response.get(
                "answer",
                "No answer generated."
            )
        )

        # ---------------------------------------------
        # Confidence Score
        # ---------------------------------------------

        confidence = response.get(
            "confidence_score",
            0.0
        )

        st.markdown(
            f"**Confidence Score:** `{confidence}`"
        )

        # ---------------------------------------------
        # Recommended Action
        # ---------------------------------------------

        st.info(
            "**Recommended Action:** "
            + str(
                response.get(
                    "recommended_action",
                    "No recommendation available."
                )
            )
        )


# ---------------------------------------------------------
# Citation & Source Panel
# ---------------------------------------------------------

with col2:

    st.subheader(
        "📌 Citation & Source Panel"
    )

    if submit_btn and user_query.strip():

        citations = response.get(
            "citations",
            []
        )

        if not citations:

            st.warning(
                "No explicit citation sources "
                "returned for this query."
            )

        else:

            for idx, cite in enumerate(
                citations,
                1
            ):

                document_name = cite.get(
                    "document_name",
                    "Unknown Document"
                )

                page_number = cite.get(
                    "page_number",
                    "N/A"
                )

                department = cite.get(
                    "department",
                    "Unknown"
                )

                matched_passage = cite.get(
                    "matched_passage",
                    "No passage available."
                )

                with st.expander(
                    f"[{idx}] {document_name} "
                    f"(Page {page_number})"
                ):

                    st.markdown(
                        f"**Department:** `{department}`"
                    )

                    st.markdown(
                        "**Matched Passage:**"
                    )

                    st.markdown(
                        f"> *\"{matched_passage}\"*"
                    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Infosys AI Knowledge Assistant | "
    "Enterprise RAG Platform v1.0"
)