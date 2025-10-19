import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from src.pricers.binomial import PriceResult  # adjust if you changed imports

def plot_early_exercise_boundary(
    res: PriceResult,
    title: Optional[str] = None,
    reverse_time: bool = True
):
    """
    Plot the early-exercise boundary S*(t) vs time.
    """
    if not res.early_ex_boundary:
        print("No early exercise boundary.")
        return

    N = res.S_tree.shape[0] - 1
    T = res.params["T"]
    times = np.array(sorted(res.early_ex_boundary.keys()))
    t_axis = times * (T / N)
    S_star = np.array([res.early_ex_boundary[i] for i in times])

    plt.figure(figsize=(6, 4))
    plt.plot(t_axis, S_star, marker="o")
    if reverse_time:
        plt.gca().invert_xaxis()
        plt.xlabel("Time to Maturity (years)")
    else:
        plt.xlabel("Time (years)")
    plt.ylabel("S* (early-ex threshold)")
    plt.title(title or f"Early-Exercise Boundary ({res.params['exercise']} {res.params['option_type']})")
    plt.grid(True)
    plt.show()
