# Implementation and Demonstration of Shor's Algorithm for Integer Factorization Using Qiskit

## Overview

This project implements and demonstrates the core workflow of Shor's quantum factoring algorithm using Qiskit and Qiskit Aer simulation.

The implementation focuses on integer factorization for `N = 15` and demonstrates the interaction between quantum period finding and classical post-processing.

The project includes:

- Quantum period estimation using the inverse Quantum Fourier Transform
- Reversible modular multiplication
- Controlled modular exponentiation
- Randomized base selection
- Classical GCD-based factor detection
- Classical factor recovery from the detected period
- Controlled quantum measurement experiments
- 200-trial experimental analysis
- Statistical and visual analysis of experimental outcomes
- Reproducible simulation using seeded execution

> **Scope:** This project uses an ideal Qiskit Aer simulator. No noisy hardware simulation or execution on real quantum hardware is included.

---

## Objectives

The main objectives of this project are:

1. Implement the period-finding component of Shor's algorithm using Qiskit.
2. Demonstrate reversible modular multiplication and controlled modular exponentiation for `N = 15`.
3. Estimate the multiplicative period from quantum measurements.
4. Recover non-trivial factors through classical post-processing.
5. Demonstrate both GCD and quantum execution branches.
6. Experimentally evaluate the implementation across randomized trials.
7. Analyze successful and failed factorization attempts.
8. Provide reproducible quantum simulation results.

---

## How It Works

For a selected base `a`, the implementation follows:

~~~text
Randomly select a
       │
       ▼
Calculate gcd(a, N)
       │
       ├── gcd(a, N) > 1
       │       │
       │       ▼
       │   Immediate factor found
       │
       └── gcd(a, N) = 1
               │
               ▼
       Prepare quantum registers
               │
               ▼
       Controlled modular exponentiation
               │
               ▼
       Inverse Quantum Fourier Transform
               │
               ▼
          Measurement
               │
               ▼
        Period estimation
               │
               ▼
       Classical factor recovery
               │
               ▼
          Factorization
~~~

For the quantum branch, the implementation uses a 4-qubit counting register and a 4-qubit work register.

For each counting qubit `j`, the modular multiplier

~~~text
a^(2^j) mod N
~~~

is constructed and applied as a controlled operation.

The inverse QFT is then applied to the counting register. Measurement results are converted into phase estimates and candidate periods are verified using modular arithmetic.

For an even period `r`, classical post-processing attempts to recover factors using:

~~~text
x = a^(r/2) mod N

gcd(x - 1, N)
gcd(x + 1, N)
~~~

---

## Implementation

### Modular Multiplication

A reversible modular multiplication operation is constructed using a unitary matrix:

~~~text
|y> → |a*y mod N>
~~~

for computational basis states satisfying `y < N`.

States outside the modular range are left unchanged so that the operation remains a valid permutation over the complete computational basis.

For `N = 15`, four work qubits provide 16 computational basis states, allowing the operation to be represented as a `16 × 16` unitary matrix.

### Period Estimation

Measured values are converted into phases using:

~~~text
phase = measured_value / 2^counting_qubits
~~~

A rational approximation is obtained using a continued-fraction-based approach through Python's `Fraction.limit_denominator()`.

Candidate periods are then verified by checking:

~~~text
a^r mod N = 1
~~~

### Factor Recovery

When an even period is detected, the implementation calculates:

~~~text
x = a^(r/2) mod N
~~~

and attempts to obtain non-trivial factors through the two GCD operations.

A result is accepted only when both recovered values are non-trivial and smaller than `N`.

---

## Experimental Results

The implementation was evaluated using **200 randomized trials** for:

~~~text
N = 15
~~~

### Summary

| Metric | Result |
|---|---:|
| Total trials | 200 |
| GCD branch | 90 |
| Quantum branch | 110 |
| Successful trials | 186 |
| Failed trials | 14 |
| Overall success rate | 93.00% |
| Quantum branch success rate | 87.27% |
| Detected `r = 2` | 48 |
| Detected `r = 4` | 62 |

The complete experimental dataset is stored in:

~~~text
results/experiment_results.csv
~~~

### Base Selection

The experiment randomly selects bases from:

~~~text
a ∈ {2, 3, 4, ..., 14}
~~~

The observed selection frequencies are analyzed and visualized in:

~~~text
results/base_selection_frequency.png
~~~

### Period Distribution

The detected quantum periods in the 200-trial experiment were:

~~~text
r = 2 → 48 trials
r = 4 → 62 trials
~~~

Visualization:

~~~text
results/period_distribution.png
~~~

### Period vs Base

The relationship between selected base and detected period is visualized in:

~~~text
results/period_vs_base.png
~~~

### Trial-by-Trial Outcomes

The complete sequence of GCD branches, successful quantum outcomes, and quantum failures is visualized in:

~~~text
results/trial_outcomes.png
~~~

### Quantum Measurement Distribution

A separate controlled quantum measurement experiment records the measurement bitstrings, integer values, counts, and probabilities.

