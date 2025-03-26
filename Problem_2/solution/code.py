import bisect
import random


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


# Example usage with detailed printing
if __name__ == "__main__":
    # Generate test data
    random.seed(42)  # Fixed seed for reproducibility
    links = [(random.randint(50, 500), random.randint(10, 100)) for _ in range(20)]
    jitter_thresholds = [50 * (i + 1) for i in range(20)]

    # Print input details
    print("=" * 50 + "\nINPUT DETAILS\n" + "=" * 50)
    print("\n=== LINKS ===")
    for idx, (latency, bw) in enumerate(links):
        print(f"Link {idx + 1:2}: Latency = {latency:4}ms, Bandwidth = {bw:3} Mbps")

    print("\n=== TRAFFIC TYPES ===")
    for idx, threshold in enumerate(jitter_thresholds):
        print(f"Traffic Type {idx + 1:2}: Max Jitter = {threshold:4}ms")

    # Calculate results
    print("\n" + "=" * 50 + "\nPROCESSING\n" + "=" * 50)
    print("1. Sorting links by latency...")
    sorted_links = sorted(links, key=lambda x: x[0])
    print("2. Calculating prefix sums for bandwidth...")

    # Perform calculation
    print("3. Finding maximum bandwidth for each traffic type:")
    max_bandwidths = calculate_max_bandwidth(links, jitter_thresholds)

    # Print final results
    print("\n" + "=" * 50 + "\nRESULTS\n" + "=" * 50)
    for idx, (threshold, bw) in enumerate(zip(jitter_thresholds, max_bandwidths)):
        print(f"Traffic Type {idx + 1:2} (Jitter ≤ {threshold:4}ms): " +
              f"Max Bandwidth = {bw:4} Mbps")

    # Print explanation
    print("\n" + "=" * 50 + "\nINTERPRETATION\n" + "=" * 50)
    print("For each traffic type (with different jitter tolerance):")
    print("- We find the largest group of consecutive low-latency links")
    print("- Where (max latency - min latency) ≤ the jitter limit")
    print("- Sum their bandwidths to get the maximum possible bandwidth")