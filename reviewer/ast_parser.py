# This module is responsible for parsing Python code and extracting
# structural information using AST.

import ast
from typing import Dict, List

def parse_code(code: str) -> Dict[str, object]:
    """
        Parse Python source code using AST and extract structural information.

        Parameters:
            code (str): Python source code as a string

        Returns:
            dict: Parsed structural information
        """

    tree = ast.parse(code)

    functions: List[Dict[str, object]] = []
    loop_count = 0
    if_count = 0

    for node in ast.walk(tree):

        #--------FUNCTION METADATA----------
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = node.end_lineno
            line_count = end_line - start_line + 1

            docstring = ast.get_docstring(node)
            has_docstring = docstring is not None

            parameter_count = len(node.args.args)

            functions.append({
                "name": node.name,
                "start_line": start_line,
                "end_line": end_line,
                "line_count": line_count,
                "parameter_count": parameter_count,
                "has_docstring": has_docstring,
                "ast_node": node
            })

         #----------- LOOP COUNT -------------
        elif isinstance(node, (ast.For, ast.While)):
            loop_count += 1

        #------------ IF COUNT ------------
        elif isinstance(node, ast.If):
            if_count += 1

    return {
        "functions": functions,
        "function_count": len(functions),
        "loop_count": loop_count,
        "if_count": if_count
    }