# from reviewer.ast_parser import parse_code
#
# test_code = """def greet(name):
#     \"\"\"Greets the user\"\"\"
#     if name:
#         print("Hello", name)
#     else:
#         print("Hello World")
#
# def add(a, b):
#     result = a + b
#     return result
# """
#
# result = parse_code(test_code)
#
# for func in result["functions"]:
#     print(func)
#
# print("\nSummary:")
# print("Function count:", result["function_count"])
# print("Loop count:", result["loop_count"])
# print("If count:", result["if_count"])

# from reviewer.ast_parser import parse_code
# from reviewer.rules import check_long_functions
#
# test_code = """def short_func():
#     print("This is short")
#
# def long_func():
#     x = 0
#     y = 1
#     z = 2
#     a = 3
#     b = 4
#     c = 5
#     d = 6
#     e = 7
#     f = 8
#     g = 9
#     h = 10
#     i = 11
#     j = 12
#     k = 13
#     l = 14
#     m = 15
#     n = 16
#     o = 17
#     p = 18
#     q = 19
#     r = 20
#     s = 21
#     t = 22
#     u = 23
#     v = 24
#     w = 25
#     x = 26
#     y = 27
#     z = 28
#     a = 29
#     b = 30
#     c = 31
#     d = 32
#     e = 33
#     f = 34
#     g = 35
#     h = 36
#     i = 37
#     j = 38
#     k = 39
#     l = 40
#     m = 41
#     n = 42
#     o = 43
#     p = 44
#     q = 45
#     r = 46
#     s = 47
#     t = 48
#     u = 49
#     v = 50
#     w = 51
# """
#
# parsed = parse_code(test_code)
# issues = check_long_functions(parsed["functions"])
#
# print("Detected Issues:\n")
# for issue in issues:
#     print(issue)

from reviewer.analyzer import analyze_code

test_code = """def short_func():
    print("Hello")

def long_func():
    x = 0
    y = 1
    z = 2
    a = 3
    b = 4
    c = 5
    d = 6
    e = 7
    f = 8
    g = 9
    h = 10
    i = 11
    j = 12
    k = 13
    l = 14
    m = 15
    n = 16
    o = 17
    p = 18
    q = 19
    r = 20
    s = 21
    t = 22
    u = 23
    v = 24
    w = 25
    x = 26
    y = 27
    z = 28
    a = 29
    b = 30
    c = 31
    d = 32
    e = 33
    f = 34
    g = 35
    h = 36
    i = 37
    j = 38
    k = 39
    l = 40
    m = 41
    n = 42
    o = 43
    p = 44
    q = 45
    r = 46
    s = 47
    t = 48
    u = 49
    v = 50
    w = 51
"""

result = analyze_code(test_code)

print("Summary:")
print(result["summary"])

print("\nIssues:")
for issue in result["issues"]:
    print(issue)


