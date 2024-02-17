import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

from cleanlab.datalab.datalab import Datalab

from sklearn.model_selection import train_test_split
from cleanlab.benchmarking.noise_generation import (
    generate_noise_matrix_from_trace,
    generate_noisy_labels,
)

SEED = 123
np.random.seed(SEED)

BINS = {
    "low": [-np.inf, 3.3],
    "mid": [3.3, 6.6],
    "high": [6.6, +np.inf],
}

BINS_MAP = {
    "low": 0,
    "mid": 1,
    "high": 2,
}


def create_data():

    X = np.random.rand(2000, 2) * 5
    y = np.sum(X, axis=1)
    # Map y to bins based on the BINS dict
    y_bin = np.array([k for y_i in y for k, v in BINS.items() if v[0] <= y_i < v[1]])
    y_bin_idx = np.array([BINS_MAP[k] for k in y_bin])

    # Split into train and test
    X_train, X_test, y_train, y_test, y_train_idx, y_test_idx = train_test_split(
        X, y_bin, y_bin_idx, test_size=0.5, random_state=SEED
    )

 
    py = np.bincount(y_train_idx) / float(len(y_train_idx))
    m = len(BINS)

    noise_matrix = generate_noise_matrix_from_trace(
        m,
        trace=0.9 * m,
        py=py,
        valid_noise_matrix=True,
        seed=SEED,
    )

    noisy_labels_idx = generate_noisy_labels(y_train_idx, noise_matrix)
    noisy_labels = np.array([list(BINS_MAP.keys())[i] for i in noisy_labels_idx])
    
    py_test = np.bincount(y_test_idx) / float(len(y_test_idx))
    
    test_noise_matrix = generate_noise_matrix_from_trace(
        m,
        trace=0.9 * m,
        py=py_test,
        valid_noise_matrix=True,
        seed=SEED,
    )
    
    noisy_labels_test_idx = generate_noisy_labels(y_test_idx, test_noise_matrix)
    noisy_labels_test = np.array([list(BINS_MAP.keys())[i] for i in noisy_labels_test_idx])
    
    

    return X_train, y_train_idx, noisy_labels, noisy_labels_idx, X_test, y_test_idx, noisy_labels_test, noisy_labels_test_idx

def main():
    X_train, y_train_idx, noisy_labels, noisy_labels_idx, X_test, y_test_idx, noisy_labels_test, noisy_labels_test_idx = create_data()
    
    data = {"X": X_train, "y": noisy_labels}
    test_data = {"X": X_test, "y": noisy_labels_test}
    
    model = LogisticRegression()
    pred_probs = cross_val_predict(
        estimator=model, X=data["X"], y=data["y"], cv=5, method="predict_proba"
    )
    
    # Train on all training data to get test predictions
    model_test = LogisticRegression()
    test_pred_probs = model_test.fit(data["X"], data["y"]).predict_proba(test_data["X"])
    

    train_lab = Datalab(data, label_name="y")
    train_lab.find_issues(pred_probs=pred_probs, features=data["X"], issue_types={"label": {}})
    
    test_lab = Datalab(test_data, label_name="y", trained_datalab=train_lab)
    test_lab.find_issues(pred_probs=test_pred_probs, issue_types={"label": {}})
    
if __name__ == "__main__":
    main()