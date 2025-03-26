# Poison Bottle Detection Algorithm: A Friendly Guide

## 🤔 What's This Problem All About?

Imagine you have a collection of bottles, and some of them contain poison. Your job is to figure out which ones are
poisoned while using the least number of test subjects (prisoners). Sounds tricky, right? Let's break it down step by
step!

---

## 🎯 The Challenge

- You have `N` total bottles.
- `K` of these bottles are poisoned.
- Goal: Find the poisoned bottles using the **minimum** number of prisoners.

---

## 🔍 Approach 1: Finding a Single Poisoned Bottle

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


## 🔬 Approach 2: Multiple Poisoned Bottles

### 📊 Counting Combinations

**Scenario**: 8 Bottles, 3 Poisoned Bottles

Instead of binary encoding, we now count **all possible combinations** of choosing 3 bottles from 8.

#### How Many Combinations Exist?

- The number of ways to choose 3 poisoned bottles from 8 is:

  **C(8,3) = 8! / (3! * (8-3)!) = (8 × 7 × 6) / (3 × 2 × 1) = 56**

This means we need **at least** `⌈log₂(56)⌉ = 6` prisoners.

#### 👥 Prisoner Strategy

Each prisoner drinks from bottles according to a bit in a binary encoding of the 56 possible combinations.

#### **Which Prisoners Drank from Which Bottles?**

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

**Poisoned bottles:** 4, 5, 7 (part of combo {4,5,7}).

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

#### Unique Signature:

- No other combo has the ID **110110**.