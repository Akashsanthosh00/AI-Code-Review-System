import json
from pathlib import Path

from reviewer.analyzer import analyze_code
from reviewer.ml.ai_engine import enhance_with_ai

def issue_to_input_text(issue):
    parts = [
        f"rule_id: {issue.rule_id}",
        f"category: {issue.category}",
        f"severity: {issue.severity}",
        f"function_name: {issue.function_name}",
    ]

    for key, value in issue.metrics.items():
        parts.append(f"{key}: {value}")

    if issue.snippet:
        snippet = " ".join(issue.snippet.strip().split())
        parts.append(f"snippet: {snippet[:200]}")

    return " | ".join(parts)

def build_dataset_from_folder(source_folder, output_file):

    source_path = Path(source_folder)
    rows = []

    py_files = list(source_path.rglob("*.py"))

    for file_path in py_files:

        code = file_path.read_text(encoding="utf-8")

        result = analyze_code(code)
        result = enhance_with_ai(result, code)

        issues = result.get("issues", [])

        for issue in issues:

            input_text = issue_to_input_text(issue)
            output_text = issue.description

            rows.append({
                "input_text": input_text,
                "output_text": output_text
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    print("Dataset created:", output_file)


if __name__ == "__main__":
    build_dataset_from_folder(
        "sample_python_code",
        "reviewer/ml/auto_dataset.json"
    )