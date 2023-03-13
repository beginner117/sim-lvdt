import pandas as pd
import numpy as np

A = {'inn_ht': 24, 'inn_rad': 11, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 35, 'out_layers': 5,
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
G = {'inn_ht': 24, 'inn_rad': 9, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5, 'out_rad': 20, 'out_layers': 5,
     'out_dist': 28.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
H = {'inn_ht': 0, 'inn_rad': 0, 'inn_layers': 0, 'inn_dist': 0, 'out_ht': 10, 'out_rad': 16, 'out_layers': 8,
     'out_dist': 0, 'mag_len': 6, 'mag_dia': 3, 'ver_shi': 0}
I = {'inn_ht': 0, 'inn_rad': 0, 'inn_layers': 0, 'inn_dist': 0, 'out_ht': 5.2, 'out_rad': 10, 'out_layers': 8,
     'out_dist': 0, 'mag_len': 3, 'mag_dia': 1.5, 'ver_shi': 0}
J = {'inn_ht': 18, 'lowinn_ht': 23, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 0, 'out_ht': 13.5,
     'out_rad': 31.5, 'out_layers': 5, 'out_dist': 14.5, 'mag_len': 0, 'mag_dia': 0, 'ver_shi': 0}

data = {'A':A, 'B':B, 'C':C, 'D':D, 'E':E, 'F':F, 'G':G, 'H':H, 'I':I, 'J':J}
class Input:
    def __init__(self):
        pass
    def general(self):
        return [A, B, C, D, E, F, G, H, I, J]
        #return pd.DataFrame(data.keys())
    def A(self):
        return A
    def B(self):
        return B
    def C(self):
        return C
    def D(self):
        return D
    def E(self):
        return E
    def F(self):
        return F
    def G(self):
        return G
    def H(self):
        return H
    def I(self):
        return I
    def J(self):
        return J


yi = Input()
print(yi.general())