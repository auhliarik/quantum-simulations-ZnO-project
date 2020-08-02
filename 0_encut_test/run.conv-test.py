#!/usr/bin/env python

import os
import numpy as np

calc_script = 'ZnO-RS.scf.in'
pbs_script = 'pbs_Hartree'

min_encut = 25
max_encut = 65
stp_encut = 9

run_cmd = 'qsub pbs_Hartree'

for encut in np.linspace(min_encut, max_encut, stp_encut):
    
    E_scf = "{:5.3f}".format(encut)                     # format energy cutoff string

    print("Calculating {} Ry cutoff".format(E_scf))
    wd = "scf-" + E_scf

    if not os.path.exists(wd):                          # create directory for calculation
        os.makedirs(wd)

    with open(calc_script) as f:                        # create QE script in final directory
        with open(wd + "/scf.in", "w") as fa:
            for line in f:
                fa.write(line.replace("$KATOF$",E_scf)) # replace $KATOF$ with actual value
    
    with open(pbs_script) as f:                         # create PBS script in final directory
        with open(wd + "/pbs_Hartree", "w") as fa:
            for line in f:
                fa.write(line.replace("$NAME$",'MoS2-'+E_scf))

    os.system("cd "+wd+";"+run_cmd)                     # run calculation with PBS
