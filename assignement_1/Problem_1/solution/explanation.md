# Poison Bottle Detection Algorithm: Brute Force method


## 🔍 Thinking out loud: Single Poisoned Bottle

### 🧩 The Binary Encoding Magic
**Scenario**: 8 Bottles, 1 Poisoned Bottle

#### Intuition
Think of binary numbers like secret labels for the bottles. Each bottle gets a unique binary number, and each prisoner
drinks from bottles where their respective bit is `1`.

#### **Example: Assigning Binary Numbers to Bottles**
```
Bottle 0: 000 (0 in decimal)
Bottle 1: 001 (1 in decimal)
Bottle 2: 010 (2 in decimal)
Bottle 3: 011 (3 in decimal)
Bottle 4: 100 (4 in decimal)
Bottle 5: 101 (5 in decimal)
Bottle 6: 110 (6 in decimal)
Bottle 7: 111 (7 in decimal)
```

#### 👥 Prisoner Assignment

We need **3 prisoners** because `log₂(8) = 3`.
Each prisoner drinks from bottles where their respective bit is `1`.

| Bottle # | P1 Drinks? | P2 Drinks? | P3 Drinks? |
|----------|------------|------------|------------|
| 0        | ❌ No       | ❌ No       | ❌ No       |
| 1        | ✅ Yes      | ❌ No       | ❌ No       |
| 2        | ❌ No       | ✅ Yes      | ❌ No       |
| 3        | ✅ Yes      | ✅ Yes      | ❌ No       |
| 4        | ❌ No       | ❌ No       | ✅ Yes      |
| 5        | ✅ Yes      | ❌ No       | ✅ Yes      |
| 6        | ❌ No       | ✅ Yes      | ✅ Yes      |
| 7        | ✅ Yes      | ✅ Yes      | ✅ Yes      |

#### 🕵️ Identifying the Poisoned Bottle

If **prisoner 1 and prisoner 3 die, but prisoner 2 survives**, the corresponding binary is **101**, meaning **Bottle 5**
is poisoned.


## 🔬 Actual Problem: Multiple Poisoned Bottles

### 📊 Counting Combinations

**Scenario based illustration**: 8 Bottles, 3 Poisoned Bottles

Instead of binary encoding, we now count **all possible combinations** of choosing 3 bottles from 8 as more than 1 
bottle can be poisoned.

#### How Many Combinations Exist?

- The number of ways to choose 3 poisoned bottles from 8 is:

  **C(8,3) = 8! / (3! * (8-3)!) = (8 × 7 × 6) / (3 × 2 × 1) = 56**

#### Number of Prisoners Required
Let's take n as the number of prisoners required

Since, there are only 2 states (alive or dead), the number of prisoners required is the smallest integer n such that
2^n ≥ 56
=> n ≥ log₂(56)
=> n >= 6
This means we need **at least** `6` prisoners.

Formula is ~= log₂(C(N, K))
#### 👥 Prisoner Strategy

Each prisoner drinks from bottles according to a bit in a binary encoding of the 56 possible combinations

#### **Example table of which Prisoners Drank from Which Bottles?**

| ID  | Bottles Comb | Binary ID | P1 (LSB) | P2  | P3  | P4  | P5  | P6 (MSB) |
|-----|--------------|-----------|----------|-----|-----|-----|-----|----------|
| 1   | {0,1,2}      | 000001    | ✓        | ✗   | ✗   | ✗   | ✗   | ✗        |
| 2   | {0,1,3}      | 000010    | ✗        | ✓   | ✗   | ✗   | ✗   | ✗        |
| 3   | {0,1,4}      | 000011    | ✓        | ✓   | ✗   | ✗   | ✗   | ✗        |
| 4   | {0,1,5}      | 000100    | ✗        | ✗   | ✓   | ✗   | ✗   | ✗        |
| 5   | {0,1,6}      | 000101    | ✓        | ✗   | ✓   | ✗   | ✗   | ✗        |
| 6   | {0,1,7}      | 000110    | ✗        | ✓   | ✓   | ✗   | ✗   | ✗        |
| 7   | {0,2,3}      | 000111    | ✓        | ✓   | ✓   | ✗   | ✗   | ✗        |
| 8   | {0,2,4}      | 001000    | ✗        | ✗   | ✗   | ✓   | ✗   | ✗        |
| 9   | {0,2,5}      | 001001    | ✓        | ✗   | ✗   | ✓   | ✗   | ✗        |
| 10  | {0,2,6}      | 001010    | ✗        | ✓   | ✗   | ✓   | ✗   | ✗        |
| ... | ...          | ...       | ...      | ... | ... | ... | ... | ...      |
| 54  | {4,5,6}      | 110101    | ✓        | ✗   | ✓   | ✗   | ✓   | ✓        |
| 55  | {4,5,7}      | 110110    | ✗        | ✓   | ✓   | ✗   | ✓   | ✓        |
| 56  | {4,6,7}      | 110111    | ✓        | ✓   | ✓   | ✗   | ✓   | ✓        |

### Step 3: Simulate the Test

Let's say **Poisoned bottles:** 4, 5, 7 (part of combo {4,5,7}).

#### Prisoner actions:

- **P6** drinks from {4,5,7} → **dies** (because 4,5,7 are poisoned).
- **P5** drinks from {4,5,7} → **dies**.
- **P3** drinks from {4,5,7} → **dies**.
- **P2** drinks from {4,5,7} → **dies**.
- **P1, P4 ** skip {4,5,7} → **survive**.

**Result:** Only P6, P5, P3 & P2 die.

---
### Step 4: Decode the Result

- **Dead prisoners = 1 bits** → P6, P5, P3, P2.
- **Surviving prisoners = 0 bits** → P1, P4.
- **Binary ID = 110110** (P6 to P1).

**Look up 110110 in the table** → {4,5,7}.

---

### Why This Works

#### Unique Signature is applied to each combination, which can be revered back to the original combination:
- In this case, No other combo has the ID **110110**.
--- 
 ### Problems with this approach:
- This will not scale with the number of bottles and poisoned bottles.
- The number combinations will explode to a very high value.

--- 
### Time Complexity of the problem is:

***O(log(C(N,K))*C(N,K))***
C(N,K) = Combinations of K bottles from N (N choose K)
K = Number of poisoned bottles

***Breakdown:***

1. Generating all combinations: O(C(N,K))
2. Creating binary mappings for each combination: O(log(C(N,K)))
   - Reason: TC is O(log(N)) for binary encoding of N
    ```shell
    Example:
    N = 8
    To get binary of 8 we divide it by 3 times
    8/2 = 4, remainder = 0
    4/2 = 2, remainder = 0
    2/2 = 1, remainder = 0
    As 1 is less than 2, 1 is considered as the remainder:
    This can be mathematically represented as:
    log₂(8) = 3
    ```
3. Lookup during decoding: O(1) with perfect hashing

--- Space Complexity of the problem is:
***O(C(N,K))***
As this will store all the combinations of K bottles from N bottles in a hashMap.
