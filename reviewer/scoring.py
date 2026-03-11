def calculate_score(issues):
    if not issues:
        return {"score": 95}

    score = 100

    for issue in issues:
        severity = getattr(issue, "severity", "INFO")

        if severity == "INFO":
            score -= 3
        elif severity == "WARNING":
            score -= 8
        elif severity == "CRITICAL":
            score -= 18
        else:
            score -= 5

    score = max(score, 0)
    return {
        "score": score,
        "reason": "No major rule violations detected, but perfection is reserved for code with stronger maintainability signals."
    }