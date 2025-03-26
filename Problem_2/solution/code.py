import bisect


def calculate_max_bandwidth(links, jitter_thresholds):
    # Sort the links by their latency
    sorted_links = sorted(links, key=lambda x: x[0])
    latencies = [link[0] for link in sorted_links]
    bandwidths = [link[1] for link in sorted_links]

    # Compute prefix sums of bandwidths
    prefix_sums = [0] * (len(sorted_links) + 1)
    for i in range(len(sorted_links)):
        prefix_sums[i + 1] = prefix_sums[i] + bandwidths[i]

    # Process each jitter threshold to find maximum bandwidth
    results = []
    for J in jitter_thresholds:
        max_bandwidth = 0
        for i in range(len(sorted_links)):
            target = latencies[i] + J
            # Find the rightmost index where latency <= target
            j = bisect.bisect_right(latencies, target) - 1
            if j >= i:
                current_sum = prefix_sums[j + 1] - prefix_sums[i]
                if current_sum > max_bandwidth:
                    max_bandwidth = current_sum
        results.append(max_bandwidth)
    return results


# Example usage with sample data
if __name__ == "__main__":
    import random

    # Generate 20 random links (latency, bandwidth)
    random.seed(42)  # For reproducibility
    links = [(random.randint(50, 500), random.randint(10, 100)) for _ in range(20)]
    # Generate 20 jitter thresholds (e.g., 50, 100, 150, ..., 500)
    jitter_thresholds = [50 * (i + 1) for i in range(20)]

    # Calculate results
    max_bandwidths = calculate_max_bandwidth(links, jitter_thresholds)

    # Print results
    for idx, bw in enumerate(max_bandwidths):
        print(f"Traffic Type {idx + 1} (Jitter ≤ {jitter_thresholds[idx]}): Max Bandwidth = {bw}")