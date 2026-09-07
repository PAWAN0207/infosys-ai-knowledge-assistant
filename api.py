import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

from ai_workflows.citation_builder.citation_formatter import (
    GroundedResponseSchema,
)
from ai_workflows.grounded_synthesis.synthesis_engine import (
    EnterpriseGroundedEngine,
)
from ingestion_pipeline.embedding_jobs.vector_indexer import (
    EnterprisePDFIndexer,
)

load_dotenv()

app = FastAPI(
    title="Infosys AI Knowledge Assistant API",
    description="Enterprise RAG API with RBAC, grounded responses, and citations.",
    version="1.0.0",
)

_engine = None


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Employee question",
    )
    designation: str = Field(
        default="Software Engineer",
        description="Employee designation",
    )


def initialize_knowledge_base() -> None:
    """Build the ChromaDB knowledge base when it does not exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vector_db_path = os.path.join(script_dir, "vector_db")

    chroma_db_file = os.path.join(vector_db_path, "chroma.sqlite3")

    if os.path.exists(chroma_db_file):
        return

    print("Vector database not found. Building knowledge base from PDFs...")

    indexer = EnterprisePDFIndexer()
    indexer.process_and_index()

    print("Knowledge base initialization completed.")


def get_engine() -> EnterpriseGroundedEngine:
    global _engine

    if _engine is None:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured.")

        initialize_knowledge_base()

        _engine = EnterpriseGroundedEngine(
            google_api_key=api_key,
        )

    return _engine


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {
        "status": "healthy",
        "service": "infosys-ai-knowledge-assistant-api",
    }


@app.post("/query", response_model=GroundedResponseSchema)
def query_knowledge_base(data: QueryRequest) -> Any:
    engine = get_engine()

    return engine.generate_response(
        query=data.query,
        designation=data.designation,
    )
