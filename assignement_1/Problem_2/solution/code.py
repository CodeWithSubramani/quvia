import random
import bisect
from typing import List, Tuple


def generate_test_case(num_links: int = 20, num_traffic_types: int = 20) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Generate random links and traffic type jitter thresholds"""
    links = [(random.randint(100, 500), random.randint(10, 100)) for _ in range(num_links)]
    traffic_types = sorted([random.randint(50, 300) for _ in range(num_traffic_types)], reverse=True)
    return links, traffic_types


def max_bandwidth_with_jitter(links: List[Tuple[int, int]], jitter_threshold: int, verbose: bool = False) -> int:
    """
    Calculate maximum bandwidth while respecting jitter constraints

    Args:
        links: List of (latency, bandwidth) tuples
        jitter_threshold: Maximum allowed latency difference
        verbose: Print debug information

    Returns:
        Maximum bandwidth of valid link combinations
    """
    # Sort links by latency
    sorted_links = sorted(links, key=lambda x: x[0])
    latencies = [link[0] for link in sorted_links]
    bandwidths = [link[1] for link in sorted_links]

    # Compute prefix sums for O(1) range sum queries
    prefix_sums = [0] * (len(bandwidths) + 1)
    for i in range(len(bandwidths)):
        prefix_sums[i + 1] = prefix_sums[i] + bandwidths[i]

    max_bw = 0
    best_subset = []

    if verbose:
        print(f"\nEvaluating jitter threshold: {jitter_threshold}")
        print("Sorted Links (Latency, Bandwidth):")
        for i, link in enumerate(sorted_links):
            print(f"Link {i}: {link}")

    # Check all possible contiguous subsets
    for i in range(len(latencies)):
        max_allowed = latencies[i] + jitter_threshold
        j = bisect.bisect_right(latencies, max_allowed) - 1

        current_bw = prefix_sums[j + 1] - prefix_sums[i]
        current_subset = sorted_links[i:j + 1]

        if verbose:
            jitter = latencies[j] - latencies[i] if j > i else 0
            print(f"\nStart at Link {i} (latency {latencies[i]}):")
            print(f"Max allowed latency: {max_allowed} -> Valid through Link {j} (latency {latencies[j]})")
            print(f"Subset Jitter: {jitter} (Threshold: {jitter_threshold})")
            print(f"Subset Bandwidth: {current_bw}")
            print("Links in subset:", current_subset)

        if current_bw > max_bw:
            max_bw = current_bw
            best_subset = current_subset

    if verbose and best_subset:
        actual_jitter = best_subset[-1][0] - best_subset[0][0]
        print(f"\nBest subset for threshold {jitter_threshold}:")
        print(f"Links: {best_subset}")
        print(f"Jitter: {actual_jitter} (<= {jitter_threshold})")
        print(f"Total Bandwidth: {max_bw}")

    return max_bw


def main():
    # Generate test case
    links, traffic_types = generate_test_case()

    print("=== Generated Test Case ===")
    print("\nLinks (Latency, Bandwidth):")
    for i, link in enumerate(links):
        print(f"Link {i + 1}: {link}")

    print("\nTraffic Types (Jitter Thresholds):")
    for i, threshold in enumerate(traffic_types):
        print(f"Traffic Type {i + 1}: {threshold}ms")

    # Evaluate each traffic type
    print("\n=== Bandwidth Allocation Results ===")
    results = []
    for i, threshold in enumerate(traffic_types):
        verbose = (i == 0)  # Show details for first traffic type only
        bw = max_bandwidth_with_jitter(links, threshold, verbose)
        results.append((f"Traffic Type {i + 1}", threshold, bw))
        print(f"Traffic Type {i + 1}: Max BW = {bw} (Jitter <= {threshold}ms)")

    # Print summary table
    print("\n=== Summary ===")
    print("{:<15} {:<20} {:<15}".format("Traffic Type", "Jitter Threshold", "Max Bandwidth"))
    for result in results:
        print("{:<15} {:<20} {:<15}".format(*result))


if __name__ == "__main__":
    main()