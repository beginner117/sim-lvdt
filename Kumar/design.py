import femm_model
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil

class Sensortype():
    def __init__(self, InnCoilCurrent, Simfreq, OutCoilCurrent):
        self.InnCoilCurrent = InnCoilCurrent
        self.Simfreq = Simfreq
        self.OutCoilCurrent = OutCoilCurrent

    def para(self):
        return [self.InnCoilCurrent, self.Simfreq, self.OutCoilCurrent]

class Wiretype():
    def __init__(self, outcoil_material:None, inncoil_material:None):
        self.outcoil_material = outcoil_material
        self.inncoil_material = inncoil_material
# wire diamater, insulation thickness, wire type, electrical conductivity, resistivity(ohm*m), mag_perm(H/m)
    def prop31(self):
        return [0.2261, 0.0190, "31 AWG"]

    def prop32(self):
        return [0.2032, 0.0178, "32 AWG",  58, 1.68*(10**(-8)), 1.256*(10**(-6))]

    def mag_mat(self):
        mat = "N40"
        return mat

    def yoke_mat(self):
        mate = "Pure iron, annealed"
        return mate

class Geometry():
    def __init__(self, inn_ht, inn_rad, inn_layers, inn_dist, out_ht, out_rad, out_layers, out_dist, mag_len, mag_dia, ver_shi):

        self.inn_ht = inn_ht
        self.inn_rad = inn_rad
        self.inn_layers = inn_layers
        self.inn_dist = inn_dist
        self.out_ht = out_ht
        self.out_rad = out_rad
        self.out_layers = out_layers
        self.out_dist = out_dist
        self.mag_len = mag_len
        self.mag_dia = mag_dia
        self.ver_shi = ver_shi

    def inncoil(self):
        return [self.inn_ht, self.inn_rad, self.inn_layers, self.inn_dist]

    def outcoil(self):
        return [self.out_ht, self.out_rad, self.out_layers, self.out_dist]

    def mag(self):
        return [self.mag_len, self.mag_dia, self.ver_shi]


class Geometry1():
    def __init__(self, innUP_ht:float, innLOW_ht:float, inn_rad:float, inn_layers:float, inn_dist:float, out_ht:float, out_rad:float, out_layers:float, out_dist:float, mag_ht:float, mag_rad:float, ver_shi:float):

        self.innUP_ht = innUP_ht
        self.innLOW_ht = innLOW_ht
        self.inn_rad = inn_rad
        self.inn_layers = inn_layers
        self.inn_dist = inn_dist
        self.out_ht = out_ht
        self.out_rad = out_rad
        self.out_layers = out_layers
        self.out_dist = out_dist
        self.mag_ht = mag_ht
        self.mag_rad = mag_rad
        self.ver_shi = ver_shi

    def Upp_Inncoil(self):
        return [self.innUP_ht, self.inn_rad, self.inn_layers, self.inn_dist]

    def Low_Inncoil(self):
        return [self.innLOW_ht, self.inn_rad, self.inn_layers, self.inn_dist]

    def outcoil(self):
        return [self.out_ht, self.out_rad, self.out_layers, self.out_dist]

    def mag(self):
        return [self.mag_ht, self.mag_rad, self.ver_shi]

'''
class Position(Geometry1):
    def __init__(self):

        Geometry1.__init__(self)
    def Low_Inncoil(self):
        Low_Inncoil_OutRadius = Geometry1.Low_Inncoil()[1] + (
                    (Wiretype.prop31()[0] + Wiretype.prop31()[1] * 2) * Geometry1.Low_Inncoil()[2])
        Low_Inncoil_Lowend = -1 * (Geometry1.Low_Inncoil()[3] + (Geometry1.Low_Inncoil()[0]) / 2)
        Low_Inncoil_Uppend = Low_Inncoil_Lowend + Geometry1.Low_Inncoil()[0]
        Low_Inncoil_NrWind_p_Layer = (Geometry1.Upp_Inncoil()[0]) / (Wiretype.prop31()[0] + Wiretype.prop31()[1] * 2)
        Low_Inncoil_NrWindings = Low_Inncoil_NrWind_p_Layer * Geometry1.Upp_Inncoil()[2]
        Low_Inncoil_Circuit = "Low_Inncoil_Circuit"
        return [Low_Inncoil_OutRadius, Low_Inncoil_Lowend, Low_Inncoil_Uppend, Low_Inncoil_NrWind_p_Layer,
                Low_Inncoil_NrWindings,
                Low_Inncoil_Circuit]
'''

class Blocks():
    def __init__(self):
        self.b1_l = 7
        self.b1_h = 33.5
        self.b2_l = 2.75
        self.b2_h = 9
        self.b3_l = 18.95
        self.b3_h = 9
        self.b4_l = 16.20
        self.b4_h = 12.5
        self.b5_l = 3.4
        self.b5_h = 2
        self.b6_l = 12.8
        self.b6_h = 6
        self.b7_l = 16.65
        self.b7_h = 2

        self.yokeinnrad = 8
        self.yokeuppend = -14-42
        self.yokeoutrad = 44.45
        self.innyoke_gap = 4.25

    def b1(self):
        return [self.b1_l, self.b1_h]
    def b2(self):
        return [self.b2_l, self.b2_h]
    def b3(self):
        return [self.b3_l, self.b3_h]
    def b4(self):
        return [self.b4_l, self.b4_h]
    def b5(self):
        return [self.b5_l, self.b5_h]
    def b6(self):
        return [self.b6_l, self.b6_h]
    def b7(self):
        return [self.b7_l, self.b7_h]

