# Assignment 5: Quicksort Algorithm — Implementation, Analysis, and Randomization

## 1. Introduction and objectives
Quicksort is a divide-and-conquer sorting algorithm. It selects a pivot, partitions the array so elements less than or equal to the pivot are placed to its left and larger elements to its right, and recursively sorts the resulting subarrays. This report implements last-element-pivot (deterministic) and random-pivot (randomized) Quicksort, analyzes their asymptotic complexity, and compares their observed execution times for random, sorted, and reverse-sorted lists. Both implementations sort in place.

## 2. Implementation and design decisions
The Python module `quicksort.py` provides `quicksort(values)` and `randomized_quicksort(values, rng=None)`. Both use Lomuto partitioning: the rightmost element is the active pivot; an index tracks the division between elements less than or equal to the pivot and remaining elements; after a single scan, swapping places the pivot at its final sorted position. The deterministic implementation always uses the last element. The randomized implementation first selects an index uniformly from the current subarray and exchanges its value with the last element; it then uses the same partition function. Optional random-number generator injection permits repeatable trials.

The implementation recursively processes the *smaller* partition and iteratively processes the larger partition. This technique avoids deep Python call stacks even when pivots are highly unbalanced. It does **not** prevent quadratic running time: deterministic selection of the last element still causes highly unequal partitions for already sorted or reverse-sorted unique values. Neither algorithm requires a second full-sized list; both modify the input list and return the same list. The use of `<=` also ensures equal values partition correctly, but all-equal input can lead to quadratic behavior even under randomized pivot selection.

The `test_quicksort.py` unit tests verify empty lists, one-element lists, duplicated values, negative numbers, sorted and reverse-sorted inputs, and other arrays. Both functions matched Python's `sorted` output in these tests.

## 3. Theoretical time and space complexity
**Best case — O(n log n).** If each pivot divides n elements into two roughly equal parts, partitioning costs O(n) at each recursion level and there are O(log n) levels. The recurrence T(n) = 2T(n/2) + O(n) yields O(n log n).

**Average case — expected O(n log n).** For random permutations, even deterministic last-element selection yields sufficiently balanced partitions on average. Randomized pivot selection ensures that each position in the current subarray is equally likely to become the pivot, independently of the original ordering. The expected number of comparisons is O(n log n). One can understand this by summing expected comparison probabilities across pairs of elements: the probability that sorted-order elements i and j are compared equals 2/(j-i+1), giving approximately 2n ln(n) comparisons overall.

**Worst case — O(n²).** If the pivot is always the minimum or maximum, partition sizes are 0 and n-1. The recurrence T(n) = T(n-1) + O(n) accumulates n + (n-1) + ... + 1 = O(n²). Last-element pivot selection exhibits this outcome on sorted and reverse-sorted distinct values. Randomization makes this sequence of bad pivots very unlikely but does not eliminate the possibility, so randomized Quicksort also has O(n²) worst-case time.

**Space complexity and overheads.** Lomuto partitioning uses O(1) auxiliary workspace apart from recursion. Standard recursive Quicksort typically uses O(log n) stack space for balanced splits and can use O(n) for pathologically unbalanced splits. The smaller-side-first recursive implementation here limits stack depth to O(log n) even in the worst case, while continuing the larger range in a loop. Total auxiliary memory is therefore O(log n) for recursion; additional temporary objects and RNG state are constant-sized with respect to n. Python function calls and pivot sampling introduce constant-factor overhead. The algorithms are not stable: equal-key elements can change their relative order.

| Case | Deterministic time | Randomized time | Auxiliary space (this implementation) |
|---|---|---|---|
| Best | O(n log n) | O(n log n) | O(log n) |
| Average / expected | O(n log n) on random inputs | Expected O(n log n) on any fixed distinct-key ordering | O(log n) |
| Worst | O(n²) | O(n²) | O(log n) |

## 4. Experimental methodology
Measurements were performed using Python's `time.perf_counter()` and captured in `benchmark_results.csv`. Five trials were conducted for each algorithm, array size (100, 500, 1,000, 2,000, 4,000), and distribution (random unique integers, sorted increasing integers, reverse-sorted integers). The random datasets use deterministic seeds, and each version sorts a fresh copy of the same input. Dataset generation and copying occur outside the timed portion. Randomized pivot selection is included in the measured sort time. Each result is checked against Python's built-in `sorted`. All measurements are in milliseconds and are environment-specific, so another machine or run may yield different values.

### Observed mean times (ms; 5 trials each)

| Distribution | n | Deterministic | Randomized |
|---|---:|---:|---:|
| Random | 100 | 0.043 | 0.117 |
| Random | 500 | 0.313 | 0.443 |
| Random | 1,000 | 0.826 | 1.066 |
| Random | 2,000 | 1.768 | 2.355 |
| Random | 4,000 | 4.000 | 5.292 |
| Sorted | 100 | 0.290 | 0.075 |
| Sorted | 500 | 8.068 | 0.513 |
| Sorted | 1,000 | 35.667 | 0.987 |
| Sorted | 2,000 | 153.159 | 2.374 |
| Sorted | 4,000 | 656.056 | 4.415 |
| Reverse-sorted | 100 | 0.237 | 0.067 |
| Reverse-sorted | 500 | 5.850 | 0.472 |
| Reverse-sorted | 1,000 | 28.314 | 1.064 |
| Reverse-sorted | 2,000 | 114.179 | 2.229 |
| Reverse-sorted | 4,000 | 466.419 | 4.849 |

See `benchmark_chart.png` for the three distribution-specific curves. The CSV includes mean, median, minimum, and maximum measurements.

## 5. Interpretation and discussion
For random unique elements, both algorithms grew much more slowly than quadratically over these sizes. The deterministic version was faster in this experiment because its partitioning logic has no extra random pivot selection; this does not imply it is robust to structured input. At n = 4,000, the deterministic version took 4.000 ms versus 5.292 ms for the randomized version on random inputs.

For sorted data at n = 4,000, deterministic Quicksort took 656.056 ms while randomized Quicksort took 4.415 ms, a roughly 149-fold gap. The deterministic time also rose sharply as n doubled, as expected from its O(n²) degeneracy on these inputs. For reverse-sorted input at n = 4,000, the deterministic implementation took 466.419 ms compared with 4.849 ms for the randomized one, a roughly 96-fold gap. The randomized implementation maintained far better performance because its pivot was not systematically an extreme element.

These results support the expected time complexity theory but do not prove it. Timing is affected by interpreter overhead, processor load, cache behavior, and the limited number of observations. The chosen arrays also contain unique values; inputs with many duplicates may degrade the selected two-way partitioning approach. A three-way partition or introspective fallback could improve robustness. Python's built-in `sort` is generally preferable in production because it is highly optimized, stable, and engineered to handle many common data patterns.

## 6. Conclusion
Deterministic last-element-pivot Quicksort is straightforward and can be efficient on unsorted random inputs, but it is extremely sensitive to input order. Random pivot selection incurs modest overhead on random inputs yet greatly reduces the likelihood of pathological partitions when data are sorted or reverse-sorted. The measured experiments agree with the theoretical distinction between expected O(n log n) behavior and worst-case O(n²) behavior. Both versions in this submission are in-place, unit-tested, and reproducibly benchmarked.

## References
Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Python Software Foundation. (n.d.). *time — Time access and conversions*. https://docs.python.org/3/library/time.html
