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
                # try:
                p = float(directory[12:])

                file = open(root+"/"+directory+"/vc-relax.out").read()
                if 'Final enthalpy' in file:
                    start_flag = file.find('Final enthalpy =')
                    end_flag = file.find('\n', start_flag)
                    enthalpy = float(file[start_flag + len('Final enthalpy ='):end_flag])
                else:
                    # If 'Final enthalpy' is not present, take the last calculated one
                    start_flag = file.rfind('enthalpy new')
                    end_flag = file.find('\n', start_flag)
                    enthalpy = float(file[start_flag + len('enthalpy new            ='):end_flag])
                p_enthalpy.append([p,enthalpy])
                # except:
                #     print('error')
    return np.array(sorted(p_enthalpy, key=lambda x: x[0]))

p_enthalpy_RS = get_p_enthalpy('RS')
p_RS = p_enthalpy_RS[:,0]/10            # GPa
enthalpy_RS = p_enthalpy_RS[:,1]/2      # A^3, 2 atoms in basis

p_enthalpy_RS = get_p_enthalpy('WU')
p_WU = p_enthalpy_WU[:,0]/10          # GPa
enthalpy_WU = p_enthalpy_WU[:,1]/8    # A^3, 8 atoms in basis

plt.plot(p_RS,enthalpy_RS,'bo',label='RS enthalpy')
plt.plot(p_WU,enthalpy_WU,'ro',label='WU enthalpy')
plt.xlabel('Pressure [GPa]')
plt.ylabel('Enthalpy/atom [Ry]')
plt.legend()
plt.tight_layout()
plt.savefig("enthalpy.png")
