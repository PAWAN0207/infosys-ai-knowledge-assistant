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
    "grounding_evaluation_dataset.json",
)


def load_dataset() -> List[Dict[str, Any]]:
    """Load grounding evaluation cases."""
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_fact_coverage(
    answer: str,
    expected_facts: List[str],
) -> Dict[str, Any]:
    """Check whether expected facts are present in the answer."""

    if not expected_facts:
        return {
            "coverage": 0.0,
            "matched_facts": [],
            "missing_facts": [],
        }

    answer_lower = answer.lower()

    matched_facts = []
    missing_facts = []

    for fact in expected_facts:
        if fact.lower() in answer_lower:
            matched_facts.append(fact)
        else:
            missing_facts.append(fact)

    coverage = (
        len(matched_facts) / len(expected_facts)
    )

    return {
        "coverage": coverage,
        "matched_facts": matched_facts,
        "missing_facts": missing_facts,
    }


def check_citations(
    response: Dict[str, Any],
    expected_document: str,
) -> Dict[str, Any]:
    """Validate citation presence and expected document."""

    citations = response.get("citations", [])

    citation_present = bool(citations)

    expected_document_cited = False

    for citation in citations:
        citation_text = str(citation)

        if expected_document.lower() in citation_text.lower():
            expected_document_cited = True
            break

    return {
        "citation_present": citation_present,
        "expected_document_cited": expected_document_cited,
    }


def check_rbac_denial(
    response: Dict[str, Any],
) -> bool:
    """Check whether the response correctly denied access."""

    answer = str(
        response.get("answer", "")
    ).lower()

    denial_indicators = [
        "access denied",
        "insufficient domain context",
        "role clearance",
        "not authorized",
        "unauthorized",
        "do not have access",
    ]

    return any(
        indicator in answer
        for indicator in denial_indicators
    )


def evaluate_case(
    engine: EnterpriseGroundedEngine,
    case: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate one grounding case."""

    start_time = time.perf_counter()

    question = case["question"]
    designation = case["designation"]

    expected_facts = case.get(
        "expected_supported_facts",
        [],
    )

    expected_behavior = case.get(
        "expected_behavior",
        "allow",
    )

    expected_document = case.get(
        "expected_document",
        "",
    )

    try:
        response = engine.generate_response(
            query=question,
            designation=designation,
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        answer = str(
            response.get("answer", "")
        )

        # -----------------------------------------------------
        # RBAC DENY CASE
        # -----------------------------------------------------
        if expected_behavior == "deny":

            denial_detected = check_rbac_denial(
                response
            )

            citations = response.get(
                "citations",
                [],
            )

            passed = (
                denial_detected
                and not citations
            )

            return {
                "id": case["id"],
                "type": "RBAC",
                "passed": passed,
                "fact_coverage": 0.0,
                "citation_present": bool(citations),
                "expected_document_cited": False,
                "denial_detected": denial_detected,
                "confidence": response.get(
                    "confidence_score",
                    0.0,
                ),
                "latency_ms": latency_ms,
                "answer": answer,
            }

        # -----------------------------------------------------
        # NORMAL GROUNDING CASE
        # -----------------------------------------------------
        fact_result = check_fact_coverage(
            answer,
            expected_facts,
        )

        citation_result = check_citations(
            response,
            expected_document,
        )

        confidence = response.get(
            "confidence_score",
            0.0,
        )

        passed = (
            fact_result["coverage"] == 1.0
            and citation_result["citation_present"]
            and citation_result[
                "expected_document_cited"
            ]
        )

        return {
            "id": case["id"],
            "type": "RAG",
            "passed": passed,
            "fact_coverage": fact_result[
                "coverage"
            ],
            "matched_facts": fact_result[
                "matched_facts"
            ],
            "missing_facts": fact_result[
                "missing_facts"
            ],
            "citation_present": citation_result[
                "citation_present"
            ],
            "expected_document_cited": citation_result[
                "expected_document_cited"
            ],
            "denial_detected": False,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "answer": answer,
        }

    except Exception as exc:
        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "id": case["id"],
            "type": (
                "RBAC"
                if expected_behavior == "deny"
                else "RAG"
            ),
            "passed": False,
            "fact_coverage": 0.0,
            "matched_facts": [],
            "missing_facts": expected_facts,
            "citation_present": False,
            "expected_document_cited": False,
            "denial_detected": False,
            "confidence": 0.0,
            "latency_ms": latency_ms,
            "answer": f"ERROR: {exc}",
        }


def print_result(
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
        f"Fact Coverage: "
        f"{result['fact_coverage']:.2%}"
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

    if result.get("missing_facts"):
        print("Missing Facts:")

        for fact in result["missing_facts"]:
            print(f"  - {fact}")


def main() -> None:
    """Run grounding evaluation."""

    load_dotenv()

    dataset = load_dataset()

    print("=" * 70)
    print(
        "INFOSYS AI KNOWLEDGE ASSISTANT "
        "- GROUNDING EVALUATION"
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

    overall_pass_rate = (
        passed / total
        if total
        else 0.0
    )

    rag_pass_rate = (
        sum(
            1
            for result in rag_results
            if result["passed"]
        )
        / len(rag_results)
        if rag_results
        else 0.0
    )

    average_fact_coverage = (
        sum(
            result["fact_coverage"]
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

    document_citation_rate = (
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

    average_confidence = (
        sum(
            result["confidence"]
            for result in results
        )
        / total
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

    print("\n" + "=" * 70)
    print("GROUNDING EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Overall Pass Rate: "
        f"{overall_pass_rate:.2%}"
    )

    print(
        f"Authorized Grounding Pass Rate: "
        f"{rag_pass_rate:.2%}"
    )

    print(
        f"Expected Fact Coverage: "
        f"{average_fact_coverage:.2%}"
    )

    print(
        f"Citation Presence Rate: "
        f"{citation_rate:.2%}"
    )

    print(
        f"Expected Document Citation Rate: "
        f"{document_citation_rate:.2%}"
    )

    print(
        f"RBAC Grounding Pass Rate: "
        f"{rbac_pass_rate:.2%}"
    )

    print(
        f"Average Confidence: "
        f"{average_confidence:.2f}"
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