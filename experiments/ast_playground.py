import ast

test_code = """
def greet(name):
    if name:
        print("Hello", name)
    else:
        print("Hello World")

for i in range(3):
    greet(i)
    
def add(a, b):
    result = a + b
    return result

for i in range(3):
    if i % 2 == 0:
        print(i)
"""

tree = ast.parse(test_code)

function_count = 0
loop_count = 0
if_count = 0

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        function_count += 1
        print("Found function:", node.name)

    elif isinstance(node, ast.For) or isinstance(node, ast.While):
        loop_count += 1
        print("Found loop:", type(node).__name__)

    elif isinstance(node, ast.If):
        if_count += 1
        print("Found if condition")

print("\nSummary:")
print("Functions:", function_count)
print("Loops:", loop_count)
print("If conditions:", if_count)
