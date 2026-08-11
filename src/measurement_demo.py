import csv
from pathlib import Path
from shor_core import run_shor

N= 15
A =2
SHOTS = 4096

print("="*50)
print("Controlled Quantum Demonstration")
print("="*50)

result = run_shor(
    N=N,
    shots= SHOTS,
    base =A
)
print(f"\nN = {N}")
print(f"Selected base, a = {A}")
print(f"gcd({A}, {N}) = {result['gcd']}")

print(f"\nDetected period: r = {result['period']}")

# Save measurement results
project_root = Path(__file__).resolve().parent.parent

results_dir = project_root / "results"
results_dir.mkdir(exist_ok=True)

output_file = results_dir / "measurement_results.csv"

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "bitstring",
        "measured_value",
        "count",
        "probability"
    ])

    for bitstring, count in sorted(result["counts"].items()):

        measured_value = int(bitstring, 2)
        probability = count / SHOTS

        writer.writerow([
            bitstring,
            measured_value,
            count,
            probability
        ])

print(f"\nMeasurement data saved to: {output_file}")

if result["factors"] is not None:
    factor_1, factor_2 = result["factors"]
    print("\nFactorization :")
    print(f"{N} = {factor_1} x {factor_2}")
else:
    print("\nThis run did not produce non-trivial factors.")