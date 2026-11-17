"""
Assignment 1: Minimum Edit Distance using Dynamic Programming
Student Name: Essam Badwy Arafa
University ID: 202310070

Costs: insertion = 1, deletion = 1, substitution = 2.
Includes a DP table, traceback alignment, spelling correction,
and a string-alignment demonstration.
"""

INSERTION_COST = 1
DELETION_COST = 1
SUBSTITUTION_COST = 2


def minimum_edit_distance(source, target):
    rows, cols = len(source) + 1, len(target) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i * DELETION_COST
    for j in range(cols):
        dp[0][j] = j * INSERTION_COST

    for i in range(1, rows):
        for j in range(1, cols):
            substitution = dp[i - 1][j - 1]
            if source[i - 1] != target[j - 1]:
                substitution += SUBSTITUTION_COST

            insertion = dp[i][j - 1] + INSERTION_COST
            deletion = dp[i - 1][j] + DELETION_COST
            dp[i][j] = min(insertion, deletion, substitution)

    return dp, dp[-1][-1]


def print_dp_table(source, target, dp):
    column_labels = ["-"] + list(target)
    row_labels = ["-"] + list(source)
    width = 4
    print("\\nDP TABLE")
    print(" " * 5 + "".join(f"{label:>{width}}" for label in column_labels))
    for label, row in zip(row_labels, dp):
        print(f"{label:>3}  " + "".join(f"{value:>{width}}" for value in row))


def get_alignment(source, target, dp):
    i, j = len(source), len(target)
    left, right, operations = [], [], []

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if source[i - 1] == target[j - 1] else SUBSTITUTION_COST
            if dp[i][j] == dp[i - 1][j - 1] + cost:
                left.append(source[i - 1])
                right.append(target[j - 1])
                operations.append("Match" if cost == 0 else "Substitution")
                i -= 1
                j -= 1
                continue

        if j > 0 and dp[i][j] == dp[i][j - 1] + INSERTION_COST:
            left.append("-")
            right.append(target[j - 1])
            operations.append("Insertion")
            j -= 1
        else:
            left.append(source[i - 1])
            right.append("-")
            operations.append("Deletion")
            i -= 1

    return "".join(reversed(left)), "".join(reversed(right)), list(reversed(operations))


def correct_spelling(word, vocabulary):
    best_word, best_distance = None, float("inf")
    for candidate in vocabulary:
        _, distance = minimum_edit_distance(word, candidate)
        if distance < best_distance:
            best_word, best_distance = candidate, distance
    return best_word, best_distance


def main():
    source, target = "sunday", "saturday"
    dp, distance = minimum_edit_distance(source, target)

    print("Source:", source)
    print("Target:", target)
    print_dp_table(source, target, dp)
    print("\\nMinimum edit distance =", distance)

    aligned_source, aligned_target, operations = get_alignment(source, target, dp)
    print("\\nSTRING ALIGNMENT")
    print(aligned_source)
    print(aligned_target)
    print("Operations:", " -> ".join(operations))

    vocabulary = ["saturday", "sunday", "someday", "holiday"]
    misspelled = "saturdya"
    suggestion, cost = correct_spelling(misspelled, vocabulary)
    print("\\nSPELLING CORRECTION")
    print("Misspelled word:", misspelled)
    print("Suggested word:", suggestion)
    print("Edit distance:", cost)


if __name__ == "__main__":
    main()
