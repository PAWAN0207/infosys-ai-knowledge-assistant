import os
import requests
import streamlit as st

from ai_workflows.query_classification.rbac_classifier import (
    ROLE_PERMISSIONS
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Infosys AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL LAYOUT
   ===================================================== */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 1.5rem;
}

[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #151820;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}


/* =====================================================
   HEADINGS
   ===================================================== */

h1 {
    font-size: 2.35rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.8px;
}

h2,
h3 {
    font-weight: 650 !important;
}


/* =====================================================
   CAPTIONS
   ===================================================== */

[data-testid="stCaptionContainer"] {
    color: #8f96a3;
}


/* =====================================================
   BUTTONS
   ===================================================== */

div.stButton > button {
    min-height: 44px;
    border-radius: 8px;
    font-weight: 600;
}


/* =====================================================
   TEXT AREA
   ===================================================== */

textarea {
    border-radius: 9px !important;
}


/* =====================================================
   METRICS
   ===================================================== */

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 0.8rem;
}


/* =====================================================
   EXPANDERS
   ===================================================== */

[data-testid="stExpander"] {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 9px;
}


/* =====================================================
   CONTAINERS
   ===================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 10px;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {
    border-color: rgba(255, 255, 255, 0.10);
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer-text {
    text-align: center;
    color: #7f8793;
    font-size: 0.78rem;
    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# API CONFIGURATION
# =========================================================

RAG_API_URL = os.getenv(
    "RAG_API_URL",
    "https://infosys-ai-knowledge-assistant-4ovi.onrender.com"
).rstrip("/")


# =========================================================
# SESSION STATE
# =========================================================

if "response" not in st.session_state:
    st.session_state.response = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# =========================================================
# BACKEND HEALTH CHECK
# =========================================================

@st.cache_data(ttl=30)
def check_backend_health():
    """Check whether the Render FastAPI backend is available."""

    try:
        response = requests.get(
            f"{RAG_API_URL}/health",
            timeout=15
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


# =========================================================
# HEADER
# =========================================================

st.title("🤖 Infosys AI Knowledge Assistant")

st.caption(
    "Enterprise RAG platform for secure knowledge discovery, "
    "role-aware retrieval, grounded responses, and source citations."
)

st.divider()


# =========================================================
# SIDEBAR — EMPLOYEE SESSION
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # Employee Session
    # -----------------------------------------------------

    st.subheader("👤 Employee Session")

    designation_list = list(
        ROLE_PERMISSIONS.keys()
    )

    user_designation = st.selectbox(
        "Employee Designation",
        options=designation_list,
        index=0
    )

    allowed_departments = ROLE_PERMISSIONS.get(
        user_designation,
        []
    )

    st.divider()


    # -----------------------------------------------------
    # System Status
    # -----------------------------------------------------

    st.subheader("⚙️ System Status")

    backend_online = check_backend_health()

    with st.container(border=True):

        st.caption("FASTAPI BACKEND")

        if backend_online:
            st.markdown("🟢 **Connected**")
        else:
            st.markdown("🔴 **Unavailable**")


    with st.container(border=True):

        st.caption("RAG ENGINE")

        if backend_online:
            st.markdown("🟢 **Running on Render**")
        else:
            st.markdown("🔴 **Unavailable**")


    st.divider()


    # -----------------------------------------------------
    # Access Clearance
    # -----------------------------------------------------

    st.subheader("🔐 Access Clearance")

    if allowed_departments:

        for department in allowed_departments:

            with st.container(border=True):
                st.markdown(
                    f"✅ **{department}**"
                )

    else:

        st.warning(
            "No department access assigned."
        )


    st.divider()

    st.caption(
        "Role-based access is enforced at the retrieval layer."
    )


# =========================================================
# MAIN WORKSPACE
# =========================================================

query_col, source_col = st.columns(
    [1.15, 0.85],
    gap="large"
)


# =========================================================
# QUERY WORKSPACE
# =========================================================

with query_col:

    st.subheader("💬 Employee Query Workspace")

    st.caption(
        "Ask questions across authorized SOPs, policies, "
        "technical guides, and enterprise manuals."
    )

    user_query = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: What is the response SLA for "
            "Severity 1 incidents?"
        ),
        height=120,
        label_visibility="collapsed"
    )

    submit_btn = st.button(
        "🔎 Submit Query",
        type="primary",
        use_container_width=True
    )


    # =====================================================
    # QUERY PROCESSING
    # =====================================================

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
                "Searching authorized knowledge and generating grounded response..."
            ):

                try:

                    api_response = requests.post(
                        f"{RAG_API_URL}/query",
                        json=request_payload,
                        timeout=180
                    )

                    if api_response.status_code == 200:

                        st.session_state.response = (
                            api_response.json()
                        )

                        st.session_state.last_query = (
                            user_query.strip()
                        )

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

                except requests.RequestException:

                    st.error(
                        "Unable to connect to the FastAPI backend. "
                        "Please try again."
                    )


    # =====================================================
    # GROUNDED ANSWER
    # =====================================================

    response = st.session_state.response

    if response:

        st.divider()

        st.subheader("💡 Grounded Answer")

        if st.session_state.last_query:

            st.caption(
                f"Query: {st.session_state.last_query}"
            )

        answer = response.get(
            "answer",
            "No answer generated."
        )

        with st.container(border=True):

            st.markdown(answer)

        st.markdown("")


        # -------------------------------------------------
        # Response Metrics
        # -------------------------------------------------

        confidence = response.get(
            "confidence_score",
            0.0
        )

        citations = response.get(
            "citations",
            []
        )

        metric1, metric2 = st.columns(2)

        with metric1:

            st.metric(
                label="Confidence Score",
                value=str(confidence)
            )

        with metric2:

            st.metric(
                label="Sources Retrieved",
                value=len(citations)
            )


        # -------------------------------------------------
        # Recommended Action
        # -------------------------------------------------

        recommended_action = response.get(
            "recommended_action",
            "No recommendation available."
        )

        st.info(
            f"**Recommended Action:** {recommended_action}"
        )


# =========================================================
# CITATION & SOURCE PANEL
# =========================================================

with source_col:

    st.subheader("📌 Citation & Source Panel")

    st.caption(
        "Retrieved enterprise context used to support "
        "the generated response."
    )

    response = st.session_state.response

    if not response:

        st.info(
            "Submit a query to view supporting sources "
            "and citations."
        )

    else:

        citations = response.get(
            "citations",
            []
        )

        if not citations:

            st.warning(
                "No explicit citation sources were returned."
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
                    f"Source {idx} • "
                    f"{document_name} • "
                    f"Page {page_number}"
                ):

                    st.caption(
                        "Department"
                    )

                    st.write(
                        department
                    )

                    st.markdown(
                        "**Matched Passage**"
                    )

                    st.markdown(
                        f'> "{matched_passage}"'
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Infosys AI Knowledge Assistant"
)

st.caption(
    "RAG v1.0 • Streamlit + FastAPI • Enterprise RAG Demonstration"
)