from typing import List, Dict, cast
from reviewer.core.issue_context import IssueContext

class LongFunctionRule:
    id = "LONG_FUNCTION"

    def check(
        self,
        functions: List[Dict[str, object]],
        config: Dict[str, object]
    ) -> List[IssueContext]:

        issues = []

        thresholds = config["long_function"]
        warning_limit = thresholds["warning"]
        critical_limit = thresholds["critical"]

        for func in functions:
            line_count = cast(int, func["line_count"])

            if line_count > warning_limit:

                severity = (
                    "CRITICAL"
                    if line_count > critical_limit
                    else "WARNING"
                )

                function_name = cast(str, func["name"])
                start_line = cast(int, func["start_line"])
                end_line = cast(int, func["end_line"])
                snippet = cast(str, func.get("source", ""))

                issues.append(
                    IssueContext(
                        rule_id=self.id,
                        title="Function is too long",
                        category="maintainability",
                        severity=severity,
                        function_name=function_name,
                        line_start=start_line,
                        line_end=end_line,
                        snippet=snippet,
                        description=(
                            f"Function '{function_name}' is too long "
                            f"({line_count} lines)."
                        ),
                        why_it_matters=(
                            "Long functions are harder to read, test, "
                            "debug, and maintain."
                        ),
                        suggestion=(
                            "Break this function into smaller helper "
                            "functions with focused responsibilities."
                        ),
                        example_hint=None,
                        metrics={
                            "line_count": line_count
                        },
                        extra={}
                    )
                )

        return issues