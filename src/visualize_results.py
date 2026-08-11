import csv
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "results" / "experiment_results.csv"

results = []

with open(input_file, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        results.append(row)


#------------------------------------------------------------------------
# PLOT 1 : BASE SELECTION FREQUENCY
#------------------------------------------------------------------------

base_frequency = Counter(
    int(row["a"])
    for row in results
)

bases = sorted(base_frequency.keys())
frequencies = [
    base_frequency[a]
    for a in bases
]


plt.figure(figsize=(9,5))

plt.bar(bases, frequencies)

plt.xlabel("Selected base (a)")
plt.ylabel("Number of Trials")
plt.title("Random Base Selection Across 200 Shor Trials")

plt.xticks(bases)

plt.tight_layout()
base_plot = (
    project_root
    / "results"
    /"base_selection_frequency.png"
)

plt.savefig(base_plot, dpi=300)
plt.show()
print(f"Plot saved to : {base_plot}")

#------------------------------------------------------------------------
# PLOT 2 : QUANTUM PERIOD DISTRIBUTION
#------------------------------------------------------------------------

period_frequency = Counter(
    int(row["period"])
    for row in results
    if row["branch"]=="quantum"
    and row["period"] != ""
)

periods = sorted(period_frequency.keys())

period_counts = [
    period_frequency[period]
    for period in periods
]


plt.figure(figsize=(7,5))

plt.bar(periods, period_counts)

plt.xlabel("Detected Period (r)")
plt.ylabel("Number of Quantum Trials")
plt.title("Detected Period Distribution")

plt.xticks(periods)

plt.tight_layout()

period_plot = (
    project_root
    / "results"
    /"period_distribution.png"
)

plt.savefig(period_plot, dpi=300)
plt.show()
print(f"Plot saved to : {period_plot}")