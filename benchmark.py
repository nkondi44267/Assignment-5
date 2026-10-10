"""Reproducible empirical comparison of Quicksort variants.

Run: python benchmark.py
Outputs benchmark_results.csv and benchmark_chart.png.
Timing excludes input copying and dataset generation. Time includes pivot RNG
for randomized Quicksort. The same original arrays are provided to both methods.
"""
import csv
import random
import statistics
import time
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from quicksort import quicksort, randomized_quicksort

SIZES = [100, 500, 1000, 2000, 4000]
TRIALS = 5
SEED = 8345
DISTRIBUTIONS = ('random', 'sorted', 'reverse-sorted')


def make_data(n, distribution, seed):
    if distribution == 'random':
        return random.Random(seed).sample(range(n * 10), n)
    if distribution == 'sorted':
        return list(range(n))
    return list(range(n - 1, -1, -1))


def run_benchmarks():
    results = []
    for distribution in DISTRIBUTIONS:
        for n in SIZES:
            timings = {'deterministic': [], 'randomized': []}
            for trial in range(TRIALS):
                original = make_data(n, distribution, SEED + trial * 10007 + n)
                expected = sorted(original)
                for name, sorter in (('deterministic', quicksort), ('randomized', randomized_quicksort)):
                    values = original.copy()
                    start = time.perf_counter()
                    if name == 'randomized':
                        sorter(values, rng=random.Random(SEED + trial * 31 + n))
                    else:
                        sorter(values)
                    elapsed = (time.perf_counter() - start) * 1000
                    assert values == expected, f'{name} failed {distribution} size {n}'
                    timings[name].append(elapsed)
            for name, samples in timings.items():
                results.append({'distribution': distribution, 'size': n, 'algorithm': name,
                                'trials': TRIALS, 'mean_ms': round(statistics.mean(samples), 4),
                                'median_ms': round(statistics.median(samples), 4),
                                'min_ms': round(min(samples), 4), 'max_ms': round(max(samples), 4)})
            print(f'{distribution:14} n={n:5}: deterministic={statistics.mean(timings["deterministic"]):9.3f} ms; randomized={statistics.mean(timings["randomized"]):9.3f} ms')

    output = Path(__file__).resolve().parent
    with (output / 'benchmark_results.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8))
    for ax, distribution in zip(axes, DISTRIBUTIONS):
        for name in ('deterministic', 'randomized'):
            subset = [r for r in results if r['distribution'] == distribution and r['algorithm'] == name]
            ax.plot([r['size'] for r in subset], [r['mean_ms'] for r in subset], marker='o', label=name)
        ax.set_title(distribution.title())
        ax.set_xlabel('Number of elements (n)')
        ax.set_ylabel('Mean run time (ms)')
        ax.grid(alpha=.3)
        ax.legend(fontsize=8)
    fig.suptitle('Quicksort: deterministic vs. randomized (5 trials per condition)')
    fig.tight_layout()
    fig.savefig(output / 'benchmark_chart.png', dpi=180)
    plt.close(fig)
    return results

if __name__ == '__main__':
    run_benchmarks()
