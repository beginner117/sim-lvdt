import sys
sys.path.append('./modules/')
import numpy as np
import math
import MakeBfield
import femm_simulation
import matplotlib.pyplot as plt
from wakepy import set_keepawake, unset_keepawake

set_keepawake(keep_screen_awake=False) # Keeps the computer running until the script is finished, prevents the computer
# from entering sleepmode

# FEMM simulation
"""
sim_code = femm_simulation.Position_sensor(False, sim_range={'steps_size_offset': [[40, 0.25, -5]]},
                                               data={'filename(s)': ['typeF_test'], 'is default': ['yes'],
                                                     'design or parameter': ['F']})
sim_code.lvdt()#"""

'asymm_circle_flux_polar should put error notice when r_max > than biggest value of FEMM R vector'

### Example Code for singular layers

#first generate a B field with make_b_field
#MakeBfield.make_b_field2(35, 0.01, 38, 0.1, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005')
#MakeBfield.remove_inncoil_b_field('F', 'typeF_dr_1_dz_01_1layer', 'typeF_dr_1_dz_01_1layer_rminn')
#you can plot it using this command
#MakeBfield.plot_b_field('typeF_dr_1_dz_01_Mesh_0.005')
#plt.show()
#after generating
#MakeBfield.compute_symm_flux("F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_1layer_symm')
#MakeBfield.compute_asymm_flux(0, 0.01, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x0_dtheta01')
#MakeBfield.compute_asymm_flux(1, 0.01, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x1_dtheta01')
#MakeBfield.compute_asymm_flux(3, 0.01, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x3_dtheta01')
#MakeBfield.compute_asymm_flux(5, 0.01, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x5_dtheta01')
#MakeBfield.compute_asymm_flux(6, 0.01, "F_out_1layer", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x6_dtheta01')

### Code for simulating multiple layers, while also looping over varying transversal offset
# important to uncomment if __name__ == '__main__': for parallel processing

# if __name__ == '__main__':
# Loop over varying transversal offsets
#     #offsets = [0, 1, 3, 5, 6] # offsets vec used for Type F
#     #offsets = [0, 1, 3, 5, 10, 15, 19] # offsets vec used for Type A
#     for a in offsets:
#         MakeBfield.compute_asymm_flux_layers_par(a, 0.001, "F", 'typeF_dr_1_dz_01_Mesh_0.005', 'typeF_dr_1_dz_01_asymm_x'+ str(a) +'_dtheta001_5layers_Tot')

# Code for computing the voltage, looping over varying offsets

# F_off = [0,1,3,5,6]
# A_off = [0,1,3,5,10,15,19]
# for a in F_off:
#     MakeBfield.compute_voltages_disc(34, "F", 'typeF_dr_1_dz_01_asymm_x'+str(a)+'_dtheta001_5layers_Tot'
#                                      , 'typeF_dr_1_dz_01_asymm_x'+str(a)+'_dtheta001_5layers_Tot_disc')

unset_keepawake()