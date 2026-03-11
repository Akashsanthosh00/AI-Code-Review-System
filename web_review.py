from reviewer.analyzer import analyze_code
from reviewer.ml.ai_engine import enhance_with_ai
from reviewer.report import print_report

import io
import sys

def analyze_code_to_text(code: str) -> str:
    result = analyze_code(code)
    result = enhance_with_ai(result, code)

    buffer = io.StringIO()
    sys.stdout = buffer

    print_report(result)

    sys.stdout = sys.__stdout__

    return buffer.getvalue()