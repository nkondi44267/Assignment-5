# Assignment 5: Quicksort Algorithm — Implementation, Analysis, and Randomization

Python implementations of deterministic last-pivot Quicksort and randomized-pivot Quicksort, with unit tests, reproducible benchmarks, data, plots, and an analysis report.

## Files

- `quicksort.py`: algorithms and simple usage example
- `test_quicksort.py`: correctness checks
- `benchmark.py`: repeated timed comparisons; produces CSV and chart
- `benchmark_results.csv`: experimental measurements (five trials per condition)
- `benchmark_chart.png`: comparison of mean running times by input distribution
- `REPORT.md`: complete implementation, theoretical and experimental analysis
- `Assignment_5_Quicksort_Report.pdf`: print-ready report with empirical chart

## Requirements

- Python 3.10 or later (standard library for algorithms and tests)
- Matplotlib for benchmark chart: `python -m pip install matplotlib`

## Run

```bash
python quicksort.py
python -m unittest -v test_quicksort.py
python benchmark.py
```

To use in another Python program:

```python
from quicksort import quicksort, randomized_quicksort

items = [8, 3, 7, 1, 4]
quicksort(items)
print(items)  # [1, 3, 4, 7, 8]

more_items = [8, 3, 7, 1, 4]
randomized_quicksort(more_items)
print(more_items)
```

Both functions modify the given list in place and also return it.

## Main findings

- Both implementations sort the tested inputs correctly.
- Balanced partitions lead to `O(n log n)` behavior; pathologically unbalanced partitions lead to `O(n^2)` time.
- Last-element-pivot Quicksort slows dramatically on sorted and reverse-sorted input.
- Random pivots improve robustness to input order, although worst-case `O(n^2)` remains possible.
- Both algorithms use `O(log n)` auxiliary stack space in **these implementations** because the smaller partition is handled recursively and the larger one iteratively.

Full setup, measurement procedure, observed data, caveats, and conclusions are in `REPORT.md` and the PDF.

## GitHub submission

Create an empty GitHub repository, add these files, and push them:

```bash
git init
git add .
git commit -m "Implement and benchmark deterministic and randomized Quicksort"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Replace the example GitHub URL with your own empty repository's URL. Submit the resulting repository link to your instructor.
