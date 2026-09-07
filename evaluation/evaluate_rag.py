import json
import os
import sys
import time
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_workflows.query_classification.rbac_classifier import (
    ROLE_PERMISSIONS,
)


DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "evaluation_dataset.json",
)

VECTOR_DB_PATH = os.path.join(
    PROJECT_ROOT,
    "vector_db",
)


def load_dataset() -> List[Dict[str, Any]]:
    """Load evaluation questions from JSON."""
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_allowed_departments(
    designation: str,
) -> List[str]:
    """Return departments allowed by the production RBAC matrix."""
    return ROLE_PERMISSIONS.get(
        designation,
        [],
    )


def build_vector_store() -> Chroma:
    """Connect to the existing ChromaDB vector store."""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=api_key,
    )

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
    )


def get_ranking_metrics(
    retrieved_documents: List[str],
    expected_document: str,
) -> Dict[str, Any]:
    """Calculate Hit@1, Hit@3, Hit@5 and reciprocal rank."""

    try:
        rank = retrieved_documents.index(
            expected_document
        ) + 1
    except ValueError:
        rank = None

    hit_at_1 = (
        rank is not None
        and rank <= 1
    )

    hit_at_3 = (
        rank is not None
        and rank <= 3
    )

    hit_at_5 = (
        rank is not None
        and rank <= 5
    )

    reciprocal_rank = (
        1 / rank
        if rank is not None
        else 0.0
    )

    return {
        "rank": rank,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hit_at_5": hit_at_5,
        "reciprocal_rank": reciprocal_rank,
    }


