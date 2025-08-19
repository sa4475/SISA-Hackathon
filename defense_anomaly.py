import math
from collections import Counter


def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    length = float(len(text))
    probs = [count / length for count in counts.values()]
    return -sum(p * math.log(p, 2) for p in probs if p > 0)


def is_suspicious(text: str) -> bool:
    # Heuristic threshold; entropy > 3 suggests randomness/obfuscation.
    return shannon_entropy(text) > 3.0


if __name__ == '__main__':
    queries = [
        "admin' OR '1'='1",
        "a" * 20,
        "qziysdkfmcqewru345",
        "<script>alert(1)</script>",
    ]
    suspicious = [q for q in queries if is_suspicious(q)]
    print("High-entropy suspicious queries:", suspicious)
