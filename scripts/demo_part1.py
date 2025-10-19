import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pricers.binomial import crr_binomial_pricer
from src.utils.bs import black_scholes_european
from src.utils.plotting import plot_early_exercise_boundary

def main():
    S0, K, r, q, sigma, T, N = 100.0, 100.0, 0.03, 0.0, 0.20, 1.0, 500

    # American PUT
    res_put = crr_binomial_pricer(S0, K, r, q, sigma, T, N, option_type="put", exercise="american")
    print(f"American Put: {res_put.price:.6f}")
    plot_early_exercise_boundary(res_put, "American Put Early-Exercise Threshold")

    # American CALL (q=0) ~ European Call
    res_call = crr_binomial_pricer(S0, K, r, q, sigma, T, N, option_type="call", exercise="american")
    bs_call  = black_scholes_european(S0, K, r, q, sigma, T, "call")
    print(f"American Call (q=0): {res_call.price:.6f}  |  BS Euro Call: {bs_call:.6f}")

if __name__ == "__main__":
    main()
