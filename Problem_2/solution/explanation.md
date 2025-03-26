# Algorithm Explanation: Maximum Bandwidth Allocation with Jitter Constraints

## Algorithm Overview
The goal is to find the maximum bandwidth for each traffic type by selecting a subset of links such that:
1. **Jitter** (max latency - min latency in the subset) ≤ traffic type's threshold.
2. **Bandwidth** is maximized for valid subsets.

### Key Steps
1. **Sort Links by Latency**  
   Sort all links in ascending order of latency to enable efficient contiguous subset evaluation.

2. **Compute Prefix Sums**  
   Create a prefix sum array of bandwidths to quickly calculate the sum of any contiguous subset.

3. **Binary Search for Valid Subsets**  
   For each starting index `i` in the sorted links, use binary search to find the farthest valid ending index `j` where:

4. latency[j] - latency[i] ≤ jitter_threshold

The bandwidth for this subset is `prefix_sum[j+1] - prefix_sum[i]`.

4. **Track Maximum Bandwidth**  
Iterate over all possible starting indices and update the maximum bandwidth for each traffic type.

---

## Example Walkthrough
### Input Data
**Links (unsorted):**  
`[(300, 20), (200, 50), (150, 30), (250, 40)]`  
**Jitter Threshold:** `100`

### Step 1: Sort Links by Latency
| Sorted Links (Latency, Bandwidth) | Latency | Bandwidth |
|-----------------------------------|---------|-----------|
| Link 0                            | 150     | 30        |
| Link 1                            | 200     | 50        |
| Link 2                            | 250     | 40        |
| Link 3                            | 300     | 20        |

### Step 2: Compute Prefix Sums

Prefix Sums: [0, 30, 80, 120, 140]


### Step 3: Find Valid Subsets
For **jitter threshold = 100**:

| Start Index | Max Allowed Latency | Valid End Index (Binary Search) | Bandwidth Calculation |
|-------------|---------------------|---------------------------------|-----------------------|
| 0 (150)     | 150 + 100 = 250     | Index 2 (latency = 250)         | 30 + 50 + 40 = 120    |
| 1 (200)     | 200 + 100 = 300     | Index 3 (latency = 300)         | 50 + 40 + 20 = 110    |
| 2 (250)     | 250 + 100 = 350     | Index 3 (latency = 300)         | 40 + 20 = 60          |
| 3 (300)     | 300 + 100 = 400     | Index 3                         | 20                    |

**Maximum Bandwidth = 120** (from subset [Link 0, Link 1, Link 2]).

---

## Complexity Analysis
- **Sorting Links**: `O(N log N)`  
- **Prefix Sums**: `O(N)`  
- **Bandwidth Calculation per Traffic Type**:  
  - For each start index: `O(log N)` (binary search)  
  - Total: `O(N log N)` per traffic type  

**Overall Complexity**: `O(N log N + T * N log N)`  
(where `N` = number of links, `T` = number of traffic types)

Space Complexity
O(N) for storing sorted links, latencies, bandwidths, and prefix sums.

No scalability issues even for N = 1e5.

---

## Key Observations
1. **Optimal Subset** is always a contiguous range in the sorted latency list.
2. **Efficiency** comes from avoiding brute-force checks of all possible subsets.
3. **Edge Cases**:  
   - If no subset satisfies the jitter threshold, bandwidth = 0.  
   - Single-link subsets are always valid (jitter = 0).

---

## Solution Code Highlights
```python
# Sorted links enable contiguous subset checks
sorted_links = sorted(links, key=lambda x: x[0])

# Binary search to find valid endpoint
target = latencies[i] + J
j = bisect.bisect_right(latencies, target) - 1

# Calculate bandwidth using prefix sums
current_sum = prefix_sums[j + 1] - prefix_sums[i]