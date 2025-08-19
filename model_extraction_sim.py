from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def main() -> None:
    print("[Model Extraction Simulation]")
    X, y = make_classification(n_samples=1500, n_features=10, n_informative=6, random_state=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Target (victim) model — treated as a black box that answers queries
    target = KNeighborsClassifier(n_neighbors=5)
    target.fit(X_train, y_train)
    target_acc = accuracy_score(y_test, target.predict(X_test))

    # Attacker queries the target to build a surrogate dataset
    rng = np.random.default_rng(0)
    X_query = rng.normal(size=(2000, X.shape[1]))
    y_query = target.predict(X_query)

    # Train surrogate
    surrogate = DecisionTreeClassifier(max_depth=6, random_state=0)
    surrogate.fit(X_query, y_query)
    mimic_acc = accuracy_score(target.predict(X_test), surrogate.predict(X_test))

    print(f"Target accuracy on test:   {target_acc:.3f}")
    print(f"Surrogate mimic accuracy:  {mimic_acc:.3f}")
    print("Insight: With enough queries, a surrogate can approximate decision behavior.")


if __name__ == "__main__":
    main()


