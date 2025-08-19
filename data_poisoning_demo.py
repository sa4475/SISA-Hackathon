from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_and_eval(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    return accuracy_score(y_test, preds)


def poison_labels(y, fraction: float = 0.2, seed: int = 7):
    rng = np.random.default_rng(seed)
    y_poisoned = y.copy()
    n = len(y)
    idx = rng.choice(n, int(n * fraction), replace=False)
    y_poisoned[idx] = 1 - y_poisoned[idx]
    return y_poisoned


def main() -> None:
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_redundant=2,
        n_classes=2,
        random_state=0,
    )
    clean_acc = train_and_eval(X, y)
    y_poison = poison_labels(y, fraction=0.2)
    poison_acc = train_and_eval(X, y_poison)

    print("[Data Poisoning Demo]")
    print(f"Clean accuracy:   {clean_acc:.3f}")
    print(f"Poisoned accuracy:{poison_acc:.3f}")
    print("Impact: Lower accuracy under label poisoning.")


if __name__ == "__main__":
    main()


