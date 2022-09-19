import numpy as np
import matplotlib.pyplot as plt

class Position():
    def __init__(self, inn_ht, inn_rad, inn_layers, inn_dist, out_ht, out_rad, out_layers,  out_dist,
                 ver_shi, inn_wiredia, inn_wireins, out_wiredia, out_wireins, mag_len, mag_dia):
        self.inn_ht = inn_ht
        self.inn_rad = inn_rad
        self.inn_layers = inn_layers
        self.inn_dist = inn_dist
        self.out_ht = out_ht
        self.out_rad = out_rad
        self.out_layers = out_layers
        self.out_dist = out_dist
        self.ver_shi = ver_shi
        self.inn_wiredia = inn_wiredia
        self.out_wiredia = out_wiredia
        self.inn_wireins = inn_wireins
        self.out_wireins = out_wireins
        self.mag_len = mag_len
        self.mag_dia = mag_dia

        
    def inncoil(self):
        InnCoil_OutRadius = self.inn_rad + ((self.inn_wiredia + self.inn_wireins * 2) * self.inn_layers)
        InnCoil_Lowend = (self.inn_dist - self.inn_ht) / 2
        InnCoil_Uppend = InnCoil_Lowend + self.inn_ht
        InnCoil_NrWind_p_Layer = (self.inn_ht) / (self.inn_wiredia + self.inn_wireins * 2)
        InnCoil_NrWindings = InnCoil_NrWind_p_Layer * self.inn_layers
        InnCoil_Circuit = "InnCoil_Circuit"
        return [InnCoil_OutRadius, InnCoil_Lowend, InnCoil_Uppend, InnCoil_NrWind_p_Layer, InnCoil_NrWindings,
                InnCoil_Circuit]
        
    def upp_outcoil(self):
        UppOutCoil_OutRadius = self.out_rad + (
                    (self.out_wiredia + self.out_wireins * 2) * self.out_layers)
        UppOutCoil_LowEnd = (self.out_dist - self.out_ht) / 2
        UppOutCoil_UppEnd = UppOutCoil_LowEnd + self.out_ht
        UppOutCoil_NrWind_p_Layer = (self.out_ht) / (self.out_wiredia + self.out_wireins * 2)
        UppOutCoil_NrWindings = UppOutCoil_NrWind_p_Layer * self.out_layers
        UppOutCoil_Circuit = "UppOutCoil_Circuit"
        return [UppOutCoil_OutRadius, UppOutCoil_LowEnd, UppOutCoil_UppEnd, UppOutCoil_NrWind_p_Layer,
                UppOutCoil_NrWindings, UppOutCoil_Circuit]
        
    def low_outcoil(self):
        LowOutCoil_OutRadius = self.out_rad + (
                    (self.out_wiredia + self.out_wireins * 2) * self.out_layers)
        LowOutCoil_UppEnd = -1 * (self.out_dist - self.out_ht) / 2
        LowOutCoil_LowEnd = LowOutCoil_UppEnd - self.out_ht
        LowOutCoil_NrWind_p_Layer = (LowOutCoil_UppEnd - LowOutCoil_LowEnd) / (
                    self.out_wiredia + self.out_wireins * 2)
        LowOutCoil_NrWindings = LowOutCoil_NrWind_p_Layer * self.out_layers
        LowOutCoil_Circuit = "LowOutCoil_Circuit"
        return [LowOutCoil_OutRadius, LowOutCoil_UppEnd, LowOutCoil_LowEnd, LowOutCoil_NrWind_p_Layer,
                LowOutCoil_NrWindings, LowOutCoil_Circuit]

    def magnet(self):
        Magnet_UppEnd = self.mag_len / 2 + self.ver_shi
        Magnet_LowEnd = -self.mag_len / 2 + self.ver_shi
        Magnet_Radius = self.mag_dia / 2
        return [Magnet_UppEnd, Magnet_LowEnd, Magnet_Radius]
    
class Length():
    def __init__(self, inn_layers, inn_rad, inn_wiredia, inn_wireins, innwind_pr_layer, out_layers, out_rad, out_wiredia, out_wireins, outwind_pr_layer):
        self.inn_layers = inn_layers
        self.inn_rad = inn_rad
        self.inn_wiredia = inn_wiredia
        self.inn_wireins = inn_wireins
        self.innwind_pr_layer = innwind_pr_layer
        self.out_layers = out_layers
        self.out_rad = out_rad
        self.out_wiredia = out_wiredia
        self.out_wireins = out_wireins
        self.outwind_pr_layer = outwind_pr_layer

    def inncoil(self):
        InnCoil_TotalWire = 0
        for i in range(0, self.inn_layers):
            # circ = 2*np.pi*InnCoil_InRadius+i*(InnCoil_WireDiam+InnCoil_WireInsul)
            circ = 2 * np.pi * (self.inn_rad + i * (self.inn_wiredia + self.inn_wireins * 2))
            InnCoil_TotalWire += circ * self.innwind_pr_layer
        print("Total length of inn coil wire (mm):", InnCoil_TotalWire)
        print("\n")
        return InnCoil_TotalWire

    def upp_outcoil(self):
        UppOutCoil_TotalWire = 0
        for i in range(0, self.out_layers):
            circ = 2 * np.pi * (self.out_rad + i * (self.out_wiredia + self.out_wireins * 2))
            UppOutCoil_TotalWire += circ * self.outwind_pr_layer
        print("Total length of upper out wire (mm):", UppOutCoil_TotalWire)
        print("\n")
        return UppOutCoil_TotalWire

    def low_outcoil(self):
        LowOutCoil_TotalWire = 0
        for i in range(0, self.out_layers):
            # circ = 2*np.pi*LowOutCoil_InRadius+i*(LowOutCoil_WireDiam+LowOutCoil_WireInsul)
            circ = 2 * np.pi * (self.out_rad + i * (self.out_wiredia + self.out_wireins * 2))
            LowOutCoil_TotalWire += circ * self.outwind_pr_layer
        print("Total length of lower out coil wire (mm):", LowOutCoil_TotalWire)
        print("\n")
        return LowOutCoil_TotalWire



