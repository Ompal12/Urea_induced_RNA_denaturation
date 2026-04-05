import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# FUNCTION TO READ XVG FILE

def read_xvg(filename):
    x, y = [], []
    try:
        with open(filename) as f:
            for line in f:
                if line.startswith(('#', '@')):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
    except FileNotFoundError:
        print(f"Warning: {filename} not found.")
    return np.array(x), np.array(y)

# INPUT SYSTEMS

systems = {
    "provide system label": ("rmsd.xvg", "rgyr.xvg"),
    
}

# COLLECT DATA

data = []
for conc, (rmsd_xvg, rg_xvg) in systems.items():
    _, rmsd = read_xvg(rmsd_xvg)
    _, rg   = read_xvg(rg_xvg)
    
    if len(rmsd) > 0 and len(rg) > 0:
        n = min(len(rmsd), len(rg))
        for i in range(n):
            data.append([float(conc), rmsd[i], rg[i]])

df = pd.DataFrame(data, columns=["Urea (M)", "RMSD (nm)", "Rg (nm)"])


sns.set(style="white", font_scale=1.2)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Common styling for both axes
for ax in axes:
    # Ensure ticks are visible on both axes
    ax.tick_params(axis='both', which='major', direction='out', length=6, width=1.5, colors='black', left=True, bottom=True)
    # Ensure grid is off
    ax.grid(False)
    # Optional: add a frame back if desired, or use despine
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)

# RMSD violin
sns.violinplot(
    data=df,
    x="Urea (M)",
    y="RMSD (nm)",
    inner="quartile",
    palette="Blues",
    ax=axes[0]
)
axes[0].set_title("RMSD Distribution vs Urea")

# Rg violin
sns.violinplot(
    data=df,
    x="Urea (M)",
    y="Rg (nm)",
    inner="quartile",
    palette="Reds",
    ax=axes[1]
)
axes[1].set_title("Radius of Gyration vs Urea")

plt.tight_layout()
plt.savefig("violin_RMSD_Rg_vs_Urea.png", dpi=300)
plt.show()

print("Saved: violin_RMSD_Rg_vs_Urea.png")
