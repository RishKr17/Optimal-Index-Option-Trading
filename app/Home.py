import streamlit as st
from src.pricers.binomial import crr_binomial_pricer
from src.utils.plotting import plot_early_exercise_boundary

st.set_page_config(page_title="Optimal Index Option Trading", page_icon="📈", layout="centered")

st.title("📊 Optimal Index Option Trading")
st.markdown("### Part 1 – American Option Pricer")

S0 = st.slider("Spot Price (S₀)", 50, 150, 100, step=5)
K = st.slider("Strike Price (K)", 50, 150, 100, step=5)
r = st.number_input("Risk-free rate (r)", 0.0, 0.10, 0.03, step=0.01)
sigma = st.number_input("Volatility (σ)", 0.05, 1.0, 0.20, step=0.05)
T = st.number_input("Maturity (years)", 0.1, 2.0, 1.0, step=0.1)
N = st.slider("Binomial steps (N)", 50, 1000, 500, step=50)
option_type = st.selectbox("Option type", ["put", "call"])

if st.button("Run pricer"):
    res = crr_binomial_pricer(S0, K, r, 0.0, sigma, T, N, option_type=option_type, exercise="american")
    st.success(f"**American {option_type.title()} Price:** {res.price:.4f}")
    st.pyplot(plot_early_exercise_boundary(res, f"American {option_type.title()} Early-Exercise Threshold"))
