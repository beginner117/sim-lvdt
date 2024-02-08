import femm
import femm_model
import feed
import sys
import numpy as np
from scipy import integrate
from multiprocessing import Process
import fields
import matplotlib.pyplot as plt

class LVDT:
    def __init__(self, load_file):
        self.file = load_file
    def outer_flux(self, offset, flux_file, wire_dia = None, outer_coil_layers=None, outer_coil_rad=None):
        f = np.load(self.file, allow_pickle=True)
        f1 = f['Innercoil_config'].item()
        f2 = f['Input_parameters'].item()
        flux_data = fields.Flux(self.file, offset, flux_file, save=True)
        if wire_dia:
            wire_thickness = wire_dia
        else:
            bare_wire_dia = f2['outercoil Diameter_Insulation_Wiretype'][0]
            insulation_thickness = f2['outercoil Diameter_Insulation_Wiretype'][1]
            wire_thickness = bare_wire_dia+(2*insulation_thickness)
        if outer_coil_layers:
            outcoil_layers = outer_coil_layers
        else:
            outcoil_layers = f1['out_layers']
        if outer_coil_rad:
            outer_rad = outer_coil_rad
        else:
            outer_rad = f1['out_rad']

        flux_data.outcoil_flux(wire_thickness, outcoil_layers, outer_rad)

    def response(self, inncoil_range, outer_coil_dist=None, outer_coil_width=None, wire_dia = None, inner_current=None):
        f = np.load(self.file, allow_pickle=True)
        f1 = f['Innercoil_config'].item()
        f2 = f['Input_parameters'].item()
        inn_vol = abs(f['innercoil_voltage'].item())
        if wire_dia:
            wire_thickness = wire_dia
        else:
            bare_wire_dia = f2['outercoil Diameter_Insulation_Wiretype'][0]
            insulation_thickness = f2['outercoil Diameter_Insulation_Wiretype'][1]
            wire_thickness = bare_wire_dia + (2 * insulation_thickness)
        if outer_coil_dist:
            outcoil_dist = outer_coil_dist
        else:
            outcoil_dist = f1['out_dist']
        if outer_coil_width:
            outer_width = outer_coil_width
        else:
            outer_width = f1['out_ht']
        if inner_current:
            inn_exe = inner_current
        else:
            inn_exe = f2['Innercoil_current(A)']
        vol = fields.Voltages(self.file)
        res = vol.calculate(inncoil_range, outcoil_dist, outer_width, wire_thickness)

        plt.plot(res[0], inn_exe*(res[3]-res[1]), 'o--')
        plt.xlabel('Inner coil distance [mm]')
        plt.ylabel('Response [V/A]')
        plt.title('Outer coil response')
        plt.grid()
        plt.show()

        m, co = np.polyfit(res[0],(res[3]-res[1])/inn_exe, 1)
        print('slope of the response[V/mmA] : ',m )

        m_v, co_v = np.polyfit(res[0],((res[3]-res[1])/inn_vol)*70.02, 1)
        print('voltage normalised slope of the response [V/mmV] : ', m_v)


