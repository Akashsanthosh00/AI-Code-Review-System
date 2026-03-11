from typing import List, Dict, cast
from reviewer.core.issue_context import IssueContext


# =========================
# FUNCTION PARAMETER RULE
# =========================

class FunctionParameterRule:
    id = "FUNCTION_PARAMETER_COUNT"

    def check(
        self,
        functions: List[Dict[str, object]],
        config: Dict[str, object]
    ) -> List[IssueContext]:

        issues = []

        warning = config.get("function_parameters", {}).get("warning", 4)
        critical = config.get("function_parameters", {}).get("critical", 6)

        for func in functions:

            param_count = cast(int, func.get("parameter_count", 0))

            severity = None

            if param_count >= critical:
                severity = "CRITICAL"
            elif param_count >= warning:
                severity = "WARNING"

            if severity:
                function_name = cast(str, func["name"])
                start_line = cast(int, func["start_line"])
                end_line = cast(int, func["end_line"])
                snippet = cast(str, func.get("source", ""))

                issues.append(
                    IssueContext(
                        rule_id=self.id,
                        title="Too Many Parameters",
                        category="maintainability",
                        severity=severity,
                        function_name=function_name,
                        line_start=start_line,
                        line_end=end_line,
                        snippet=snippet,
                        description=(
                            f"Function '{function_name}' has {param_count} parameters."
                        ),
                        why_it_matters=(
                            "Functions with too many parameters are harder "
                            "to understand, test, and maintain."
                        ),
                        suggestion=(
                            "Reduce the number of parameters by grouping "
                            "related values into objects or helper structures."
                        ),
                        example_hint=None,
                        metrics={
                            "parameter_count": param_count
                        },
                        extra={}
                    )
                )

        return issues