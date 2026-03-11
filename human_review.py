from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class Finding:
    category : str
    severity : str
    title : str
    what_i_saw : str
    why_it_matters : str
    suggestion : str

def _safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    return d[key] if isinstance(d, dict) and key in d else default

def _coerce_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _severity_from_rules(rule_output: Dict[str, Any]) -> str:
    """
    Heuristic severity based on typical rule outputs.
    Adjust thresholds to match your engine.
    """
    nested_loops = _coerce_int(_safe_get(rule_output, "nested_loops", 0))
    max_depth = _coerce_int(_safe_get(rule_output, "max_loop_depth", nested_loops))
    cc = _coerce_int(_safe_get(rule_output, "cyclomatic_complexity", 0))
    func_len = _coerce_int(_safe_get(rule_output, "function_length", 0))

    # High severity triggers
    if _safe_get(rule_output, "syntax_error", False) or _safe_get(rule_output, "runtime_error_risk", False):
        return "high"
    if nested_loops >= 2 or max_depth >= 2:
        return "high"
    if _safe_get(rule_output, "possible_cubic", False) or _safe_get(rule_output, "possible_exponential", False):
        return "high"
    if cc >= 16 or func_len >= 80:
        return "high"

    # Medium severity triggers
    if _safe_get(rule_output, "missing_edge_case", False) or _safe_get(rule_output, "bug_risk", False):
        return "medium"
    if _safe_get(rule_output, "possible_quadratic", False):
        return "medium"
    if cc >= 10 or func_len >= 40:
        return "medium"

    return "low"


def _estimate_time_complexity(rule_output: Dict[str, Any]) -> Optional[str]:
    """
    Uses your existing rule outputs if present, otherwise makes a best-effort guess.
    """
    est = _safe_get(rule_output, "estimated_time_complexity")
    if isinstance(est, str) and est.strip():
        return est.strip()

    if _safe_get(rule_output, "possible_exponential", False):
        return "Exponential (likely)"
    if _safe_get(rule_output, "possible_cubic", False):
        return "O(n^3) (likely)"
    if _safe_get(rule_output, "possible_quadratic", False) or _coerce_int(_safe_get(rule_output, "nested_loops", 0)) >= 2:
        return "O(n^2) (likely)"
    if _safe_get(rule_output, "uses_sort_after_merge", False) or _safe_get(rule_output, "sort_in_loop", False):
        return "O(n log n) or worse (check sorting usage)"

    return None


