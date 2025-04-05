# Problem 2: Traffic Type Bandwidth Allocation with Jitter Constraints

## Problem Setting

You are given:
- **20 traffic types**, each with a **maximum tolerable jitter limit** (e.g., 50, 100, 200, etc.).
- **20 links**, each characterized by a `(latency, bandwidth)` tuple (e.g., `(200, 50)` where 200 is latency and 50 is bandwidth).

### Jitter Calculation
When traffic flows through multiple links, the observed jitter is computed as:
Jitter = max(Latencies) - min(Latencies)


### Allocation Rules
- If the calculated jitter **exceeds** the traffic type's maximum tolerable limit, the links **cannot be combined**.
- Otherwise, the **serviced bandwidth** is the sum of the individual link bandwidths.

### Example
Consider two links with latencies `(200, 50)` and `(300, 20)`:
- **Jitter** = `max(200, 300) - min(200, 300) = 100`
- If the traffic type's **jitter limit** is `120`, the allocation is allowed, and the **total bandwidth** = `50 + 20 = 70`.

## Task
Write a Python program to:
1. Handle **20 traffic types** (each with unique jitter thresholds) and **20 links** (with randomized latencies).
2. **Maximize the allocatable bandwidth** for each traffic type while respecting its jitter constraint.

### Deliverables
1. **Algorithm Documentation**: Explain your approach (e.g., brute-force, dynamic programming, greedy heuristics).
2. **Python Code**: Submit the code separately with your email.

## Scoring Criteria
Your solution will be evaluated based on:
- **Efficiency** of the algorithm (time/space complexity).
- Correctness and scalability for larger inputs.