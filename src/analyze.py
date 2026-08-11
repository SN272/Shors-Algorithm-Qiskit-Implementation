import csv
from pathlib import Path
from collections import Counter

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