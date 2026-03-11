from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass
class IssueContext:
    rule_id: str
    title: str
    category: str
    severity: str
    function_name: str
    line_start: int
    line_end: int
    snippet: str

    description: Optional[str] = None
    why_it_matters: Optional[str] = None
    suggestion: Optional[str] = None
    example_hint: Optional[str] = None
    better_approach: Optional[str] = None
    expected_improvement: Optional[str] = None

    metrics: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)