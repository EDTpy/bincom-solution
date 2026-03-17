"""
Bincom ICT Solutions – Python Basic Developer Test
Author : Ogunkanmi Taiwo
Date   : 2026-03-17

Install dependencies:
    pip install psycopg2-binary
"""

import random
import statistics
from collections import Counter

# ──────────────────────────────────────────────
#  COLOUR DATA
# ──────────────────────────────────────────────

WEEKLY_COLORS = {
    "MONDAY":    ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK",
                  "BLUE", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED",
                  "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "TUESDAY":   ["ARSH", "BROWN", "GREEN", "BROWN", "BLUE", "BLUE",
                  "BLEW", "PINK", "PINK", "ORANGE", "ORANGE", "RED",
                  "WHITE", "BLUE", "WHITE", "WHITE", "BLUE", "BLUE", "BLUE"],
    "WEDNESDAY": ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK",
                  "RED", "YELLOW", "ORANGE", "RED", "ORANGE", "RED",
                  "BLUE", "BLUE", "WHITE", "BLUE", "BLUE", "WHITE", "WHITE"],
    "THURSDAY":  ["BLUE", "BLUE", "GREEN", "WHITE", "BLUE", "BROWN",
                  "PINK", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED",
                  "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "FRIDAY":    ["GREEN", "WHITE", "GREEN", "BROWN", "BLUE", "BLUE",
                  "BLACK", "WHITE", "ORANGE", "RED", "RED", "RED",
                  "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "WHITE"],
}

# ──────────────────────────────────────────────
#  COLOR CLEANING
# ──────────────────────────────────────────────

CORRECTIONS = {
    "BLEW":   "BLUE",
    "ARSH":   "ASH",
    "ORAGNE": "ORANGE",
    "GREN":   "GREEN",
    "WHIT":   "WHITE",
    "REED":   "RED",
    "YELOW":  "YELLOW",
    "BROWM":  "BROWN",
}

def clean_color(color: str) -> str:
    """
    Strips whitespace, converts to uppercase, then fixes
    known misspellings using the CORRECTIONS dictionary.
    """
    color = color.strip().upper()
    return CORRECTIONS.get(color, color)   # return corrected or original


def clean_all_colors(weekly: dict) -> dict:
    """Applies clean_color() to every entry in the weekly dict."""
    return {
        day: [clean_color(c) for c in colors]
        for day, colors in weekly.items()
    }


# Apply cleaning before anything else
WEEKLY_COLORS = clean_all_colors(WEEKLY_COLORS)

# ──────────────────────────────────────────────
#  COLOR CLEANING
# ──────────────────────────────────────────────

CORRECTIONS = {
    "BLEW":  "BLUE",
    "ARSH":  "ASH",
    "ORNG":  "ORANGE",
    "GREN":  "GREEN",
    "WHTE":  "WHITE",
    "BRWN":  "BROWN",
    "YELOW": "YELLOW",
    "PURPL": "PURPLE",
    "PNIK":  "PINK",
}

def clean_color(color: str) -> str:
    """
    Strips whitespace, uppercases the color, then checks it
    against the CORRECTIONS dictionary.
    Returns the corrected color name, or the original if no
    correction is needed.
    """
    color = color.strip().upper()
    return CORRECTIONS.get(color, color)   # return fix, or original if clean


# Flatten all colors into one list and clean each one
all_colors = []
for day, day_colors in WEEKLY_COLORS.items():
    for color in day_colors:
        cleaned = clean_color(color)
        if cleaned != color:
            print(f"  [CLEANED] {day}: '{color}' → '{cleaned}'")
        all_colors.append(cleaned)

print()

freq = Counter(all_colors)  # e.g. {"BLUE": 30, "WHITE": 17, ...}

print("=" * 50)
print("  Bincom ICT Solutions")
print("=" * 50)
print(f"\nTotal colour entries : {len(all_colors)}")
print(f"Colour frequencies  : {dict(freq)}")


# ──────────────────────────────────────────────
#  Q1 – Mean colour
#  The mean frequency is the average of all
#  colour counts.  The "mean colour" is the
#  colour whose count is closest to that average.
# ──────────────────────────────────────────────

mean_freq = sum(freq.values()) / len(freq)
mean_colour = min(freq, key=lambda c: abs(freq[c] - mean_freq))

