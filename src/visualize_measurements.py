import matplotlib.pyplot as plt
import csv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "results"
    / "measurement_results.csv"
)

output_file = (
    project_root
    /"results"
    /"measurement_distribution.png"
)

measurements =[]

with open(input_file, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        measurements.append({
            "y": int(row["measured_value"]),
            "probability": float(row["probability"])
        })

measurements.sort(key = lambda item: item["y"])

values = [
    item["y"]
    for item in measurements
]

probabilities = [
    item["probability"]
    for item in measurements
]

plt.figure(figsize=(8,5))
plt.bar(values, probabilities)
plt.xlabel("Measured value (y)")
plt.ylabel("Measured probability")
plt.title("Quantum Measurement Distribution for N=15, a=2")
plt.xticks(values)
plt.ylim(0, 0.30)
plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.show()
print(f"Measurement plot saved to : {output_file}")