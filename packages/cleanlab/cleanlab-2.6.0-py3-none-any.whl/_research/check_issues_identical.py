from typing import List
import numpy as np
import os
import argparse

# Function being evaluated
from cleanlab.segmentation.filter import find_label_issues

# Seed for reproducibility of random inputs
SEED = 42

def main(directory: str):
    """A MWE for computing the output of find_label_issues and saving it to a file.

    Parameters
    ----------
    directory : str
        A directory to save the output to.
    """
    # Configuration
    np.random.seed(SEED)
    N, K, H, W = 200, 2, 5, 5
    pred_probs_shape = (N, K, H, W)
    labels_shape = (N, H, W)
    batch_size = 50
    assert N % batch_size == 0
    
    # Create random inputs
    pred_probs = np.random.rand(*pred_probs_shape)
    labels = np.random.randint(0, 2, labels_shape)
    
    # Fetch outputs
    issues = find_label_issues(labels, pred_probs, n_jobs=None, batch_size=batch_size)

    # Save outputs
    os.makedirs(directory, exist_ok=True)
    np.save(directory + "/issues.npy", issues)
    
    
def compare_outputs(files: List[str]):
    """
    Compare the outputs of two files.
    
    Parameters"""
    issues_1 = np.load(files[0])
    issues_2 = np.load(files[1])
    assert np.array_equal(issues_1, issues_2), "Outputs are not identical."

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str, default=".")
    parser.add_argument("--compare-files", nargs=2, type=str, default=None)
    args = parser.parse_args()
    if args.compare_files is None:
        # Run the affected function and save the output
        main(args.directory)
    else:
        # Compare the saved outputs
        compare_outputs(args.compare_files)
    