def _build_findings(rule_output: Dict[str, Any]) -> List[Finding]:
    """
    Convert rule signals into user-facing findings.
    Add/remove rules here to match your engine output keys.
    """
    findings: List[Finding] = []

    nested_loops = _coerce_int(_safe_get(rule_output, "nested_loops", 0))
    max_depth = _coerce_int(_safe_get(rule_output, "max_loop_depth", nested_loops))
    possible_quadratic = bool(_safe_get(rule_output, "possible_quadratic", False))
    possible_cubic = bool(_safe_get(rule_output, "possible_cubic", False))
    uses_linear_search_in_loop = bool(_safe_get(rule_output, "uses_linear_search_in_loop", False))
    contains_membership_check = bool(_safe_get(rule_output, "contains_membership_check", False))
    inefficient_string_concat = bool(_safe_get(rule_output, "inefficient_string_concat", False))
    recursion = bool(_safe_get(rule_output, "recursion", False))
    repeated_subproblems = bool(_safe_get(rule_output, "repeated_subproblems", False))
    broad_exception = bool(_safe_get(rule_output, "broad_exception", False))
    missing_edge_case = bool(_safe_get(rule_output, "missing_edge_case", False))
    edge_case = _safe_get(rule_output, "edge_case", None)
    inplace_mutation = bool(_safe_get(rule_output, "inplace_mutation", False))
    mutates_list_in_loop = bool(_safe_get(rule_output, "mutates_list_in_loop", False))
    algorithm_mismatch = bool(_safe_get(rule_output, "algorithm_mismatch", False))
    simplification_opportunity = bool(_safe_get(rule_output, "simplification_opportunity", False))
    refactor_opportunity = bool(_safe_get(rule_output, "refactor_opportunity", False))

    # ---- Performance findings ----
    if possible_cubic or max_depth >= 3:
        findings.append(Finding(
            category="performance",
            severity="high",
            title="Very high time complexity risk",
            what_i_saw="Multiple nested loops / deep loop nesting detected.",
            why_it_matters="This can become extremely slow as input grows and may time out on large datasets.",
            suggestion="Reduce nesting by using precomputed maps/sets, sliding window, or rethinking the algorithm to avoid triple nested work."
        ))
    elif possible_quadratic or (nested_loops >= 2 or max_depth >= 2):
        findings.append(Finding(
            category="performance",
            severity="high",
            title="Quadratic time complexity risk",
            what_i_saw="Nested loops or repeated expensive operations were detected.",
            why_it_matters="This commonly leads to O(n²) behavior, which slows down quickly on larger inputs.",
            suggestion="Use a dictionary/set for faster lookups, or restructure logic to avoid scanning the list inside another loop."
        ))

    if uses_linear_search_in_loop or contains_membership_check:
        findings.append(Finding(
            category="performance",
            severity="medium" if not (nested_loops >= 2 or possible_quadratic) else "high",
            title="Repeated linear search inside loop",
            what_i_saw="A membership check / linear search is performed repeatedly inside a loop.",
            why_it_matters="Repeated scans can turn an apparently simple loop into O(n²) time.",
            suggestion="Use a set/dict/Counter to make lookups O(1) and compute results in one pass."
        ))

    if inefficient_string_concat:
        findings.append(Finding(
            category="performance",
            severity="low",
            title="Inefficient string building",
            what_i_saw="String concatenation is performed repeatedly in a loop.",
            why_it_matters="Repeated concatenation can create many intermediate strings and slow down runtime.",
            suggestion="Accumulate into a list and ''.join(...) at the end, or use slicing where applicable."
        ))

    if recursion and repeated_subproblems:
        findings.append(Finding(
            category="performance",
            severity="high",
            title="Inefficient recursion (repeated subproblems)",
            what_i_saw="Recursive calls with overlapping subproblems were detected.",
            why_it_matters="This can cause exponential runtime and become unusable for larger n.",
            suggestion="Add memoization (cache) or rewrite as iterative DP to reduce time complexity."
        ))
    elif recursion:
        findings.append(Finding(
            category="performance",
            severity="medium",
            title="Recursion depth risk",
            what_i_saw="Recursive implementation detected.",
            why_it_matters="Large inputs may hit recursion limits or cause stack overflows.",
            suggestion="Consider an iterative version or ensure input constraints are safe; add memoization if applicable."
        ))

    # ---- Bug / correctness findings ----
    if broad_exception:
        findings.append(Finding(
            category="bug",
            severity="medium",
            title="Overly broad exception handling",
            what_i_saw="A bare/very broad except block was detected.",
            why_it_matters="It can hide real bugs and make failures silent and harder to debug.",
            suggestion="Catch specific exceptions (e.g., KeyError/ValueError) or use safer APIs like dict.get()."
        ))

    if algorithm_mismatch:
        findings.append(Finding(
            category="bug",
            severity="low",
            title="Implementation may not match function intent",
            what_i_saw="The function name/intent appears inconsistent with the algorithm used.",
            why_it_matters="This can confuse users and lead to wrong expectations about performance or behavior.",
            suggestion="Rename the function to match behavior, or implement the intended algorithm (e.g., true binary search)."
        ))

    if inplace_mutation or mutates_list_in_loop:
        findings.append(Finding(
            category="bug",
            severity="medium",
            title="Potential side effects due to mutation",
            what_i_saw="In-place mutation of input data was detected (or mutation while iterating).",
            why_it_matters="This can surprise callers and can introduce subtle bugs if the input is reused elsewhere.",
            suggestion="Avoid mutating inputs unless documented; use a copy (e.g., sorted(arr)) or build a new output list."
        ))

        # ---- Edge cases ----
    if missing_edge_case:
        extra = f" ({edge_case})" if edge_case else ""
        findings.append(Finding(
            category="edge_case",
            severity="medium",
            title="Missing edge case handling",
            what_i_saw=f"Edge case checks appear to be missing{extra}.",
            why_it_matters="Unhandled edge cases can cause runtime errors or incorrect results in real usage.",
            suggestion="Add guard clauses (e.g., empty input, invalid parameters) and include tests for those cases."
        ))

        # ---- Readability / refactor ----
    if simplification_opportunity:
        findings.append(Finding(
            category="readability",
            severity="low",
            title="Simplification opportunity",
            what_i_saw="The code can be written more directly / Pythonically.",
            why_it_matters="Simpler code is easier to maintain, review, and less error-prone.",
            suggestion="Prefer direct iteration (for x in items), enumerate, comprehensions, and remove redundant variables."
        ))

    if refactor_opportunity:
        findings.append(Finding(
            category="readability",
            severity="medium",
            title="Refactor for clarity",
            what_i_saw="Multiple branches/conditions suggest the function can be broken down.",
            why_it_matters="High branching increases cognitive load and makes future changes risky.",
            suggestion="Extract helper functions, reduce nesting (early returns), and add small comments for non-obvious logic."
        ))

    return findings

