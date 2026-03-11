import argparse
from pathlib import Path

from reviewer.analyzer import analyze_code
from reviewer.report import print_report, export_json_report
from reviewer.ml.ai_engine import enhance_with_ai

def main():
    parser = argparse.ArgumentParser(
        description="AI Code Review System (CLI)"
    )

    parser.add_argument(
        "file",
        help="Path to the Python source file to review"
    )

    parser.add_argument(
        "--json",
        help="Path to save JSON report",
        required=False
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File not found -> {file_path}")
        return

    if file_path.suffix != ".py":
        print("Error: Only Python (.py) files are supported")
        return

    try:
        code = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    result = analyze_code(code)
    result = enhance_with_ai(result, code)

    print_report(result)

    if args.json:
        export_json_report(result, args.json)

if __name__ == "__main__":
    main()