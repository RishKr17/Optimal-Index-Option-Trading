import math

def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def black_scholes_european(S, K, r, q, sigma, T, option_type: str):
    if T <= 0 or sigma <= 0:
        intrinsic = max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)
        return float(intrinsic)
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be > 0")

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    D_r, D_q = math.exp(-r * T), math.exp(-q * T)

    if option_type == "call":
        return S * D_q * _phi(d1) - K * D_r * _phi(d2)
    else:
        return K * D_r * _phi(-d2) - S * D_q * _phi(-d1)
