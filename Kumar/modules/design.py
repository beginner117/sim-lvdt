
class Sensortype:
    def __init__(self, InnCoilCurrent, Simfreq, OutCoilCurrent):
        """
        class to determine the type of sensor.
        In general, 20mA-10khZ Inner coil current with no outer coil current indicates LVDT. 1A DC outer coil current with no inner coil current indicates VC

        ________INPUT________
        InnCoilCurrent: Inner coil current in Amps_(float)
        Simfreq: Frequency in Hz_(float)
        OutCoilCurrent: Outer coil current in Amps_(float)

        """
        self.InnCoilCurrent = InnCoilCurrent
        self.Simfreq = Simfreq
        self.OutCoilCurrent = OutCoilCurrent

    def para(self):
        """
        method in the class 'Sensortype' that returns the list containing inner coil current, excitation frequency, outer coil current
        returns a list containing sensor parameters
        _______Output_______
        Inner coil current
        Frequency
        Outer coil current
        """
        return [self.InnCoilCurrent, self.Simfreq, self.OutCoilCurrent]

class Simulation:
    """
    class to determine the coil motion parameters
    """
    def __init__(self, Nsteps, stepsize, inncoil_offset, data_file, fit_points = None):
        self.Nsteps = Nsteps
        self.stepsize = stepsize
        self.inncoil_offset = inncoil_offset
        self.data_file = data_file
        self.fit_points = fit_points
    def parameters(self):
        return [self.Nsteps, self.stepsize, self.inncoil_offset, self.data_file, self.fit_points]
class Wiretype():
    def __init__(self, outcoil_material, inncoil_material):
        self.outcoil_material = outcoil_material
        self.inncoil_material = inncoil_material
# wire diamater, insulation thickness, wire type, resistance(Ω/mm), electrical conductivity, resistivity(ohm*m), mag_perm(H/m)
    def prop_out(self):
        if self.outcoil_material == "30 AWG":
            return [0.254, 0.0216, "30 AWG", 103.7/304800]
        if self.outcoil_material == "31 AWG":
            return [0.2261, 0.0190, "31 AWG", 130.9/304800]
        if self.outcoil_material == "32 AWG":
            return [0.2032, 0.0178, "32 AWG", 162/304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]
        if self.outcoil_material == "34 AWG":
            return [0.1602, 0.01652, "34 AWG", 261.3/304800]
        if self.outcoil_material == "test1":
            return [0.190+0.01, 0.016, "test1", 0.6029/1000]
        if self.outcoil_material == "test2":
            return [0.200+0.007-0.007, 0.016, "test2", 0.5441/1000]
        if self.outcoil_material == "32 AWG_corrected_1":
            #return [0.2032+0.0062, 0.0178, "32 AWG_corrected_1", 162/304800]
            return [0.2032, 0.0178+(0.0062/2), "32 AWG_corrected_1", 162 / 304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]
        if self.outcoil_material == "32 AWG_corrected_2":
            #return [0.2032+0.0202, 0.0178, "32 AWG_corrected_2", 162/304800]
            return [0.2032, 0.0178+(0.0202/2), "32 AWG_corrected_2", 162 / 304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]

    def prop_inn(self):
        if self.inncoil_material == "30 AWG":
            return [0.254, 0.0216, "30 AWG", 103.7/304800]
        if self.inncoil_material == "31 AWG":
            return [0.2261, 0.0190, "31 AWG", 130.9/304800]
        if self.inncoil_material == "32 AWG":
            return [0.2032, 0.0178, "32 AWG", 162/304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]
        if self.inncoil_material == "34 AWG":
            return [0.1602, 0.01652, "34 AWG", 261.3/304800]
        if self.inncoil_material == "test1":
            return [0.190+0.01-0.01, 0.016, "test1", 0.6029/1000]
        if self.inncoil_material == "test2":
            return [0.200+0.007, 0.016, "test2", 0.5441/1000]
        if self.inncoil_material == "32 AWG_corrected_1":
            #return [0.2032+0.0062, 0.0178, "32 AWG_corrected_1", 162/304800]
            return [0.2032, 0.0178 + (0.0062 / 2), "32 AWG_corrected_1", 162 / 304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]
        if self.inncoil_material == "32 AWG_corrected_2":
            #return [0.2032+0.0202, 0.0178, "32 AWG_corrected_2", 162/304800]
            return [0.2032, 0.0178 + (0.0202 / 2), "32 AWG_corrected_2", 162 / 304800, 58, 1.68 * (10 ** (-8)), 1.256 * (10 ** (-6))]

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


class Geometry_yoke():
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