def _grade_and_score(findings: List[Finding], rule_output: Dict[str, Any]) -> Tuple[str, int, str]:
    """
    Produces an overall grade/score and a 1–2 line summary.
    """
    # Base score
    score = 90

    # Weight by severity
    for f in findings:
        if f.severity == "high":
            score -= 18
        elif f.severity == "medium":
            score -= 10
        else:
            score -= 4

    # Clamp
    score = max(0, min(100, score))

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "E"

        # Summary: pick top 2 findings by severity
        sev_rank = {"high": 3, "medium": 2, "low": 1}
        top = sorted(findings, key=lambda x: sev_rank.get(x.severity, 0), reverse=True)[:2]
        if not top:
            summary = "No major issues detected. The code looks clean and maintainable."
        else:
            summary = "; ".join([f"{t.category} concern ({t.severity})" for t in top])
            summary = summary[0].upper() + summary[1:] + "."

        return grade, score, summary

    # ----------------------------
    # Public API
    # ----------------------------

    def generate_human_review(
            code: str,
            rule_output: Dict[str, Any],
            function_name: Optional[str] = None,
    ) -> str:
        """
        Returns a human-readable review (string) for display to users.

        Parameters
        ----------
        code : str
            The code being reviewed (can be a single function or a snippet).
        rule_output : Dict[str, Any]
            Output from your Layer 1/2 rule engine.
        function_name : Optional[str]
            If you have it, include for nicer reporting.

        Returns
        -------
        str
            A formatted human-readable review.
        """
        findings = _build_findings(rule_output)

        # Always compute metrics we can show
        cc = _safe_get(rule_output, "cyclomatic_complexity")
        func_len = _safe_get(rule_output, "function_length")
        max_depth = _safe_get(rule_output, "max_loop_depth", _safe_get(rule_output, "nested_loops"))
        time_complexity = _estimate_time_complexity(rule_output)

        grade, score, summary = _grade_and_score(findings, rule_output)

        header_name = f" for `{function_name}`" if function_name else ""
        lines: List[str] = []
        lines.append("### 🔎 Code Review Report" + header_name)
        lines.append("")
        lines.append(f"#### Overall Assessment: {('✅ Looks Good' if score >= 85 else '⚠ Needs Improvement')}")
        lines.append(summary)
        lines.append("")
        if not findings:
            lines.append("No significant issues were detected by the rule engine.")
            lines.append("")
        else:
            lines.append("### Findings")
            # Group in consistent order
            order = ["performance", "bug", "edge_case", "readability"]
            sev_rank = {"high": 3, "medium": 2, "low": 1}
            sorted_findings = sorted(
                findings,
                key=lambda f: (order.index(f.category) if f.category in order else 99, -sev_rank.get(f.severity, 0)),
            )

            for idx, f in enumerate(sorted_findings, start=1):
                sev_label = f.severity.capitalize()
                lines.append(f"{idx}) {f.title} ({sev_label} Severity)")
                lines.append(f"   - What I saw: {f.what_i_saw}")
                lines.append(f"   - Why it matters: {f.why_it_matters}")
                lines.append(f"   - Suggestion: {f.suggestion}")
                lines.append("")

        # Metrics section
        lines.append("### 📊 Complexity & Metrics")
        if time_complexity:
            lines.append(f"- Estimated Time Complexity: **{time_complexity}**")
        if cc is not None:
            lines.append(f"- Cyclomatic Complexity: **{cc}**")
        if func_len is not None:
            lines.append(f"- Function Length: **{func_len} lines**")
        if max_depth is not None:
            lines.append(f"- Max Loop Depth: **{max_depth}**")
        lines.append("")
        lines.append(f"### ✅ Final Recommendation")
        lines.append(f"Grade: **{grade}**  |  Score: **{score}/100**")
        if score >= 85:
            lines.append("Keep this structure. Consider minor readability improvements if desired.")
        elif score >= 70:
            lines.append(
                "Address the highlighted issues (especially performance/edge cases) to improve reliability and maintainability.")
        else:
            lines.append(
                "Refactor the function to reduce complexity and add missing validations; then re-run the review.")
        lines.append("")

        return "\n".join(lines)