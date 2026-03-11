from abc import ABC, abstractmethod
from typing import List, Dict

class BaseRule(ABC):
    """
    Base class for all code review rules.
    """

    rule_id: str = "BASE_RULE"
    category: str = "GENERAL"
    severity: str = "INFO"

    @abstractmethod
    def check(self, functions: List[Dict], config: Dict) -> List[Dict]:
        """
        Run rule check.

        Returns:
            List of issues
        """
        pass