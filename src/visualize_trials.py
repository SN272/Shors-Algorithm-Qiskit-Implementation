import csv
from pathlib import Path
import matplotlib.pyplot as plt

#-----------------------------------------------------------------
# FILE PATHS
#-----------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "results"
    / "experiment_results.csv"
)

output_file =(
    project_root
    / "results"
    /"trial_outcomes.png"
)

#--------------------------------------------------------------------
# READ EXPERIMENTAL DATA
#--------------------------------------------------------------------

trials = []
with open(input_file, newline="")as file:
    reader = csv.DictReader(file)
    for row in reader:
        trial = int(row["trial"])
        branch = row["branch"]
        period = row["period"]
        factor_1 = row["factor_1"]
        factor_2 = row["factor_2"]

        # Determine experimental outcome
        if branch == "gcd":
            outcome = 0

        elif branch == "quantum" and (factor_1 == "" or factor_2 == ""):
            outcome = -1

        elif branch == "quantum" and period == "2":
            outcome = 2

        elif branch == "quantum" and period == "4":
            outcome = 4

        else:
            outcome = -1

        trials.append({
            "trial": trial,
            "outcome": outcome
        })


# ------------------------------------------------------------
# Plot trial-by-trial outcomes
# ------------------------------------------------------------

trial_numbers = [
    item["trial"]
    for item in trials
]

outcomes = [
    item["outcome"]
    for item in trials
]


plt.figure(figsize=(12, 6))

plt.plot(
    trial_numbers,
    outcomes,
    marker="o",
    linewidth=1
)


# ------------------------------------------------------------
# Labels
# ------------------------------------------------------------

plt.xlabel("Trial number")

plt.ylabel("Experimental outcome")

plt.title(
    "Trial-by-Trial Outcomes of 200 Shor Algorithm Runs for N = 15"
)

plt.yticks(
    [-1, 0, 2, 4],
    [
        "Quantum failure",
        "GCD branch",
        "Quantum: r = 2",
        "Quantum: r = 4"
    ]
)

plt.xticks(range(0, len(trials) + 1, 20))

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()


# ------------------------------------------------------------
# Save figure
# ------------------------------------------------------------

plt.savefig(
    output_file,
    dpi=300
)

plt.show()

print(f"Trial outcome plot saved to: {output_file}")