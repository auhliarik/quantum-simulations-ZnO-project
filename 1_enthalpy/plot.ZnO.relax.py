#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import os
import numpy as np
from matplotlib import pyplot as plt

def get_p_enthalpy(mode):
    p_enthalpy = []
    for root, directories, files in os.walk("."):
        for directory in sorted(directories):
            if "vc-relax-{}-".format(mode) in directory:
                try:
                    p = float(directory[12:])

                    for line in open(root+"/"+directory+"/vc-relax.out"):
                        line = line.strip()
                        if line.startswith('Final enthalpy'):
                            # Line has format like: 'Final enthalpy =    -503.2618573805 Ry'
                            enthalpy = float(line[17:-3])

                    p_enthalpy.append([p,enthalpy])
                except:
                    print('error')
    return np.array(sorted(p_enthalpy, key=lambda x: x[0]))

p_enthalpy_RS = get_p_enthalpy('RS')
p_RS = p_enthalpy_RS[:,0]/10          # GPa
enthalpy_RS = p_enthalpy_RS[:,1]      # A^3

plt.plot(p_RS,enthalpy_RS,'bo',label='relax. data')
plt.xlabel('Pressure [GPa]')
plt.ylabel('Enthalpy [Ry]')
plt.legend()
plt.tight_layout()
plt.savefig("enthalpy.png")
