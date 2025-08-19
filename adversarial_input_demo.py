from __future__ import annotations

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def fgsm(x: np.ndarray, grad_sign: np.ndarray, epsilon: float) -> np.ndarray:
    return x + epsilon * grad_sign


def main() -> None:
    print("[Adversarial Input Demo]")
    iris = load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)
    clean_acc = accuracy_score(y_test, clf.predict(X_test))

    # Approximate gradient sign via weights direction for demonstration
    W = clf.coef_.mean(axis=0)
    grad_sign = np.sign(W)
    X_adv = fgsm(X_test, grad_sign, epsilon=0.15)
    adv_acc = accuracy_score(y_test, clf.predict(X_adv))

    print(f"Clean accuracy: {clean_acc:.3f}")
    print(f"Adversarial accuracy (FGSM-like): {adv_acc:.3f}")
    print("Observation: Subtle input shifts can reduce accuracy.")


if __name__ == "__main__":
    main()


