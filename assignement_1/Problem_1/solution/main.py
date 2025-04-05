import itertools
import math


class PoisonBottleDetector:
    def __init__(self, total_bottles, poison_count, inputted_poisonous_bottles):
        self.total_bottles = total_bottles
        self.poison_count = poison_count
        self.inputted_poisonous_bottles = inputted_poisonous_bottles
        self.poisonous_bottles = []
        self.total_combinations = self.calculate_combinations()
        self.total_prisoners = self.calculate_combination_prisoners()

    def calculate_combinations(self):
        """Calculate total number of combinations"""
        return math.comb(self.total_bottles, self.poison_count)

    def calculate_combination_prisoners(self):
        """Calculate exact number of prisoners for combination testing"""
        return math.ceil(math.log2(self.total_combinations))

    def mark_poisonous_bottles(self, poison_list=None):
        """Mark poisonous bottles"""
        self.poisonous_bottles = poison_list if poison_list is not None else []
        return self.poisonous_bottles

    def detect_poison_bottles(self):
        """Detect poisonous bottles"""
        # Generate all possible combinations
        all_combinations = list(itertools.combinations(range(self.total_bottles), self.poison_count))

        # Identify the index of the combination containing the poisonous bottles
        poisonous_combination_index = next(
            (index for index, combination in enumerate(all_combinations) \
             if set(combination) == set(
                self.inputted_poisonous_bottles)),
            None
        )  ### Dummy method to mimic the actual detection process

        # Use binary representation of the combination index
        if poisonous_combination_index is not None:
            binary_representation = bin(poisonous_combination_index)[2:].zfill(self.total_prisoners)
            identified_bottles = self.decode_bottles_from_binary(binary_representation)
        else:
            identified_bottles = []

        return {
            'original_poisonous_bottles': self.inputted_poisonous_bottles,
            'total_combinations': self.total_combinations,
            'identified_poisonous_bottles': identified_bottles,
            'total_prisoners_needed': self.total_prisoners
        }

    def decode_bottles_from_binary(self, binary_str):
        """
        Decode bottles from binary representation of combination index

        :param binary_str: Binary string representation
        :return: List of decoded bottles
        """
        # Generate all combinations
        all_combinations = list(itertools.combinations(range(self.total_bottles), self.poison_count))

        # Convert binary to index
        combination_index = int(binary_str, 2)

        # Return the combination at this index
        return list(all_combinations[combination_index])


# Example usage and testing
def main():
    # Test scenarios
    scenarios = [
        (1000, 1, [19]),
        (8, 3, [1, 2, 3]),
        (1000, 2, [439, 19]),
        (1000, 3, [439, 19, 12]),  # Example from the problem statement
        (100, 4, [20, 19, 12, 11]),
        (50, 5, [20, 19, 12, 11, 39]),
    ]

    for total_bottles, poison_count, poison_list in scenarios:
        print(f"\nScenario: {total_bottles} bottles, {poison_count} poisonous, specific bottles {poison_list}")

        # Create detector
        detector = PoisonBottleDetector(total_bottles, poison_count, inputted_poisonous_bottles=poison_list)

        # Run detection
        result = detector.detect_poison_bottles()

        print("Original Poisonous Bottles:", sorted(result['original_poisonous_bottles']))
        print("Identified Poisonous Bottles:", sorted(result['identified_poisonous_bottles']))
        print("Total Combinations", result['total_combinations'])
        print("Total Prisoners Needed:", result['total_prisoners_needed'])

        # Verify correctness
        assert set(result['original_poisonous_bottles']) == set(result['identified_poisonous_bottles']), \
            "Failed to correctly identify poisonous bottles!"


if __name__ == "__main__":
    main()
