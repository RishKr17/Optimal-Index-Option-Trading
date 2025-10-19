from dataclasses import dataclass
from typing import Dict, Literal, Optional
import math
import numpy as np

OptionType = Literal["call", "put"]
ExerciseType = Literal["european", "american"]

@dataclass
class PriceResult:
    price: float
    early_ex_boundary: Dict[int, float]
    S_tree: np.ndarray
    V_tree: np.ndarray
    exercise_mask: np.ndarray
    params: dict

def crr_binomial_pricer(
    S0: float, K: float, r: float, q: float, sigma: float, T: float, N: int,
    option_type: OptionType = "put", exercise: ExerciseType = "american",
    tol_exercise: float = 1e-12
) -> PriceResult:
    if N < 1: raise ValueError("N must be >= 1")
    if S0 <= 0 or K <= 0: raise ValueError("S0 and K must be > 0")
    if sigma <= 0 or T <= 0: raise ValueError("sigma and T must be > 0")

    dt = T / N
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    p = (math.exp((r - q) * dt) - d) / (u - d)
    if not (0.0 < p < 1.0):
        raise ValueError(f"Risk-neutral p out of (0,1): {p:.6f}. Increase N or check inputs.")

    S_tree = np.full((N + 1, N + 1), np.nan)
    V_tree = np.full((N + 1, N + 1), np.nan)
    exercise_mask = np.zeros((N + 1, N + 1), dtype=bool)

    S_tree[0, 0] = S0
    for i in range(1, N + 1):
        S_tree[i, 0] = S_tree[i - 1, 0] * d
        for j in range(1, i + 1):
            S_tree[i, j] = S_tree[i - 1, j - 1] * u

    if option_type == "call":
        V_tree[N, :N+1] = np.maximum(S_tree[N, :N+1] - K, 0.0)
    else:
        V_tree[N, :N+1] = np.maximum(K - S_tree[N, :N+1], 0.0)

    for i in reversed(range(N)):
        for j in range(i + 1):
            continuation = disc * (p * V_tree[i + 1, j + 1] + (1 - p) * V_tree[i + 1, j])

            exercise_val = (S_tree[i, j] - K) if option_type == "call" else (K - S_tree[i, j])
            exercise_val = max(exercise_val, 0.0)

            if exercise == "american":
                if exercise_val > continuation + tol_exercise:
                    V_tree[i, j] = exercise_val
                    exercise_mask[i, j] = True
                else:
                    V_tree[i, j] = continuation
            else:
                V_tree[i, j] = continuation

    boundary: Dict[int, float] = {}
    if exercise == "american":
        for i in range(N):
            row_ex = exercise_mask[i, :i+1]
            if not np.any(row_ex): continue
            S_row = S_tree[i, :i+1]
            if option_type == "put":
                idx = np.where(row_ex)[0]
                j_star = int(np.max(idx))
                if j_star < i:
                    boundary[i] = 0.5 * (S_row[j_star] + S_row[j_star + 1])
                else:
                    boundary[i] = S_row[j_star]
            else:
                idx = np.where(row_ex)[0]
                j_star = int(np.min(idx))
                if j_star > 0:
                    boundary[i] = 0.5 * (S_row[j_star - 1] + S_row[j_star])
                else:
                    boundary[i] = S_row[j_star]

    return PriceResult(
        price=float(V_tree[0, 0]),
        early_ex_boundary=boundary,
        S_tree=S_tree, V_tree=V_tree, exercise_mask=exercise_mask,
        params=dict(S0=S0, K=K, r=r, q=q, sigma=sigma, T=T, N=N,
                    option_type=option_type, exercise=exercise)
    )
