#!/usr/bin/env python3

import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
from MDAnalysis.analysis import rms, align
from mpl_toolkits.mplot3d import Axes3D  # Required for some matplotlib versions

# INPUT SYSTEMS
systems = {
    "provide system label": ("rmsd.xvg", "rgyr.xvg"),
}

# Selection strings
HELIX1 = "resid 0-22 and name P"
HELIX2 = "(resid 22-40 or resid 77-88) and name P"
HELIX3 = "resid 41-76 and name P"
ALIGN_SEL = "name P"


# LOOP OVER SYSTEMS

for label, (top, traj) in systems.items():

    print(f"\n=== Processing {label} M urea ===")

    u = mda.Universe(top, traj)
    ref = mda.Universe(top)

    # Aligning the trajectory to the reference based on all P atoms
    aligner = align.AlignTraj(
        u,
        ref,
        select=ALIGN_SEL,
        in_memory=False,
        verbose=False
    )
    aligner.run()

    rmsd_selection = {
        "H1": HELIX1,
        "H2": HELIX2,
        "H3": HELIX3
    }

    R = rms.RMSD(
        u,
        ref,
        select=rmsd_selection,
        ref_frame=0
    )
    R.run()

    try:
        rmsd_data = R.results.rmsd[:, 3:]
    except AttributeError:
        # Fallback for MDAnalysis versions < 2.0
        rmsd_data = R.rmsd[:, 3:]

    np.savetxt(
        f"rmsd_{label}M.dat",
        rmsd_data,
        header="Helix1_RMSD(A) Helix2_RMSD(A) Helix3_RMSD(A)"
    )

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    frames = np.arange(len(rmsd_data))

    # Scatter plot: X=H1, Y=H2, Z=H3
    sc = ax.scatter(
        rmsd_data[:, 0], 
        rmsd_data[:, 1], 
        rmsd_data[:, 2], 
        c=frames,
        cmap="viridis",
        s=6,
        alpha=0.6
    )

    ax.set_xlabel("Helix-1 RMSD ($\AA$)")
    ax.set_ylabel("Helix-2 RMSD ($\AA$)")
    ax.set_zlabel("Helix-3 RMSD ($\AA$)")
    ax.set_title(f"RNA Helix RMSD Landscape ({label} M urea)")
    
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label("Frame Index")

    plt.tight_layout()
    plt.savefig(f"rmsd_{label}M.png", dpi=300)
    plt.close()

    print(f"Saved rmsd_{label}M.dat and rmsd_{label}M.png")

