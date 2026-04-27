import os
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO


def read_xvg(file):

    data = []

    with open(file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith('#') or line.startswith('@'):
                continue
            data.append(line)

    result = "".join(data)
    array = np.genfromtxt(StringIO(result))

    x = array[:,0]
    y = array[:,1]
    x_minlim = x[0]
    x_maxlim = x[-1]

    return x, y


def plot_graph(x, y, title, xlabel, ylabel, outputfile):

    fig, ax = plt.subplots(figsize=(12,7))
    ax.plot(x, y, color="darkturquoise", linewidth=1)
    ax.set_title(title, fontsize=18)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)

    ax.tick_params(direction="in", size=6, width=2)
    ax.set_xlim(x[0], x[-1])
    plt.tight_layout()

    plt.savefig(outputfile, dpi=300)

    plt.show()



print("\nEnter the required .xvg files\n")

protein_rmsd = input("Enter Protein RMSD file: ")
crystal_rmsd = input("Enter Crystal vs Equilibrated RMSD file: ")
rmsf_file = input("Enter RMSF file: ")
sasa_file = input("Enter SASA file: ")
rog_file = input("Enter Radius of Gyration file: ")
hbond_file = input("Enter Hbond file: ")


# Protein RMSD
x,y = read_xvg(protein_rmsd)
plot_graph(x, y,"Protein RMSD","Time (ns)","RMSD (nm)","protein_rmsd.jpeg")

# Crystal vs Equilibrated RMSD
x,y = read_xvg(crystal_rmsd)
plot_graph(x, y,"Crystal vs Equilibrated Structure RMSD","Time (ns)","RMSD (nm)","crystal_equilibrated_rmsd.jpeg")

# RMSF
x,y = read_xvg(rmsf_file)
plot_graph(x, y,"Residue Flexibility (RMSF)","Residue Number","RMSF (nm)","rmsf.jpeg")

# SASA
x,y = read_xvg(sasa_file)
plot_graph(x, y,"Solvent Accessible Surface Area","Time (ns)","SASA (nm^2)","sasa.jpeg")

# Radius of Gyration
x,y = read_xvg(rog_file)
plot_graph(x/1000, y,"Radius of Gyration","Time (ns)","Radius of Gyration (nm)","rog.jpeg")

# Hydrogen Bonds
x,y = read_xvg(hbond_file)
plot_graph(x/1000, y,"Hydrogen Bonds","Time (ns)","Number of Hydrogen Bonds","hbond.jpeg")


print("\nAll plots generated successfully.\n")