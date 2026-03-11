from typing import Dict, List

from reviewer.ast_parser import parse_code
from reviewer.rules.registry import get_all_rules
from reviewer.scoring import calculate_score
from reviewer.config.config_loader import load_rules_config

def analyze_code(code: str) -> Dict[str, object]:
    """
    Analyze Python source code and return review issues.
    """

    parsed_data = parse_code(code)
    functions = parsed_data["functions"]

    issues: List[Dict[str, object]] = []

    config = load_rules_config()
    rules = get_all_rules()

    # ---- RULE EXECUTION ----
    for rule in rules:
        try:
            issues.extend(rule.check(functions, config))
        except Exception as e:
            print(f"Rule {rule.__class__.__name__} failed: {e}")

    # ---- SCORE ----
    score_info = calculate_score(issues)

    return {
        "summary": {
            "function_count": parsed_data["function_count"],
            "loop_count": parsed_data["loop_count"],
            "if_count": parsed_data["if_count"],
            "issue_count": len(issues)
        },
        "issues": issues,
        "score": score_info
    }