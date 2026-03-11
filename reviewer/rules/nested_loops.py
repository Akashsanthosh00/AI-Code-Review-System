from typing import List, Dict
from reviewer.rules.base_rule import BaseRule
from reviewer.core.issue_context import IssueContext
import ast


class NestedLoopRule(BaseRule):

    rule_id = "NESTED_LOOP"
    category = "performance"

    def check(self, functions: List[Dict], config: Dict) -> List[IssueContext]:

        issues = []

        for func in functions:

            ast_node = func["ast_node"]
            max_depth = self._max_loop_depth(ast_node)

            severity = self._get_severity_for_nesting(max_depth)

            if severity == "INFO":
                continue

            issues.append(
                IssueContext(
                    rule_id=self.rule_id,
                    title="Nested loops detected",
                    category=self.category,
                    severity=severity,
                    function_name=func["name"],
                    line_start=func["start_line"],
                    line_end=func["end_line"],
                    snippet=self._extract_snippet(func),
                    description=f"Function '{func['name']}' contains nested loops "f"with depth {max_depth}.",
                    why_it_matters="Nested loops can increase time complexity significantly, especially for large inputs.",
                    suggestion="Consider using a set or dictionary-based lookup to avoid pairwise comparison and reduce time complexity.",
                    example_hint=None,
                    metrics={
                        "nesting_depth": max_depth
                    },
                    extra={}
                )
            )

        return issues

    def _extract_snippet(self, func: Dict) -> str:
        return func.get("source", "")

    def _get_severity_for_nesting(self, depth: int) -> str:

        if depth >= 3:
            return "CRITICAL"
        elif depth == 2:
            return "WARNING"
        else:
            return "INFO"

    def _max_loop_depth(self, node: ast.AST, current_depth: int = 0) -> int:

        max_depth = current_depth

        for child in ast.iter_child_nodes(node):

            if isinstance(child, (ast.For, ast.While, ast.AsyncFor)):
                depth = self._max_loop_depth(child, current_depth + 1)
            else:
                depth = self._max_loop_depth(child, current_depth)

            max_depth = max(max_depth, depth)

        return max_depth