print(f"\n[Q1] Mean frequency : {mean_freq:.2f}")
print(f"     Mean colour    : {mean_colour}  (count = {freq[mean_colour]})")


# ──────────────────────────────────────────────
#  Q2 – Most worn colour (mode)
# ──────────────────────────────────────────────

most_worn = freq.most_common(1)[0]

print(f"\n[Q2] Most worn colour : {most_worn[0]}  (worn {most_worn[1]} times)")


# ──────────────────────────────────────────────
#  Q3 – Median colour
# ──────────────────────────────────────────────

sorted_colors = sorted(all_colors)
median_index  = len(sorted_colors) // 2
median_colour = sorted_colors[median_index]

print(f"\n[Q3] Median colour : {median_colour}")


# ──────────────────────────────────────────────
#  Q4 (BONUS) – Variance of colour frequencies
# ──────────────────────────────────────────────

variance = statistics.variance(list(freq.values()))

print(f"\n[Q4 BONUS] Variance of colour frequencies : {variance:.4f}")


# ──────────────────────────────────────────────
#  Q5 (BONUS) – Probability that a randomly
#               chosen colour is RED
# ──────────────────────────────────────────────

red_count   = freq["RED"]
probability = red_count / len(all_colors)

print(f"\n[Q5 BONUS] P(RED) = {red_count}/{len(all_colors)} = {probability:.4f}")


# ──────────────────────────────────────────────
#  Q6 – Save colours + frequencies to PostgreSQL
#  I used Supabase for my PostgreSQL
# ──────────────────────────────────────────────

DB_URL = "postgresql://postgres.qvzjsuffjrnauflauoup:08165167266Emmy!@aws-1-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require"

def save_to_db():
    try:
        import psycopg2

        conn = psycopg2.connect(DB_URL)
        cur  = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS color_frequency (
                color     VARCHAR(50) PRIMARY KEY,
                frequency INTEGER NOT NULL
            );
        """)

        for color, count in freq.items():
            cur.execute("""
                INSERT INTO color_frequency (color, frequency)
                VALUES (%s, %s)
                ON CONFLICT (color)
                DO UPDATE SET frequency = EXCLUDED.frequency;
            """, (color, count))

        conn.commit()
        cur.close()
        conn.close()
        print("\n[Q6] Colours saved to database successfully!")

    except Exception as e:
        print(f"\n[Q6] Database error: {e}")

save_to_db()


# ──────────────────────────────────────────────
#  Q7 (BONUS) – Recursive binary search
#  The list must be sorted before searching.
# ──────────────────────────────────────────────

def recursive_binary_search(sorted_list, target, low=0, high=None):
    if high is None:
        high = len(sorted_list) - 1
    if low > high:                          # base case: not found
        return -1
    mid = (low + high) // 2
    if sorted_list[mid] == target:
        return mid
    elif sorted_list[mid] < target:
        return recursive_binary_search(sorted_list, target, mid + 1, high)
    else:
        return recursive_binary_search(sorted_list, target, low, mid - 1)

print("\n[Q7 BONUS] Recursive Binary Search")
number_list = sorted([4, 15, 2, 8, 23, 42, 16, 7, 3, 11])
print(f"  List   : {number_list}")
target = int(input("  Enter a number to search for: "))
result = recursive_binary_search(number_list, target)
if result != -1:
    print(f"  Found {target} at index {result}.")
else:
    print(f"  {target} not found in the list.")


# ──────────────────────────────────────────────
#  Q8 – Generate a random 4-digit binary number
#        and convert it to base 10
# ──────────────────────────────────────────────

bits       = [random.choice([0, 1]) for _ in range(4)]
binary_str = "".join(map(str, bits))
decimal    = int(binary_str, 2)

print(f"\n[Q8] Random binary number : {binary_str}")
print(f"     Decimal (base 10)    : {decimal}")


# ──────────────────────────────────────────────
#  Q9 – Sum of the first 50 Fibonacci numbers
# ──────────────────────────────────────────────

a, b = 0, 1
fibs = []
for _ in range(50):
    fibs.append(a)
    a, b = b, a + b

print(f"\n[Q9] Sum of first 50 Fibonacci numbers : {sum(fibs)}")

print("\n" + "=" * 50)
print("  Done!")
print("=" * 50)
