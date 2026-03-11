from typing import List, Dict, cast
from reviewer.rules.base_rule import BaseRule
from reviewer.core.issue_context import IssueContext
import ast

class CyclomaticComplexityRule(BaseRule):

    rule_id = "CYCLOMATIC_COMPLEXITY"
    category = "complexity"

    def check(self, functions: List[Dict], config: Dict) -> List[IssueContext]:

        issues = []

        warning = config.get("cyclomatic_complexity", {}).get("warning", 10)
        critical = config.get("cyclomatic_complexity", {}).get("critical", 15)

        for func in functions:

            ast_node = cast(ast.AST, func["ast_node"])

            visitor = CyclomaticComplexityVisitor()
            visitor.visit(ast_node)

            complexity = visitor.complexity

            if complexity >= warning:

                severity = (
                    "CRITICAL"
                    if complexity >= critical
                    else "WARNING"
                )

                function_name = cast(str, func["name"])
                start_line = cast(int, func["start_line"])
                end_line = cast(int, func["end_line"])
                snippet = cast(str, func.get("source", ""))

                issues.append(
                    IssueContext(
                        rule_id=self.rule_id,
                        title="High Cyclomatic Complexity",
                        category=self.category,
                        severity=severity,
                        function_name=function_name,
                        line_start=start_line,
                        line_end=end_line,
                        snippet=snippet,
                        description=(
                            f"Function '{function_name}' has cyclomatic "
                            f"complexity {complexity}."
                        ),
                        why_it_matters=(
                            "Higher cyclomatic complexity makes code harder "
                            "to understand, test, debug, and maintain."
                        ),
                        suggestion=(
                            "Refactor the function by simplifying branching "
                            "logic or splitting it into smaller helper functions."
                        ),
                        example_hint=None,
                        metrics={
                            "complexity": complexity
                        },
                        extra={}
                    )
                )

        return issues


# -------------------------
# VISITOR
# -------------------------

class CyclomaticComplexityVisitor(ast.NodeVisitor):

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += len(node.handlers)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)