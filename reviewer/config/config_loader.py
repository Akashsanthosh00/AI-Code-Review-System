import json
from pathlib import Path
from typing import Dict

def load_rules_config() -> Dict[str, Dict[str, int]]:
    """
    Load rule thresholds from rules_config.json.

    Returns:
        dict: Rule configuration dictionary
    """
    config_path = Path(__file__).parent / "rules_config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Rules config file not found at {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    return config