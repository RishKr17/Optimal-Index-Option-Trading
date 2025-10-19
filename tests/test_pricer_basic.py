import math
from src.pricers.binomial import crr_binomial_pricer
from src.utils.bs import black_scholes_european

def test_american_call_matches_euro_when_q0():
    S0, K, r, q, sigma, T, N = 100, 100, 0.02, 0.0, 0.20, 1.0, 600
    binom = crr_binomial_pricer(S0,K,r,q,sigma,T,N,option_type="call",exercise="american").price
    bs    = black_scholes_european(S0,K,r,q,sigma,T,"call")
    assert abs(binom - bs) < 1e-2

def test_put_price_positive_and_boundary_present():
    res = crr_binomial_pricer(100,100,0.02,0.0,0.25,1.0,400, option_type="put", exercise="american")
    assert res.price > 0
    # likely some early exercise region
    assert isinstance(res.early_ex_boundary, dict)