def evaluate_retrieval(
    vector_db: Chroma,
    case: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate retrieval without calling the LLM."""

    start_time = time.perf_counter()

    question = case["question"]
    designation = case["designation"]
    expected_document = case["expected_document"]
    expected_department = case["expected_department"]

    expected_behavior = case.get(
        "expected_behavior",
        "allow",
    )

    allowed_departments = get_allowed_departments(
        designation
    )

    # ---------------------------------------------------------
    # RBAC DENY / UNKNOWN ROLE
    # ---------------------------------------------------------
    # If the role has no authorized departments, do not query
    # Chroma with an empty $in filter.
    if not allowed_departments:

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # For a deny test, no retrieved document means access
        # was correctly restricted.
        if expected_behavior == "deny":
            return {
                "id": case["id"],
                "type": "RBAC",
                "passed": True,
                "document_hit": False,
                "department_hit": False,
                "rank": None,
                "hit_at_1": False,
                "hit_at_3": False,
                "hit_at_5": False,
                "reciprocal_rank": 0.0,
                "retrieved_documents": [],
                "retrieved_departments": [],
                "best_distance": None,
                "latency_ms": latency_ms,
            }

        # If the dataset expects access but the role has no
        # permissions, this is a genuine evaluation failure.
        return {
            "id": case["id"],
            "type": "RAG",
            "passed": False,
            "document_hit": False,
            "department_hit": False,
            "rank": None,
            "hit_at_1": False,
            "hit_at_3": False,
            "hit_at_5": False,
            "reciprocal_rank": 0.0,
            "retrieved_documents": [],
            "retrieved_departments": [],
            "best_distance": None,
            "latency_ms": latency_ms,
        }

    # ---------------------------------------------------------
    # AUTHORIZED RETRIEVAL
    # ---------------------------------------------------------
    results = vector_db.similarity_search_with_score(
        question,
        k=5,
        filter={
            "department": {
                "$in": allowed_departments
            }
        },
    )

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    retrieved_documents = [
        doc.metadata.get(
            "source_document",
            "",
        )
        for doc, _ in results
    ]

    retrieved_departments = [
        doc.metadata.get(
            "department",
            "",
        )
        for doc, _ in results
    ]

    distances = [
        float(score)
        for _, score in results
    ]

    best_distance = (
        min(distances)
        if distances
        else None
    )

    document_hit = (
        expected_document
        in retrieved_documents
    )

    department_hit = (
        expected_department
        in retrieved_departments
    )

    # ---------------------------------------------------------
    # RBAC DENY TEST
    # ---------------------------------------------------------
    if expected_behavior == "deny":

        # The restricted document must not appear
        # in the RBAC-filtered retrieval results.
        unauthorized_document_retrieved = (
            expected_document
            in retrieved_documents
        )

        passed = not unauthorized_document_retrieved

        return {
            "id": case["id"],
            "type": "RBAC",
            "passed": passed,
            "document_hit": document_hit,
            "department_hit": department_hit,
            "rank": None,
            "hit_at_1": False,
            "hit_at_3": False,
            "hit_at_5": False,
            "reciprocal_rank": 0.0,
            "retrieved_documents": retrieved_documents,
            "retrieved_departments": retrieved_departments,
            "best_distance": best_distance,
            "latency_ms": latency_ms,
        }

    # ---------------------------------------------------------
    # NORMAL RAG EVALUATION
    # ---------------------------------------------------------
    ranking = get_ranking_metrics(
        retrieved_documents,
        expected_document,
    )

    passed = (
        document_hit
        and department_hit
    )

    return {
        "id": case["id"],
        "type": "RAG",
        "passed": passed,
        "document_hit": document_hit,
        "department_hit": department_hit,
        "rank": ranking["rank"],
        "hit_at_1": ranking["hit_at_1"],
        "hit_at_3": ranking["hit_at_3"],
        "hit_at_5": ranking["hit_at_5"],
        "reciprocal_rank": ranking[
            "reciprocal_rank"
        ],
        "retrieved_documents": retrieved_documents,
        "retrieved_departments": retrieved_departments,
        "best_distance": best_distance,
        "latency_ms": latency_ms,
    }


def print_result(
    index: int,
    total: int,
    case: Dict[str, Any],
    result: Dict[str, Any],
) -> None:
    """Print one evaluation result."""

    status = (
        "PASS"
        if result["passed"]
        else "FAIL"
    )

    print(
        f"\n[{index}/{total}] "
        f"{case['id']} - "
        f"{case['question']}"
    )

    print(
        f"Result: {status}"
    )

    print(
        f"Type: {result['type']}"
    )

    print(
        f"Expected Document: "
        f"{case['expected_document']}"
    )

    if result["type"] == "RAG":

        print(
            f"Correct Document Rank: "
            f"{result['rank']}"
        )

        print(
            f"Hit@1: "
            f"{result['hit_at_1']}"
        )

        print(
            f"Hit@3: "
            f"{result['hit_at_3']}"
        )

        print(
            f"Hit@5: "
            f"{result['hit_at_5']}"
        )

    else:

        print(
            "Unauthorized Document Retrieved: "
            f"{result['document_hit']}"
        )

    print(
        f"Department Match: "
        f"{result['department_hit']}"
    )

    print(
        f"Best Chroma Distance: "
        f"{result['best_distance']}"
    )

    print(
        f"Retrieval Latency: "
        f"{result['latency_ms']:.2f} ms"
    )


def main() -> None:
    """Run retrieval and RBAC evaluation."""

    load_dotenv()

    dataset = load_dataset()

    print("=" * 70)
    print(
        "INFOSYS AI KNOWLEDGE ASSISTANT "
        "- RETRIEVAL EVALUATION"
    )
    print("=" * 70)

    print(
        f"Evaluation cases: "
        f"{len(dataset)}"
    )

    chroma_file = os.path.join(
        VECTOR_DB_PATH,
        "chroma.sqlite3",
    )

    if not os.path.exists(chroma_file):
        raise RuntimeError(
            "ChromaDB was not found at "
            f"'{VECTOR_DB_PATH}'. "
            "Run the indexing pipeline first."
        )

    print(
        "\nConnecting to existing ChromaDB..."
    )

    vector_db = build_vector_store()

    results = []

    for index, case in enumerate(
        dataset,
        start=1,
    ):

        result = evaluate_retrieval(
            vector_db,
            case,
        )

        results.append(result)

        print_result(
            index,
            len(dataset),
            case,
            result,
        )

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    rag_results = [
        result
        for result in results
        if result["type"] == "RAG"
    ]

    rbac_results = [
        result
        for result in results
        if result["type"] == "RBAC"
    ]

    hit_at_1 = (
        sum(
            1
            for result in rag_results
            if result["hit_at_1"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    hit_at_3 = (
        sum(
            1
            for result in rag_results
            if result["hit_at_3"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    hit_at_5 = (
        sum(
            1
            for result in rag_results
            if result["hit_at_5"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    mean_reciprocal_rank = (
        sum(
            result["reciprocal_rank"]
            for result in rag_results
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    department_match_rate = (
        sum(
            1
            for result in rag_results
            if result["department_hit"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    rbac_pass_rate = (
        sum(
            1
            for result in rbac_results
            if result["passed"]
        )
        / len(rbac_results)
        if rbac_results
        else 0.0
    )

    overall_pass_rate = (
        passed / total
        if total
        else 0.0
    )

    average_latency = (
        sum(
            result["latency_ms"]
            for result in results
        )
        / total
        if total
        else 0.0
    )

    distances = [
        result["best_distance"]
        for result in results
        if result["best_distance"] is not None
    ]

    average_best_distance = (
        sum(distances) / len(distances)
        if distances
        else 0.0
    )

    print("\n" + "=" * 70)
    print("RETRIEVAL RANKING EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Overall Pass Rate: "
        f"{overall_pass_rate:.2%}"
    )

    print(
        f"Hit@1: "
        f"{hit_at_1:.2%}"
    )

    print(
        f"Hit@3: "
        f"{hit_at_3:.2%}"
    )

    print(
        f"Hit@5: "
        f"{hit_at_5:.2%}"
    )

    print(
        f"Mean Reciprocal Rank (MRR): "
        f"{mean_reciprocal_rank:.4f}"
    )

    print(
        f"Department Match Rate: "
        f"{department_match_rate:.2%}"
    )

    print(
        f"RBAC Pass Rate: "
        f"{rbac_pass_rate:.2%}"
    )

    print(
        f"Average Retrieval Latency: "
        f"{average_latency:.2f} ms"
    )

    print(
        f"Average Best Chroma Distance: "
        f"{average_best_distance:.4f}"
    )

    print(
        f"Passed: "
        f"{passed}/{total}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()