'''
class Length():
    def __init__(self):
        pass

    def inncoil(self):
        InnCoil_TotalWire = 0
        for i in range(0, geo.inncoil()[2]):
            # circ = 2*np.pi*InnCoil_InRadius+i*(InnCoil_WireDiam+InnCoil_WireInsul)
            circ = 2 * np.pi * (geo.inncoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
            InnCoil_TotalWire += circ * position.inncoil()[3]
        print("Total length of inn coil wire (mm):", InnCoil_TotalWire)
        print("\n")
        return InnCoil_TotalWire

    def upp_outcoil(self):
        UppOutCoil_TotalWire = 0
        for i in range(0, geo.outcoil()[2]):
            # circ = 2*np.pi*(UppOutCoil_InRadius+i*(UppOutCoil_WireDiam+UppOutCoil_WireInsul))
            circ = 2 * np.pi * (geo.outcoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
            UppOutCoil_TotalWire += circ * position.upp_outcoil()[3]
        print("Total length of upper out wire (mm):", UppOutCoil_TotalWire)
        print("\n")
        return UppOutCoil_TotalWire

    def low_outcoil(self):
        LowOutCoil_TotalWire = 0
        for i in range(0, geo.outcoil()[2]):
            # circ = 2*np.pi*LowOutCoil_InRadius+i*(LowOutCoil_WireDiam+LowOutCoil_WireInsul)
            circ = 2 * np.pi * (geo.outcoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
            LowOutCoil_TotalWire += circ * position.low_outcoil()[3]
        print("Total length of lower out coil wire (mm):", LowOutCoil_TotalWire)
        print("\n")
        return LowOutCoil_TotalWire
length = Length()
'''
'''
       class Position():
           def __init__(self):
               pass

           def inncoil(self):
               InnCoil_OutRadius = geo.inncoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.inncoil()[2])
               InnCoil_Lowend = (geo.inncoil()[3] - geo.inncoil()[0]) / 2
               InnCoil_Uppend = InnCoil_Lowend + geo.inncoil()[0]
               InnCoil_NrWind_p_Layer = (geo.inncoil()[0]) / (wire.prop32()[0] + wire.prop32()[1] * 2)
               InnCoil_NrWindings = InnCoil_NrWind_p_Layer * geo.inncoil()[2]
               InnCoil_Circuit = "InnCoil_Circuit"
               return [InnCoil_OutRadius, InnCoil_Lowend, InnCoil_Uppend, InnCoil_NrWind_p_Layer, InnCoil_NrWindings,
                       InnCoil_Circuit]

           def upp_outcoil(self):
               UppOutCoil_OutRadius = geo.outcoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.outcoil()[2])
               UppOutCoil_LowEnd = (geo.outcoil()[3] - geo.outcoil()[0]) / 2
               UppOutCoil_UppEnd = UppOutCoil_LowEnd + geo.outcoil()[0]
               UppOutCoil_NrWind_p_Layer = (geo.outcoil()[0]) / (wire.prop32()[0] + wire.prop32()[1] * 2)
               UppOutCoil_NrWindings = UppOutCoil_NrWind_p_Layer * geo.outcoil()[2]
               UppOutCoil_Circuit = "UppOutCoil_Circuit"
               return [UppOutCoil_OutRadius, UppOutCoil_LowEnd, UppOutCoil_UppEnd, UppOutCoil_NrWind_p_Layer,
                       UppOutCoil_NrWindings, UppOutCoil_Circuit]

           def low_outcoil(self):
               LowOutCoil_OutRadius = geo.outcoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.outcoil()[2])
               LowOutCoil_UppEnd = -1 * ((geo.outcoil()[3] - geo.outcoil()[0]) / 2)
               LowOutCoil_LowEnd = LowOutCoil_UppEnd - geo.outcoil()[0]
               LowOutCoil_NrWind_p_Layer = (LowOutCoil_UppEnd - LowOutCoil_LowEnd) / (
                           wire.prop32()[0] + wire.prop32()[1] * 2)
               LowOutCoil_NrWindings = LowOutCoil_NrWind_p_Layer * geo.outcoil()[2]
               LowOutCoil_Circuit = "LowOutCoil_Circuit"
               return [LowOutCoil_OutRadius, LowOutCoil_UppEnd, LowOutCoil_LowEnd, LowOutCoil_NrWind_p_Layer,
                       LowOutCoil_NrWindings, LowOutCoil_Circuit]

           def magnet(self):
               Magnet_UppEnd = geo.mag()[0] / 2 + geo.mag()[2]
               Magnet_LowEnd = -geo.mag()[0] / 2 + geo.mag()[2]
               Magnet_Radius = geo.mag()[1] / 2
               return [Magnet_UppEnd, Magnet_LowEnd, Magnet_Radius]
       position = Position()
'''
