

# Algorithm Explanation: Maximum Bandwidth Allocation with Jitter Constraints

## Algorithm Overview
This algorithm calculates the maximum bandwidth for each traffic type by:
1. Evaluating all possible link combinations
2. Calculating actual jitter between each link pair (max latency - min latency)
3. Selecting combinations where jitter ≤ threshold
4. Choosing the combination with maximum bandwidth


## Example Walkthrough

### Input Data
**Links (unsorted):**  
`[(300, 20), (200, 50), (150, 30), (250, 40)]`  
**Jitter Threshold:** `100`

### Step 1: Sort Links by Latency
| Link Index | Latency | Bandwidth |
|------------|---------|-----------|
| 0          | 150     | 30        |
| 1          | 200     | 50        |
| 2          | 250     | 40        |
| 3          | 300     | 20        |

### Step 2: Compute Prefix Sums
Prefix Sums: [0, 30, 80, 120, 140]

### Step 3: Evaluate Valid Subsets with Jitter Calculation

| Subset Range | Links            | Jitter Calculation | Valid? | Bandwidth |
|--------------|------------------|--------------------|--------|-----------|
| [0]          | [150]            | 0 (single link)    | Yes    | 30        |
| [0-1]        | [150, 200]       | 200-150 = 50       | Yes    | 80        |
| [0-2]        | [150, 200, 250]  | 250-150 = 100      | Yes    | 120       |
| [0-3]        | [150, 200, 250, 300] | 300-150 = 150   | No     | -         |
| [1-2]        | [200, 250]       | 250-200 = 50       | Yes    | 90        |
| [1-3]        | [200, 250, 300]  | 300-200 = 100      | Yes    | 110       |
| [2-3]        | [250, 300]       | 300-250 = 50       | Yes    | 60        |

**Maximum Valid Bandwidth = 120** (from subset [150, 200, 250])

### Step 4: Optimized Implementation (Binary Search)
For each starting index i:
1. Binary search for largest j where latency[j] - latency[i] ≤ threshold
2. Calculate bandwidth as prefix_sum[j+1] - prefix_sum[i]

## Complexity Analysis
- **Sorting:** O(N log N)
- **Prefix Sums:** O(N)
- **Binary Search per Start Index:** O(log N)
- **Total:** O(N log N) per traffic type
