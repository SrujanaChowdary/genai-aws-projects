COMPLEX_HINTS = (
    "step by step",
    "compare",
    "analyze",
    "design",
    "trade-off",
    "explain why",
)


def is_complex(prompt: str) -> bool:
    p = prompt.lower()
    return len(prompt) > 1000 or any(h in p for h in COMPLEX_HINTS)


def select_model(prompt: str, small: str, large: str) -> str:
    return large if is_complex(prompt) else small