The dataset is stored in:

~~~text
results/measurement_results.csv
~~~

and visualized in:

~~~text
results/measurement_distribution.png
~~~

---

## Failure Analysis

The 200-trial experiment produced:

~~~text
14 failed trials
~~~

All 14 failures occurred for:

~~~text
a = 14
~~~

For this base:

~~~text
gcd(14, 15) = 1
~~~

The quantum period-finding procedure successfully detects:

~~~text
r = 2
~~~

However, classical post-processing produces trivial factors rather than two non-trivial factors.

Therefore these trials are recorded as **quantum-branch failures**.

This demonstrates an important property of the factoring procedure:

> Correct period detection does not necessarily guarantee successful factor recovery.

The verified failure trials can be examined directly in:

~~~text
results/experiment_results.csv
~~~

---

## Controlled Demonstration

The project also includes a controlled quantum demonstration using a fixed base.

Example:

~~~text
N = 15
a = 2
gcd(2, 15) = 1
r = 4
15 = 3 × 5
~~~

The measurement distribution for this demonstration is stored in:

~~~text
results/measurement_results.csv
~~~

---

## Reproducibility

The core implementation supports a `seed` parameter.

The seed controls:

- Python's randomized base selection
- Qiskit Aer simulator sampling through `seed_simulator`

Therefore, controlled demonstrations can reproduce the same base selection and quantum measurement counts when the same seed is used.

For example:

~~~python
from src.shor_core import run_shor

result = run_shor(
    N=15,
    base=2,
    seed=42
)

print(result)
~~~

---

## Project Structure

~~~text
Shors-Algorithm-Qiskit/
│
├── results/
│   ├── base_selection_frequency.png
│   ├── experiment_results.csv
│   ├── measurement_distribution.png
│   ├── measurement_results.csv
│   ├── period_distribution.png
│   ├── period_vs_base.png
│   └── trial_outcomes.png
│
├── src/
│   ├── analyze.py
│   ├── experiment.py
│   ├── measurement_demo.py
│   ├── shor_core.py
│   ├── shor_n15.py
│   ├── visualize_measurements.py
│   ├── visualize_results.py
│   └── visualize_trials.py
│
├── .gitignore
├── requirements.txt
└── README.md
~~~

### Main Components

| File | Purpose |
|---|---|
| `shor_core.py` | Core Shor algorithm implementation |
| `shor_n15.py` | Basic N = 15 demonstration |
| `experiment.py` | Runs repeated randomized trials |
| `analyze.py` | Analyzes experimental results |
| `measurement_demo.py` | Controlled quantum measurement demonstration |
| `visualize_results.py` | Generates experimental visualizations |
| `visualize_measurements.py` | Visualizes measurement distributions |
| `visualize_trials.py` | Generates trial-by-trial outcome plot |

---

## Installation

Clone the repository and create a virtual environment:

~~~bash
git clone <repository-url>
cd Shors-Algorithm-Qiskit
~~~

Create and activate the environment.

### Windows

~~~powershell
python -m venv .venv
.venv\Scripts\activate
~~~

### Linux / macOS

~~~bash
python -m venv .venv
source .venv/bin/activate
~~~

Install the dependencies:

~~~bash
pip install -r requirements.txt
~~~

---

## Usage

### Basic N = 15 Demonstration

~~~bash
python src/shor_n15.py
~~~

### Run the Experimental Trials

~~~bash
python src/experiment.py
~~~

### Analyze the Results

~~~bash
python src/analyze.py
~~~

### Run the Controlled Measurement Demonstration

~~~bash
python src/measurement_demo.py
~~~

### Generate Visualizations

~~~bash
python src/visualize_results.py
python src/visualize_measurements.py
python src/visualize_trials.py
~~~

---

## Limitations

This project is an educational and experimental demonstration of Shor's algorithm for the small composite number `N = 15`.

The implementation uses:

- A small fixed register size
- Explicit unitary matrices for modular multiplication
- Qiskit Aer simulation
- Ideal simulated quantum operations

It does not attempt to demonstrate the resource requirements or practical scalability of Shor's algorithm for cryptographically relevant integers.

No noisy quantum simulation or execution on real quantum hardware is included in the current project scope.

---

## Future Work

Possible extensions include:

- Testing larger composite integers
- More general modular arithmetic circuits
- Improved period-estimation methods
- Resource and circuit-depth analysis
- Noisy quantum simulation
- Execution on real quantum hardware
- Comparison of different quantum circuit implementations

---

## Technologies

- Python
- Qiskit
- Qiskit Aer
- NumPy
- Matplotlib
- Git / GitHub

---

## Project Status

**Completed:** Core implementation, controlled demonstrations, 200-trial experimental evaluation, failure analysis, reproducibility testing, and result visualization.

The project is currently being prepared for final technical documentation and academic summer-project reporting.

## Background

This project was developed as a practical implementation following the
completion of Qiskit Global Summer School 2026 training by IBM Quantum, with the objective of applying quantum computing concepts to a complete Shor's algorithm workflow.
