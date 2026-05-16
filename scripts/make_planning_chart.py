"""Generates the Planning card thumbnail: a ballistic ball trajectory + samples.

Saved to assets/planning_chart.png. Re-run if the brand colors or chart change.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Site palette (kept in sync with styles.css)
ACCENT_BLUE = "#0d99ff"
ACCENT_PINK = "#ff5c8a"
ACCENT_ORANGE = "#ff7a59"
TEXT = "#1e1e1e"
TEXT_DIM = "#6b6b6b"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#d0d0d3",
    "axes.linewidth": 1.0,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

rng = np.random.default_rng(7)

# Ballistic ground truth (realistic juggling-height bounce)
g = 9.81
v0 = 3.5      # m/s, initial vertical velocity off the paddle
z0 = 0.55     # m, paddle/launch height in base_link
vx = 0.45     # m/s, slight horizontal drift
t_full = np.linspace(0, 1.0, 200)
x_traj = vx * t_full
z_traj = z0 + v0 * t_full - 0.5 * g * t_full ** 2

# Noisy HSV detections covering both the ascent and the descent
t_samples = np.linspace(0.06, 0.85, 9)
x_samples = vx * t_samples + rng.normal(0, 0.008, t_samples.size)
z_samples = (
    z0 + v0 * t_samples - 0.5 * g * t_samples ** 2
    + rng.normal(0, 0.025, t_samples.size)
)

strike_height = 0.50

# Find the descending crossing of the strike plane.
roots = np.roots([-0.5 * g, v0, z0 - strike_height])
real_pos_roots = sorted(float(r.real) for r in roots if abs(r.imag) < 1e-7 and r.real > 0)
t_impact = real_pos_roots[-1]  # descending branch
x_impact = vx * t_impact

fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=150)

# Strike plane
ax.axhline(
    strike_height,
    color=TEXT_DIM,
    linestyle="--",
    linewidth=1.2,
    alpha=0.55,
    label="Strike plane",
)

# Predicted trajectory (clip at strike plane on the descent for clarity)
mask = z_traj >= strike_height - 0.01
ax.plot(
    x_traj[mask],
    z_traj[mask],
    color=ACCENT_BLUE,
    linewidth=2.4,
    label="Ballistic fit",
)

# Detections
ax.scatter(
    x_samples,
    z_samples,
    color=ACCENT_ORANGE,
    s=70,
    edgecolor="white",
    linewidth=1.2,
    zorder=5,
    label="HSV detections",
)

# Impact point
ax.scatter(
    [x_impact],
    [strike_height],
    color=ACCENT_PINK,
    s=260,
    marker="*",
    zorder=6,
    edgecolor="white",
    linewidth=1.4,
    label="Predicted impact",
)

ax.set_xlabel("x (m)", fontsize=11, color=TEXT)
ax.set_ylabel("z (m)", fontsize=11, color=TEXT)
ax.tick_params(axis="both", colors=TEXT_DIM, labelsize=10)
ax.set_xlim(-0.02, max(x_traj[mask].max(), x_impact) * 1.15)
ax.set_ylim(0.3, max(z_traj.max(), z_samples.max()) * 1.1)
ax.grid(True, alpha=0.18, linewidth=0.8)
ax.legend(
    loc="upper right",
    frameon=False,
    fontsize=9.5,
    labelcolor=TEXT,
)

plt.tight_layout()

out_path = Path(__file__).resolve().parents[1] / "assets" / "planning_chart.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"wrote {out_path}")
