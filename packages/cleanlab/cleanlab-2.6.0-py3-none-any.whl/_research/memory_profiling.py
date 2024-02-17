from typing import Tuple
import numpy as np
from pathlib import Path
from tempfile import TemporaryDirectory
from multiprocessing import Process, Queue
from memory_profiler import memory_usage
from cleanlab.segmentation.filter import find_label_issues

def create_memmapped_arrays(tmp_path: Path, pred_probs_shape: Tuple[int, ...], labels_shape: Tuple[int, ...]) -> Tuple[Path, Path]:
    """
    Create memmapped arrays in a temporary directory and fill them with random data.

    Args:
    - tmp_path (Path): The path to the temporary directory.
    - N (int): The number of samples.
    - pred_probs_shape (Tuple[int, ...]): The shape of the prediction probabilities array.
    - labels_shape (Tuple[int, ...]): The shape of the labels array.

    Returns:
    - Tuple[Path, Path]: Paths to the created memmapped arrays for prediction probabilities and labels.
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

def test_function(pred_probs: np.memmap, labels: np.memmap, batch_size: int) -> None:
    """
    Test function to profile memory usage of find_label_issues.

    Args:
    - pred_probs (np.memmap): Memmapped array of prediction probabilities.
    - labels (np.memmap): Memmapped array of labels.
    - batch_size (int): Batch size for processing.
    """
    find_label_issues(labels, pred_probs, n_jobs=None, batch_size=batch_size)

def run_test_in_process(queue: Queue, pred_probs_file: Path, labels_file: Path, batch_size: int) -> None:
    """
    Wrapper function to run test_function in a separate process and measure memory usage.

    Args:
    - queue (Queue): Queue to put memory usage results.
    - pred_probs_file (Path): Path to the memmapped array of prediction probabilities.
    - labels_file (Path): Path to the memmapped array of labels.
    - batch_size (int): Batch size for processing.
    """
    pred_probs = np.memmap(pred_probs_file, dtype='float64', mode='r', shape=pred_probs_shape)
    labels = np.memmap(labels_file, dtype='int', mode='r', shape=labels_shape)

    mem_usage = memory_usage(
        (test_function, (pred_probs, labels, batch_size)),
        interval=0.01,
        max_usage=True,
        include_children=True,
    )
    queue.put(mem_usage)

if __name__ == "__main__":
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        N, K, H, W = 100000, 20, 10, 10
        pred_probs_shape = (N, K, H, W)
        labels_shape = (N, H, W)
        batch_sizes = [5000]

        pred_probs_file, labels_file = create_memmapped_arrays(tmp_path, pred_probs_shape, labels_shape)

        results_queue = Queue()
        processes = []

        for batch_size in batch_sizes:
            process = Process(target=run_test_in_process, args=(results_queue, pred_probs_file, labels_file, batch_size))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        for batch_size in batch_sizes:
            print(f"Peak memory used with batch size {batch_size}: {results_queue.get()} MiB")
