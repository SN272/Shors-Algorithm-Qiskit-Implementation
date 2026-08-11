from shor_core import run_shor

import csv
from pathlib import Path

N=15
TRIALS = 200
SHOTS = 4096

results = []

print(f"Running {TRIALS} Shor trials for N = {N}")
print("="*50)

for trial in range(1, TRIALS+1):
    result = run_shor(
        N=N,
        shots = SHOTS
    )

    results.append({
        "trial": trial,
        "a": result["a"],
        "gcd": result["gcd"],
        "branch": result["branch"],
        "period": result["period"],
        "factor_1": result["factors"][0] if result["factors"] else "",
        "factor_2": result["factors"][1] if result["factors"] else "",
        "success": result["factors"] is not None
    })

''' print(f"\nTrial {trial}")
    print(f"Base a: {result['a']}")
    print(f"GCD: {result['gcd']}")
    print(f"Branch: {result['branch']}")
    print(f"Period: {result['period']}")
    print(f"Factors: {result['factors']}\n") '''

# SAVE EXPERIMENT RESULTS

results_dir = Path(__file__).resolve().parent.parent / "results"
results_dir.mkdir(exist_ok=True)

output_file = results_dir / "experiment_results.csv"

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "trial",
            "a",
            "gcd",
            "branch",
            "period",
            "factor_1",
            "factor_2",
            "success"
        ]
    )

    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to : {output_file}")