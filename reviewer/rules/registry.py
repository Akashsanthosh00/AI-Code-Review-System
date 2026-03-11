from reviewer.rules.nested_loops import NestedLoopRule
from reviewer.rules.long_functions import LongFunctionRule
from reviewer.rules.cyclomatic_complexity import CyclomaticComplexityRule
from reviewer.rules.function_parameters import FunctionParameterRule

def get_all_rules():
    """
    Returns all active instances.
    """

    return [
        NestedLoopRule(),
        LongFunctionRule(),
        FunctionParameterRule(),
        CyclomaticComplexityRule()
    ]