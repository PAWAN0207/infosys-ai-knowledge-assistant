import json
import os
import sys
import time
from typing import Any, Dict, List

from dotenv import load_dotenv

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_workflows.grounded_synthesis.synthesis_engine import (
    EnterpriseGroundedEngine,
)


DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "generation_evaluation_dataset.json",
)


def load_dataset() -> List[Dict[str, Any]]:
    """Load generation evaluation cases."""
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(
    engine: EnterpriseGroundedEngine,
    case: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate one controlled generation case."""

    start_time = time.perf_counter()

    response = engine.generate_response(
        query=case["question"],
        designation=case["designation"],
    )

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    answer = str(
        response.get("answer", "")
    )

    citations = response.get(
        "citations",
        [],
    )

    confidence = response.get(
        "confidence_score",
        None,
    )

    expected_behavior = case.get(
        "expected_behavior",
        "allow",
    )

    expected_keywords = [
        keyword.lower()
        for keyword in case.get(
            "expected_keywords",
            [],
        )
    ]

    answer_lower = answer.lower()

    keyword_matches = [
        keyword
        for keyword in expected_keywords
        if keyword in answer_lower
    ]

    keyword_coverage = (
        len(keyword_matches)
        / len(expected_keywords)
        if expected_keywords
        else 0.0
    )

    expected_document = case.get(
        "expected_document",
        "",
    )

    citation_text = json.dumps(
        citations,
        ensure_ascii=False,
    ).lower()

    expected_document_cited = (
        expected_document.lower()
        in citation_text
    )

    citation_present = len(citations) > 0

    if expected_behavior == "deny":

        # For an unauthorized query, the expected
        # behavior is to deny access rather than
        # generate restricted information.
        deny_indicators = [
            "access denied",
            "insufficient",
            "not authorized",
            "unauthorized",
            "permission",
            "restricted",
        ]

        denial_detected = any(
            indicator in answer_lower
            for indicator in deny_indicators
        )

        restricted_document_not_cited = (
            not expected_document_cited
        )

        passed = (
            denial_detected
            and restricted_document_not_cited
        )

        return {
            "id": case["id"],
            "type": "RBAC",
            "passed": passed,
            "answer": answer,
            "citations": citations,
            "confidence": confidence,
            "keyword_coverage": keyword_coverage,
            "citation_present": citation_present,
            "expected_document_cited": (
                expected_document_cited
            ),
            "denial_detected": denial_detected,
            "latency_ms": latency_ms,
        }

    # Authorized generation case

    passed = (
        keyword_coverage == 1.0
        and citation_present
        and expected_document_cited
    )

    return {
        "id": case["id"],
        "type": "RAG",
        "passed": passed,
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "keyword_coverage": keyword_coverage,
        "citation_present": citation_present,
        "expected_document_cited": (
            expected_document_cited
        ),
        "denial_detected": False,
        "latency_ms": latency_ms,
    }


def print_case_result(
    index: int,
    total: int,
    case: Dict[str, Any],
    result: Dict[str, Any],
) -> None:
    """Print evaluation result."""

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
        f"Keyword Coverage: "
        f"{result['keyword_coverage']:.2%}"
    )

    print(
        f"Citation Present: "
        f"{result['citation_present']}"
    )

    print(
        f"Expected Document Cited: "
        f"{result['expected_document_cited']}"
    )

    if result["type"] == "RBAC":
        print(
            f"Denial Detected: "
            f"{result['denial_detected']}"
        )

    print(
        f"Confidence: "
        f"{result['confidence']}"
    )

    print(
        f"Latency: "
        f"{result['latency_ms']:.2f} ms"
    )

    print(
        f"Answer: "
        f"{result['answer']}"
    )


def main() -> None:
    """Run controlled generation evaluation."""

    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    dataset = load_dataset()

    print("=" * 70)
    print(
        "INFOSYS AI KNOWLEDGE ASSISTANT "
        "- GENERATION EVALUATION"
    )
    print("=" * 70)

    print(
        f"Evaluation cases: "
        f"{len(dataset)}"
    )

    print(
        "\nWARNING: This evaluation makes "
        f"{len(dataset)} Gemini generation calls."
    )

    engine = EnterpriseGroundedEngine()

    results = []

    for index, case in enumerate(
        dataset,
        start=1,
    ):
        result = evaluate_case(
            engine,
            case,
        )

        results.append(result)

        print_case_result(
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

    generation_pass_rate = (
        sum(
            1
            for result in rag_results
            if result["passed"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    keyword_coverage = (
        sum(
            result["keyword_coverage"]
            for result in rag_results
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    citation_rate = (
        sum(
            1
            for result in rag_results
            if result["citation_present"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    expected_document_citation_rate = (
        sum(
            1
            for result in rag_results
            if result[
                "expected_document_cited"
            ]
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

    average_latency = (
        sum(
            result["latency_ms"]
            for result in results
        )
        / total
        if total
        else 0.0
    )

    print("\n" + "=" * 70)
    print(
        "GENERATION EVALUATION SUMMARY"
    )
    print("=" * 70)

    print(
        f"Overall Pass Rate: "
        f"{passed / total:.2%}"
    )

    print(
        f"Authorized Generation Pass Rate: "
        f"{generation_pass_rate:.2%}"
    )

    print(
        f"Expected Keyword Coverage: "
        f"{keyword_coverage:.2%}"
    )

    print(
        f"Citation Presence Rate: "
        f"{citation_rate:.2%}"
    )

    print(
        f"Expected Document Citation Rate: "
        f"{expected_document_citation_rate:.2%}"
    )

    print(
        f"RBAC Generation Pass Rate: "
        f"{rbac_pass_rate:.2%}"
    )

    print(
        f"Average Generation Latency: "
        f"{average_latency:.2f} ms"
    )

    print(
        f"Passed: "
        f"{passed}/{total}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()