import os
import requests
import streamlit as st

from ai_workflows.query_classification.rbac_classifier import (
    ROLE_PERMISSIONS
)


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
# Render FastAPI Configuration
# ---------------------------------------------------------

RAG_API_URL = os.getenv(
    "RAG_API_URL",
    "https://infosys-ai-knowledge-assistant-4ovi.onrender.com"
).rstrip("/")


# ---------------------------------------------------------
# Backend Health Check
# ---------------------------------------------------------

def check_backend_health():
    """Check whether the Render FastAPI backend is available."""
    try:
        response = requests.get(
            f"{RAG_API_URL}/health",
            timeout=15
        )

        if response.status_code == 200:
            return True

    except requests.RequestException:
        pass

    return False


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

    if check_backend_health():

        st.success(
            "FastAPI Backend: Connected"
        )

        st.info(
            "RAG Engine: Running on Render"
        )

    else:

        st.error(
            "FastAPI Backend: Unavailable"
        )

    # Show current user's allowed departments

    allowed_departments = ROLE_PERMISSIONS.get(
        user_designation,
        []
    )

    st.markdown("---")

    st.subheader("🔐 Access Clearance")

    for department in allowed_departments:

        st.write(
            f"✅ {department}"
        )


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

    response = None

    if submit_btn:

        if not user_query.strip():

            st.warning(
                "Please enter a valid question."
            )

        else:

            request_payload = {
                "query": user_query.strip(),
                "designation": user_designation
            }

            with st.spinner(
                f"Querying RAG backend for "
                f"'{user_designation}'..."
            ):

                try:

                    api_response = requests.post(
                        f"{RAG_API_URL}/query",
                        json=request_payload,
                        timeout=180
                    )

                    if api_response.status_code == 200:

                        response = api_response.json()

                    elif api_response.status_code == 422:

                        st.error(
                            "Invalid query request. "
                            "Please check your input."
                        )

                    else:

                        st.error(
                            f"Backend returned HTTP "
                            f"{api_response.status_code}."
                        )

                except requests.Timeout:

                    st.error(
                        "The backend request timed out. "
                        "The Render service may be starting up "
                        "or building the knowledge base."
                    )

                except requests.RequestException as exc:

                    st.error(
                        f"Unable to connect to the FastAPI backend: "
                        f"{exc}"
                    )


        # -------------------------------------------------
        # Grounded Answer
        # -------------------------------------------------

        if response:

            st.markdown(
                "### 💡 Grounded Answer"
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

    if response:

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
                        f'> *"{matched_passage}"*'
                    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Infosys AI Knowledge Assistant | "
    "Streamlit + FastAPI + RAG v1.0"
)

st.caption(
    "Infosys AI Knowledge Assistant | "
    "Streamlit + FastAPI + RAG v1.0"
)