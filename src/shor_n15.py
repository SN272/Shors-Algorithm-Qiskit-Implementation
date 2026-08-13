import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from shor_core import run_shor

N = 15
SHOTS = 4096

result = run_shor(
    N=N,
    shots=SHOTS
)

print(f"N = {result['N']}")
print(f"Randomly selected base, a = {result['a']}")
print(f"gcd({result['a']}, {result['N']}) = {result['gcd']}")

if result["branch"]== "gcd":
    print("\nFactor found immediately:")
    print(
        f"{result['factors'][0]} × "
        f"{result['factors'][1]} = "
        f"{N}"
    )
else:
    print(f"\nDetected period from quantum measurements : "
          f"r = {result['period']}")
    print("\nMeasurement results :")

    for bitstring, count in result["counts"].items():
        print(f"{bitstring} -> {count}")

    if result["factors"] is not None:
        factor_1, factor_2 =  result["factors"]

        print("\nClassical post-processing: ")
        print(f"Factor 1 = {factor_1}")
        print(f"Factor 2 = {factor_2}")

        print(
            f"\nFactorization successful : "
            f"{N} = {factor_1} x {factor_2}"
        )
    else:
        print("\nFactorization was not successful in this trial.")
