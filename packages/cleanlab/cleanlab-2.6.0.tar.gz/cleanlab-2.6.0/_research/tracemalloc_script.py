import tracemalloc
from typing import Tuple
import numpy as np
from pathlib import Path
from tempfile import TemporaryDirectory
from cleanlab.segmentation.filter import find_label_issues

def run_test_with_tracemalloc(pred_probs: np.memmap, labels: np.memmap, batch_size: int) -> None:
    """
    Function to profile find_label_issues with tracemalloc.
    """
    tracemalloc.start()

    # Snapshot before
    snapshot1 = tracemalloc.take_snapshot()

    # Execute the function
    find_label_issues(labels, pred_probs, n_jobs=1, batch_size=batch_size)

    # Snapshot after
    snapshot2 = tracemalloc.take_snapshot()

    # Stop tracemalloc
    tracemalloc.stop()

    # Analyze memory
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    for stat in stats[:20]:  # Display top 10 memory blocks
        print(stat)
        
def create_memmapped_arrays(tmp_path: Path, pred_probs_shape: Tuple[int, ...], labels_shape: Tuple[int, ...]) -> Tuple[Path, Path]:
    """
    Create memmapped arrays in a temporary directory and fill them with random data.

    Parameters
    ----------
    tmp_path : Path
        The path to the temporary directory.
    pred_probs_shape : Tuple[int, ...]
        The shape of the prediction probabilities array.
    labels_shape : Tuple[int, ...]
        The shape of the labels array.

    Returns
    -------
    Tuple[Path, Path]: Paths to the created memmapped arrays for prediction probabilities and labels.
    """
    pred_probs_file = tmp_path / "pred_probs.dat"
    labels_file = tmp_path / "labels.dat"

    pred_probs = np.memmap(pred_probs_file, dtype='float64', mode='w+', shape=pred_probs_shape)
    labels = np.memmap(labels_file, dtype='int', mode='w+', shape=labels_shape)

    pred_probs[:] = np.random.rand(*pred_probs_shape)
    labels[:] = np.random.randint(0, 2, labels_shape)

    pred_probs.flush()
    labels.flush()

    return pred_probs_file, labels_file

if __name__ == "__main__":
 with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        N, K, H, W = 20000, 20, 10, 10
        pred_probs_shape = (N, K, H, W)
        labels_shape = (N, H, W)
        batch_sizes = [10, 5000]
        
        pred_probs_file, labels_file = create_memmapped_arrays(tmp_path, pred_probs_shape, labels_shape)

        pred_probs = np.memmap(pred_probs_file, dtype='float64', mode='r', shape=pred_probs_shape)
        labels = np.memmap(labels_file, dtype='int', mode='r', shape=labels_shape)
        for batch_size in batch_sizes:
            print(f"Analyzing batch size {batch_size}")
            
            run_test_with_tracemalloc(pred_probs, labels, batch_size)
            print("-"*80, "\n")