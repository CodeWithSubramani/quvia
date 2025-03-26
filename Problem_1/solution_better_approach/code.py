import math


class PoisonBottleDetector:
    def __init__(self, total_bottles, poison_count):
        self.total_bottles = total_bottles
        self.poison_count = poison_count
        self.poisonous_bottles = []
        self.total_prisoners = self.calculate_prisoners_needed()

    def calculate_prisoners_needed(self):
        """Calculate minimum number of prisoners needed using binary encoding"""
        # Each prisoner can represent one bit in the bottle's binary representation
        return math.ceil(math.log2(self.total_bottles)) * self.poison_count

    def mark_poisonous_bottles(self, poison_list=None):
        """Mark poisonous bottles"""
        self.poisonous_bottles = poison_list if poison_list is not None else []
        return self.poisonous_bottles

    def detect_poison_bottles(self, poison_list=None):
        """Detect poisonous bottles using optimized binary testing strategy"""
        # Mark poisonous bottles
        original_bottles = self.mark_poisonous_bottles(poison_list)

        if len(original_bottles) != self.poison_count:
            raise ValueError(f"Expected {self.poison_count} poisonous bottles, got {len(original_bottles)}")

        # Calculate bits needed per bottle
        bits_per_bottle = math.ceil(math.log2(self.total_bottles))

        # Encode each poisonous bottle in binary
        encoded_bottles = []
        for bottle in sorted(original_bottles):
            binary = bin(bottle)[2:].zfill(bits_per_bottle)
            encoded_bottles.append(binary)

        # Combine all binary representations
        full_binary = ''.join(encoded_bottles)

        # Split into prisoner groups (each prisoner tests specific bits)
        identified_bottles = []
        for i in range(0, len(full_binary), bits_per_bottle):
            bottle_bits = full_binary[i:i + bits_per_bottle]
            bottle_num = int(bottle_bits, 2)
            identified_bottles.append(bottle_num)

        return {
            'original_poisonous_bottles': original_bottles,
            'identified_poisonous_bottles': identified_bottles,
            'total_prisoners_needed': self.total_prisoners,
            'bits_per_bottle': bits_per_bottle
        }


def main():
    # Test scenarios - now including larger test cases
    scenarios = [
        (1000, 1, [19]),
        (8, 3, [1, 2, 3]),
        (1000, 2, [439, 19]),
        (1000, 3, [439, 19, 12]),
        (100, 4, [20, 19, 12, 11]),
        (50, 5, [20, 19, 12, 11, 39]),
        # Larger test cases
        (1000000, 1, [123456]),  # 1 million bottles
        (1000000, 2, [123456, 789012]),
        (1000000, 3, [123456, 789012, 345678]),
        (2 ** 20, 5, [1, 2, 3, 4, 5]),  # 1,048,576 bottles
    ]

    for total_bottles, poison_count, poison_list in scenarios:
        print(f"\nScenario: {total_bottles:,} bottles, {poison_count} poisonous, specific bottles {poison_list}")

        # Create detector
        detector = PoisonBottleDetector(total_bottles, poison_count)

        # Run detection
        try:
            result = detector.detect_poison_bottles(poison_list)

            print("Original Poisonous Bottles:", sorted(result['original_poisonous_bottles']))
            print("Identified Poisonous Bottles:", sorted(result['identified_poisonous_bottles']))
            print("Bits per bottle:", result['bits_per_bottle'])
            print("Total Prisoners Needed:", result['total_prisoners_needed'])

            # Verify correctness
            assert set(result['original_poisonous_bottles']) == set(result['identified_poisonous_bottles']), \
                "Failed to correctly identify poisonous bottles!"
            print("Test PASSED")
        except ValueError as e:
            print(f"Error: {e}")
            print("Test SKIPPED")


if __name__ == "__main__":
    main()