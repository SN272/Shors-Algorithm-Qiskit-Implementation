from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate, QFTGate
import numpy as np


def modular_multiplication_gate(a, N, num_qubits):
    """Construct the reversible modular multiplication gate."""
    dimension = 2 ** num_qubits
    matrix = np.zeros((dimension, dimension))

    for y in range(dimension):
        if y < N:
            new_y = (a * y) % N
        else:
            new_y = y

        matrix[new_y, y] = 1

    return UnitaryGate(matrix, label=f"x{a} mod {N}")


# Fixed demonstration configuration
N = 15
a = 2

counting_qubits = 4
work_qubits = 4

qc = QuantumCircuit(
    counting_qubits + work_qubits,
    counting_qubits
)

# Superposition
for qubit in range(counting_qubits):
    qc.h(qubit)

# Initialize work register to |1>
qc.x(counting_qubits)

# Controlled modular exponentiation
for j in range(counting_qubits):
    multiplier = pow(a, 2 ** j, N)

    gate = modular_multiplication_gate(
        multiplier,
        N,
        work_qubits
    )

    controlled_gate = gate.control(1)

    qc.append(
        controlled_gate,
        [j] + list(
            range(
                counting_qubits,
                counting_qubits + work_qubits
            )
        )
    )

# Inverse Quantum Fourier Transform
inverse_qft = QFTGate(counting_qubits).inverse()

qc.append(
    inverse_qft,
    range(counting_qubits)
)

# Measurement
qc.measure(
    range(counting_qubits),
    range(counting_qubits)
)

# Display circuit
print(qc.draw(output="text"))

# Save circuit image
output_file = "results/shor_circuit_n15_a2.png"

qc.draw(
    output="mpl",
    filename=output_file
)

print(f"\nCircuit diagram saved to: {output_file}")