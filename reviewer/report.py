import json
from pathlib import Path
import textwrap

def get_grade(score: int) -> str:
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Fair"
    else:
        return "Needs Improvement"

def export_json_report(result: dict, output_path: str) -> None:
    """
    Export analysis result to a JSON file.
    """

    path = Path(output_path)

    serializable_result = dict(result)

    issues = serializable_result.get("issues", [])
    serializable_result["issues"] = [
        issue.to_dict() if hasattr(issue, "to_dict") else issue
        for issue in issues
    ]

    with path.open("w", encoding="utf-8") as f:
        json.dump(serializable_result, f, indent=1)

    print(f"\nJSON report saved to: {path.resolve()}")


def print_report(result: dict) -> None:
    summary = result.get("summary", {})
    issues = result.get("issues", [])
    score_info = result.get("score", {})

    score = score_info.get("score", 0)
    grade = get_grade(score)

    if score >= 85:
        assessment = "Looks Good"
    elif score >= 70:
        assessment = "Needs Improvement"
    else:
        assessment = "Needs Major Fixes"

    def wrap(text, width=70):
        if not text:
            return ""
        return textwrap.fill(str(text), width=width)

    def get_field(issue, field, default=None):
        if isinstance(issue, dict):
            value = issue.get(field, default)
        else:
            value = getattr(issue, field, default)
        return value if value not in (None, "") else default

    print("\n" + "=" * 70)
    print("AI CODE REVIEW REPORT")
    print("=" * 70)

    print("\nOVERALL ASSESSMENT")
    print(f"Status : {assessment}")
    print(f"Grade  : {grade}")
    print(f"Score  : {score} / 100")

    if not issues:
        print("\nNo major issues detected.")
        print("\nMETRICS")
        for k, v in summary.items():
            print(f"- {k}: {v}")

        print("\nFINAL RECOMMENDATION")
        print(wrap("No major changes required. Consider adding tests and docstrings."))
        print("\n" + "=" * 70)
        return

    print("\nDETECTED ISSUES")

    for idx, issue in enumerate(issues, start=1):
        rule_id = get_field(issue, "rule_id", "ISSUE")
        severity = get_field(issue, "severity", "INFO")
        category = get_field(issue, "category", "other")
        function_name = get_field(issue, "function_name", "unknown")
        line_start = get_field(issue, "line_start", "Unknown")
        line_end = get_field(issue, "line_end", "Unknown")
        desc = get_field(issue, "description", "No description available.")
        explanation = get_field(issue, "explanation", "")
        suggestion = get_field(issue, "suggestion", "No suggestion available.")
        better_approach = get_field(issue, "better_approach", "")
        expected_improvement = get_field(issue, "expected_improvement", "")

        print("\n" + "-" * 70)
        print(f"Issue #{idx}")
        print(f"Rule ID    : {rule_id}")
        print(f"Category   : {category}")
        print(f"Severity   : {severity}")
        print(f"Function   : {function_name}")
        print(f"Lines      : {line_start}-{line_end}")

        print("\nRule-Based Finding")
        print(wrap(desc))

        if explanation:
            print("\nAI Explanation")
            print(wrap(explanation))

        print("\nSuggestion")
        print(wrap(suggestion))

        if better_approach:
            print("\nSuggested Better Approach")
            print(wrap(better_approach))

        if expected_improvement:
            print("\nExpected Improvement")
            print(wrap(expected_improvement))

    print("\n" + "-" * 70)
    print("\nMETRICS")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    print("\nFINAL RECOMMENDATION")
    if score >= 85:
        print(wrap(
            "The code quality is good overall. Resolve the minor issues and "
            "maintain consistent style."
        ))
    elif score >= 70:
        print(wrap(
            "Fix the detected issues, especially performance and bug-risk "
            "findings, before moving ahead."
        ))
    else:
        print(wrap(
            "Refactor the code and address the critical findings before "
            "considering production use."
        ))

    print("\n" + "=" * 70)