from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate, QFTGate
from qiskit_aer import AerSimulator

import numpy as np
import random

from math import gcd
from fractions import Fraction

# MODULAR MULTIPLICATION FUNCTION
def modular_multiplication_gate(a, N, num_qubits):
    #Reversible modular multiplication gate
    """
    Construct a reversible modular multiplication gate implementing
    |y> -> |a*y mod N> for y < N and leaving unused states unchanged.
    """
    dimension = 2 ** num_qubits
    matrix = np.zeros((dimension,dimension))

    for y in range(dimension):
        if y<N:
            new_y = (a*y) % N
        else:
            new_y = y
        matrix[new_y, y] =1
    return UnitaryGate(matrix, label=f"x{a} mod {N}")

# PERIOD ESTIMATION
def estimate_period_from_measurement(measured_value, counting_qubits, a, N):
    """
    Estimate and verify the multiplicative period from a measured
    phase value obtained from the inverse QFT.
    """

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

# RANDOM BASE SELECTION
def choose_random_base(N):
    """
    Randomly select a candidate base a from the range 2 <= a < N.
    """
    return random.randint(2, N-1)

# MAIN FUNCTION (RUN SHOR ALGORITHM)
def run_shor(N=15, shots=4096, seed=None, base=None):
    """
    Execute the Shor factorization demonstration.

    The algorithm first checks gcd(a, N) for an immediate factor.
    If gcd(a, N) = 1, it performs quantum period finding and then
    applies classical post-processing to recover non-trivial factors.

    Returns:
        dict: N, selected base, gcd, detected period, factors,
              measurement counts, and execution branch.
    """

    if seed is not None:
        random.seed(seed)

    if base is None:
        a = choose_random_base(N)
    else:
        a=base
    if not(1<a<N):
        raise ValueError("Base a must satisfy 1 < a < N.")
    common_factor = gcd(a,N)

    if common_factor > 1: #Immediate factor found
        return {
            "N" : N,
            "a" : a,
            "gcd" : common_factor,
            "period": None,
            "factors": (common_factor, N//common_factor),
            "counts": {},
            "branch": "gcd"
        }

   # CREATE QUANTUM CIRCUIT FOR gcd(a, N) = 1
    counting_qubits = 4
    work_qubits = 4

    qc = QuantumCircuit(
        counting_qubits + work_qubits, 
        counting_qubits
    )

    # SUPERPOSITION
    for qubit in range(counting_qubits):
        qc.h(qubit)

    # INITIALIZE WORK REGISTER TO |1>
    qc.x(counting_qubits)

    # CONTROLLED MODULAR EXPONENTIATION
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

    # INVERSE QUANTUM FOURIER TRANSFORM
    inverse_qft = QFTGate(counting_qubits).inverse()
    qc.append(
        inverse_qft,
        range(counting_qubits)
    )

    # MEASURE COUNTING REGISTER
    qc.measure(
        range(counting_qubits),
        range(counting_qubits)
    )

    # SIMULATE WITH QISKIT AER
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator)

    if seed is not None:
        job = simulator.run(
            transpiled_qc, 
            shots=shots,
            seed_simulator=seed
        )
    else:
        job = simulator.run(
            transpiled_qc,
            shots=shots
        )

    result = job.result()
    counts = result.get_counts()

    # EXTRACT THE QUANTUM PERIOD
    period_candidates = []
    for bitstring, count in counts.items():
        measured_value = int(bitstring, 2)
        period_estimate = estimate_period_from_measurement(
            measured_value,
            counting_qubits,
            a,
            N
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

    # RECOVER FACTORS
    factors = None
    if period is not None and period %2 == 0:
        x = pow(a, period//2, N)
        factor_1 = gcd(x-1, N)
        factor_2 = gcd(x+1, N)

        if (
            factor_1 > 1 
            and factor_2 > 1
            and factor_1 < N
            and factor_2 < N
        ):
            factors = (factor_1, factor_2)


    # FINAL RESULT
    return {
        "N" : N,
        "a" : a,
        "gcd" : common_factor,
        "period" : period,
        "factors" : factors,
        "counts" : counts,
        "branch" : "quantum"
    }