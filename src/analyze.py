import csv
from pathlib import Path
from collections import Counter
from math import gcd

project_root = Path(__file__).resolve().parent.parent
input_file = project_root / "results"/ "experiment_results.csv"

results =[]

with open(input_file, newline="") as file:
    reader= csv.DictReader(file)
    for row in reader:
        results.append(row)

total_trials = len(results)

gcd_trials = sum(
    row["branch"] == "gcd"
    for row in results
)

quantum_trials = sum(
    row["branch"] == "quantum"
    for row in results
)

successful_trials = sum(
    row["success"] =="True"
    for row in results
)

failed_trials = total_trials - successful_trials

successful_quantum_trials = sum(
    row["branch"] == "quantum"
    and row["success"]=="True"
    for row in results
)

periods = Counter(
    int(row["period"])
    for row in results
    if row["period"]
)

base_frequency = Counter(
    int(row["a"])
    for row in results
)

print("\n========== SHOR EXPERIMENT SUMMARY ==========\n")

print(f"Total trials: {total_trials}")

print(f"GCD branch: {gcd_trials}")
print(f"Quantum branch: {quantum_trials}")

print(f"\nSuccessful trials: {successful_trials}")
print(f"Failed trials: {failed_trials}")

print(
    f"\nOverall success rate: "
    f"{successful_trials / total_trials * 100:.2f}%"
)

if quantum_trials:
    print(
        f"Quantum branch success rate: "
        f"{successful_quantum_trials / quantum_trials * 100:.2f}%"
    )

print("\nDetected quantum periods:")

for period, count in sorted(periods.items()):
    print(f"r = {period}: {count} trials")


print("\nBase selection frequency:")

for base, count in sorted(base_frequency.items()):
    print(f"a = {base}: {count} trials")

# ============================================================
# Theoretical reference for N = 15
# ============================================================

print("\n========== THEORETICAL REFERENCE FOR N = 15 ==========")

print(
    f"{'a':>3} | "
    f"{'gcd(a,N)':>8} | "
    f"{'Branch':>8} | "
    f"{'Expected r':>10} | "
    f"{'Expected result':>18}"
)

print("-" * 65)

N = 15

for a in range(2, N):

    common_factor = gcd(a, N)

    if common_factor != 1:

        branch = "GCD"
        expected_period = "-"

        other_factor = N // common_factor

        expected_result = (
            f"{common_factor} x {other_factor}"
        )

    else:

        branch = "Quantum"

        # Calculate multiplicative order
        expected_period = None

        for r in range(1, N):

            if pow(a, r, N) == 1:
                expected_period = r
                break

        # Determine whether classical post-processing
        # produces non-trivial factors
        if expected_period % 2 == 0:

            x = pow(a, expected_period // 2, N)

            factor_1 = gcd(x - 1, N)
            factor_2 = gcd(x + 1, N)

            if (
                factor_1 > 1
                and factor_2 > 1
                and factor_1 < N
                and factor_2 < N
            ):
                expected_result = (
                    f"{factor_1} x {factor_2}"
                )
            else:
                expected_result = "trivial factors"

        else:
            expected_result = "invalid period"

    print(
        f"{a:>3} | "
        f"{common_factor:>8} | "
        f"{branch:>8} | "
        f"{str(expected_period):>10} | "
        f"{expected_result:>18}"
    )