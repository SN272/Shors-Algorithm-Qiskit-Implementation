from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate, QFTGate
from qiskit_aer import AerSimulator
import numpy as np
from math import gcd
from fractions import Fraction

#--------------------Quantum Part---------------------
def modular_multiplication_gate(a, N, num_qubits):
    #Reversible modular multiplication gate
    dimension = 2 ** num_qubits
    matrix = np.zeros((dimension,dimension))

    for y in range(dimension):
        if y<N:
            new_y = (a*y) % N
        else:
            new_y = y
        matrix[new_y, y] =1
    return UnitaryGate(matrix, label=f"x{a} mod {N}")

def estimate_period_from_measurement(measured_value, counting_qubits, a, N):
    #Estimate n verfiy period from a quantum measurement

    #Zero measurement provides no useful phase info
    if measured_value == 0:
        return None
    
    phase = measured_value / (2 ** counting_qubits)
    fraction = Fraction(phase).limit_denominator(N)
    candidate = fraction.denominator

    #Verify candidate period
    if candidate>0 and pow(a, candidate, N)==1:
        return candidate
    
    #Try small multiples of candidates
    for multiple in range(2,N):
        possible_period = candidate* multiple

        if possible_period >= N:
            break
        if pow(a, possible_period, N) ==1:
            return possible_period
    return None

#------------Classical Part-------------

def modular_exponentiation(a,x, N):
    return pow(a, x, N)

def find_period_classically(a, N):
    value=1
    for r in range(1, N):
        value = (value * a) % N
        if value == 1:
            return r
    return None

def choose_base(N):
    for a in range(2, N):
        common_factor = gcd(a,N)

        if common_factor == 1:
            return a
    return None

N=15
a= choose_base(N)

print(f"N = {N}")
print(f"Selected base, a = {a}")
print(f"gcd({a}, {N}) = {gcd(a,N)}")

period = find_period_classically(a, N)

print(f"Classical period, r = {period}")

print("\nModular Exponentiation sequence :")

for x in range(period):
    result = modular_exponentiation(a,x,N)
    print(f"{a}^{x} mod {N} = {result}")

# ---------Quantum Part-----------------------

counting_qubits = 4
work_qubits = 4

qc = QuantumCircuit(counting_qubits + work_qubits, counting_qubits)
print("\nQuantum Circuit created: ")
print(qc)

#equal superposition in counting register
for qubit in range(counting_qubits):
    qc.h(qubit)

#Initialize work reg to |1> (ket - column vector)
qc.x(counting_qubits)


print("\nQuantum circuit after work register initialization: ")
print(qc)


#Test modular multiplication gate
mod_mult_gate = modular_multiplication_gate(a, N, work_qubits)
matrix = mod_mult_gate.to_matrix()
identity = np.eye(2 ** work_qubits)
is_unitary = np.allclose(matrix.conj().T @ matrix, identity)

print("\nModular multiplication gate:")
print(mod_mult_gate)

print(f"Is the gate unitary? {is_unitary}")

#Controlled modular multiplication ggates
for j in range(counting_qubits):
    multiplier = pow(a, 2**j, N)
    gate = modular_multiplication_gate(
        multiplier,
        N,
        work_qubits
    )
    controlled_gate = gate.control(1)

    qc.append(
        controlled_gate,
        [j] + list(range(counting_qubits, counting_qubits+work_qubits))
    )

#InverseQuantum Fourier Transform
inverse_qft = QFTGate(counting_qubits).inverse()
qc.append(
    inverse_qft,
    range(counting_qubits)
)

#Measure counting registers
qc.measure(
    range(counting_qubits),
    range(counting_qubits)
)

#Run on Aer simulator
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)
job = simulator.run(transpiled_qc, shots=4096)
result = job.result()
counts = result.get_counts()


print("\nPeriod Estimation :")
period_candidates = []
for bitstring, count in counts.items():
    measured_value = int(bitstring, 2)
    period_estimate = estimate_period_from_measurement(
        measured_value,
        counting_qubits,
        a,
        N
    )

    print(
        f"{bitstring} -> "
        f"y = {measured_value},"
        f"estimated period = {period_estimate}"
    )
    if period_estimate is not None:
        period_candidates.append(period_estimate)

if period_candidates:
    period = max(
        set(period_candidates),
        key = period_candidates.count
    )
else:
    period = None

print(f"\nDetected period fromquantum measurements : r = {period}")

#Classical post-processing to recover factors
if period is not None and period %2 == 0:
    x = pow(a, period//2, N)
    factor_1 = gcd(x-1, N)
    factor_2 = gcd(x+1, N)

    print("\nClassical post-processing:")
    print(f"a^(r/2) mod N = {x}")
    print(f"Factor 1 = gcd({x} - 1, {N}) = {factor_1}")
    print(f"Factor 2 = gcd({x} + 1, {N}) = {factor_2}")

    if factor_1 > 1 and factor_2 > 1:
        print(f"\nFactorization successful: {N} = {factor_1} × {factor_2}")

print("\nMeasurement results :")
print(counts)

#print("\nFinal Shor circuit: ")
#print(qc)