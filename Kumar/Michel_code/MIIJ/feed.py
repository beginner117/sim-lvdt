import pandas as pd
import numpy as np

# 32 AWG
wire_width = 0.2032
ins_width =  0.0178 #0.02
wire_tot = wire_width + 2*ins_width

A = {'inn_ht': 24, 'inn_rad': 11, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 35, 'out_layers': 5,
     'out_dist': 54.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
# A Only 1 layer
A_out_1layer = {'inn_ht': 24, 'inn_rad': 11, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 35, 'out_layers': 1,
     'out_dist': 54.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
# F Only 1 winding and 1 layer
A_1_out_1layer = {'inn_ht': 24, 'inn_rad': 11, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': wire_tot, 'out_rad': 35, 'out_layers': 1,
     'out_dist': 54.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
B = {'inn_ht': 10, 'inn_rad': 4.5, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 10, 'out_rad': 25, 'out_layers': 7,
     'out_dist': 36, 'mag_len': 8, 'mag_dia': 5, 'ver_shi': 0}
C = {'inn_ht': 15, 'lowinn_ht': 22.5, 'inn_rad': 13.55, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 12,
     'out_rad': 20.5, 'out_layers': 5, 'out_dist': 13, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
D = {'inn_ht': 8, 'inn_rad': 7, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 8, 'out_rad': 11.5, 'out_layers': 7,
     'out_dist': 10, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
E = {'inn_ht': 8, 'inn_rad': 8, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 8, 'out_rad': 13, 'out_layers': 7,
     'out_dist': 10, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5, 'out_layers': 5,
     'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F Only 1 layer
F_out_1layer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F_out_2ndlayer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5 + wire_tot,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F_out_3rdlayer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5 + 2*wire_tot,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F_out_4thlayer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5 + 3*wire_tot,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F_out_5thlayer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5 + 4*wire_tot,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F no outer coils to investigate influence on B field
F_no_out = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 31.5,
                  'out_layers': 0, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F Only 1 winding and 1 layer
F_1_out_1layer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': wire_tot, 'out_rad': 31.5,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F Only 2 winding and 1 layer
F_2_out_1layer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 2*wire_tot, 'out_rad': 31.5,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F Only 10 winding and 1 layer
F_10_out_1layer = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 10*wire_tot, 'out_rad': 31.5,
                  'out_layers': 1, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
# F with larger outer radia
F_out_rad_plus5 = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 36.5,
                   'out_layers': 5, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
F_out_rad_plus10 = {'inn_ht': 18, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 41.5,
                   'out_layers': 5, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}
G = {'inn_ht': 24, 'inn_rad': 9, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 20, 'out_layers': 5,
     'out_dist': 28.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
H = {'inn_ht': 0, 'inn_rad': 0, 'inn_layers': 0, 'inn_dist': 0, 'out_ht': 10, 'out_rad': 16, 'out_layers': 8,
     'out_dist': 0, 'mag_len': 6, 'mag_dia': 3, 'ver_shi': 0}
I = {'inn_ht': 0, 'inn_rad': 0, 'inn_layers': 0, 'inn_dist': 0, 'out_ht': 5.2, 'out_rad': 10, 'out_layers': 8,
     'out_dist': 0, 'mag_len': 3, 'mag_dia': 1.5, 'ver_shi': 0}
J = {'inn_ht': 18, 'lowinn_ht': 23, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5,
     'out_rad': 31.5, 'out_layers': 5, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}

data = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G, 'H': H, 'I': I, 'J': J, 'F_out_1layer': F_out_1layer,
        'F_1_out_1layer': F_1_out_1layer, 'F_2_out_1layer': F_2_out_1layer, 'F_10_out_1layer': F_10_out_1layer,
        'A_out_1layer': A_out_1layer, 'A_1_out_1layer': A_1_out_1layer, 'F_no_out': F_no_out,
        'F_out_rad_plus5': F_out_rad_plus5, 'F_out_rad_plus10': F_out_rad_plus10, 'F_out_2ndlayer': F_out_2ndlayer,
        'F_out_3rdlayer': F_out_3rdlayer, 'F_out_4thlayer': F_out_4thlayer, 'F_out_5thlayer': F_out_5thlayer}


class Input:
    def __init__(self):
        pass

    def general(self):
        return [A, B, C, D, E, F, G, H, I, J]
        # return pd.DataFrame(data.keys())

    def return_data(self, design_type: str):
        return data[design_type]

# yi = Input()
# print(yi.general())
