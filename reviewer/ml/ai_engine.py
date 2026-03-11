from reviewer.ml.retriever import ExplanationRetriever

retriever = None
retriever_failed = False

def get_retriever():
    global retriever, retriever_failed

    if retriever_failed:
        return None

    if retriever is None:
        try:
            retriever = ExplanationRetriever()
        except Exception as e:
            print(f"[AI Warning] Failed to initialize retriever: {e}")
            retriever_failed = True
            return None

    return retriever


def get_code_preview(code: str, max_lines: int = 6) -> str:
    lines = code.strip().splitlines()
    preview = lines[:max_lines]
    return " ".join(line.strip() for line in preview)


def add_improvement_hints(issue):
    if issue.rule_id == "NESTED_LOOP":
        issue.better_approach = (
            "Use a set or dictionary-based lookup to avoid comparing every pair of values."
        )
        issue.expected_improvement = (
            "Can reduce time complexity from O(n²) to O(n) in common duplicate-checking cases."
        )

    elif issue.rule_id == "LONG_FUNCTION":
        issue.better_approach = (
            "Split the function into smaller helper functions, each handling one clear responsibility."
        )
        issue.expected_improvement = (
            "Improves readability, testability, and maintainability."
        )

    elif issue.rule_id == "FUNCTION_PARAMETER_COUNT":
        issue.better_approach = (
            "Group related parameters into a dataclass, config object, or structured input."
        )
        issue.expected_improvement = (
            "Reduces cognitive load and makes the function interface easier to use correctly."
        )

    elif issue.rule_id == "CYCLOMATIC_COMPLEXITY":
        issue.better_approach = (
            "Reduce branching by extracting conditions into helper functions or simplifying control flow."
        )
        issue.expected_improvement = (
            "Makes the function easier to test, debug, and reason about."
        )


def enhance_with_ai(result, code):
    issues = result.get("issues", [])
    code_preview = get_code_preview(code)
    retriever_instance = get_retriever()

    for issue in issues:
        metrics = issue.metrics or {}

        if retriever_instance is not None:
            rule_signals = {
                "rule_id": issue.rule_id,
                "category": issue.category,
                "severity": issue.severity,
                "function_name": issue.function_name,
                "metrics": str(metrics),
                "snippet": issue.snippet[:200] if issue.snippet else "",
                "code_preview": code_preview
            }

            try:
                explanation = retriever_instance.retrieve_best_explanation(rule_signals)
                if explanation:
                    issue.explanation = explanation
            except Exception as e:
                print(f"[AI Warning] Could not retrieve explanation for {issue.rule_id}: {e}")

        add_improvement_hints(issue)

    return result