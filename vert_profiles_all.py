#
# User Input
base_dir = "/glade/derecho/scratch/rozoff/cm1/storm/baseline"
var = "rtke"
#
import numpy as np
import os
from sys import exit
from netCDF4 import Dataset
import matplotlib.pyplot as plt
#
prefixes = "cm1out_diag_"
files = [f for f in os.listdir(base_dir) if f.startswith(prefixes)]
files.sort()
num_files = len(files)
zh = 200
if var == "w":
    zh = 201
#
# Initialize arrays
vargen_array = np.empty((zh, num_files))
#
for i, file in enumerate(files):
    if file.startswith(prefixes):
        file_path = os.path.join(base_dir, file)
        print(f"Reading in data from experiment {file_path}")
        if os.path.exists(file_path):
            with Dataset(file_path, 'r') as ds:
                vargen = np.squeeze(ds.variables[var][:])
                vargen_array[:, i] = vargen
                if i == 0:
                    z_axis = ds.variables['zh'][:]
                    if var == "w":
                        z_axis = ds.variables['zf'][:]
#
# /glade/work/rozoff/nsf/analysis/hifrq
fig, ax = plt.subplots(figsize = (7, 7))
for i in range(0, num_files):
    #for i in range(0, 50):
    if i < 150:
        ax.plot(np.squeeze(vargen_array[:, i]), z_axis, color = 'steelblue', linewidth = 0.5, alpha = 0.4)
    else:
        ax.plot(np.squeeze(vargen_array[:, i]), z_axis, color = 'dimgray', linewidth = 0.5, alpha = 0.4)
ax.plot(np.nanmean(vargen_array[:,150:], axis = 1), z_axis, color = 'indianred', linewidth = 4)
if var == "v":
    plt.xlim(30, 50)
    vartitle = "V (m s$^{-1}$)"
elif var == "u":
    plt.xlim(-15, 7)
    vartitle = "U (m s$^{-1}$)"
elif var == "w":
    plt.xlim(-10, 10)
    vartitle = "W (m s$^{-1}$)"
elif var == "thv":
    plt.xlim(300, 350)
    vartitle = "$θ_v$ (K)"
elif var == "qv":
    plt.xlim(0, 0.021)
    vartitle = "q$_v$ (g kg$^{-1}$)"
elif var == "rtke":
    plt.xlim(0, 10)
    vartitle = "Resolved TKE (m$^2$ s$^{-1}$)"
plt.ylim(0, 8000)
plt.xlabel(vartitle, fontsize = 16, fontweight = 'bold')
plt.ylabel('Height (m)', fontsize = 16, fontweight = 'bold')
fig.savefig(f"{var}.png", bbox_inches = 'tight', dpi = 300)
plt.show()
