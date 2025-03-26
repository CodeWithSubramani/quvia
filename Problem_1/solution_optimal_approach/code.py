import math


class PoisonBottleDetector:
    def __init__(self, total_bottles, poison_count):
        if poison_count < 0 or poison_count > total_bottles:
            raise ValueError("Invalid number of poisoned bottles")
        self.total_bottles = total_bottles
        self.poison_count = poison_count
        self.poisonous_bottles = []
        self.total_prisoners = self.calculate_prisoners_needed()

    def calculate_prisoners_needed(self):
        """Calculate minimum prisoners using combinatorial encoding"""
        if self.poison_count == 0:
            return 0
        total_combinations = math.comb(self.total_bottles, self.poison_count)
        return max(math.ceil(math.log2(total_combinations)), 1)

    def combination_to_index(self, combo):
        """Convert sorted combination to unique integer index"""
        combo = sorted(combo)
        n, k = self.total_bottles, self.poison_count
        index = 0
        prev = -1
        for i in range(k):
            current = combo[i]
            start = prev + 1
            for j in range(start, current):
                available = n - j - 1
                needed = k - i - 1
                index += math.comb(available, needed)
            prev = current
        return index

    def index_to_combination(self, index):
        """Convert index back to combination of bottles"""
        n, k = self.total_bottles, self.poison_count
        combo = []
        remaining = index
        prev = -1
        for i in range(k):
            j = prev + 1
            while True:
                available = n - j - 1
                needed = k - i - 1
                if available < needed:
                    c = 0
                else:
                    c = math.comb(available, needed)
                if remaining < c:
                    break
                remaining -= c
                j += 1
            combo.append(j)
            prev = j
        return combo

    def detect_poison_bottles(self, poison_list=None):
        """Detect poisonous bottles using combinatorial encoding strategy"""
        if poison_list is None:
            poison_list = []
        original = sorted(poison_list)
        if len(original) != self.poison_count:
            raise ValueError(f"Expected {self.poison_count} poisons, got {len(original)}")

        # Encode combination to index
        index = self.combination_to_index(original)

        # Convert index to binary
        bits_needed = self.total_prisoners
        binary = bin(index)[2:].zfill(bits_needed)

        # Decode binary back to combination
        decoded_index = int(binary, 2)
        identified = self.index_to_combination(decoded_index)

        return {
            'original_poisonous_bottles': original,
            'identified_poisonous_bottles': identified,
            'total_prisoners_needed': self.total_prisoners,
            'prisoner_bits': binary
        }


def main():
    scenarios = [
        (1000, 1, [19]),
        (8, 3, [1, 2, 3]),
        (1000, 2, [439, 19]),
        (1000, 3, [439, 19, 12]),
        (100, 4, [20, 19, 12, 11]),
        (50, 5, [20, 19, 12, 11, 39]),
        (1_000_000, 1, [123456]),
        (1_000_000, 2, [123456, 789012]),
        (1_000_000, 3, [123456, 789012, 345678]),
        (2 ** 20, 5, [1, 2, 3, 4, 5]),
    ]

    for n, k, poisons in scenarios:
        print(f"\nTesting {n:,} bottles, {k} poisons")
        detector = PoisonBottleDetector(n, k)
        try:
            result = detector.detect_poison_bottles(poisons)
            orig = result['original_poisonous_bottles']
            found = result['identified_poisonous_bottles']
            print(f"Prisoners needed: {result['total_prisoners_needed']}")
            print(f"Original: {orig}\nFound:    {found}")
            assert orig == found, "Detection failed!"
            print("Test PASSED")
        except ValueError as e:
            print(f"Invalid scenario: {e}")


if __name__ == "__main__":
    main()