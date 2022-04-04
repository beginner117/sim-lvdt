import femm
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
    def __init__(self, outcoil_material, inncoil_material):
        self.outcoil_material = outcoil_material
        self.inncoil_material = inncoil_material

    def prop31(self):
        return [0.2261, 0.0190, "31 AWG"]

    def prop32(self):
        return [0.2032, 0.0178, "32 AWG"]

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
    def __init__(self, innUP_ht, innLOW_ht, inn_rad, inn_layers, inn_dist, out_ht, out_rad, out_layers, out_dist, mag_ht, mag_rad, ver_shi):

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


class Blocks():
    def __init__(self):
        self.b1_l = 3.25
        self.b1_h = 28
        self.b2_l = 2.75
        self.b2_h = 9
        self.b3_l = 12.58
        self.b3_h = 9
        self.b4_l = 6.53
        self.b4_h = 8.65
        self.b5_l = 2.055
        self.b5_h = 2
        self.b6_l = 4.47
        self.b6_h = 4
        self.b7_l = 15.85
        self.b7_h = 6

        self.yokeinnrad = 5
        self.yokeuppend = -7.5-26.25-6.75
        self.yokeoutrad = 28.575

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

