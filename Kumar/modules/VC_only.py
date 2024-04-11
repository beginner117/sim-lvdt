import femm
import design
import femm_model
import coil
import feed
import fields
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
class Analysis:
    def __init__(self, save, sim_range:list, default, filename, design_type,input_excitation, materials = None, sim_type = 'FEMM+ana',  parameter1=None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
        self.sim_type = sim_type
        self.materials = materials
        self.input_excitation = input_excitation
    def simulate(self):
        femm.openfemm()
        femm.newdocument(0)
        value = feed.data
        in_pa = feed.Input()
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype(self.materials[1], self.materials[0], magnet_material=self.materials[2])
        input_par1 = {'TotalSteps_StepSize(mm)_Offset(mm)': self.sim_range, 'uppercoil Diameter(mm)_Insulation(mm)_Wiretype': wire.prop_out(),
                       'Magnet_material':wire.mag_mat(), 'Frequency(Hz)': sensor.para()[1], 'Outercoil_current(A)': sensor.para()[2]}
        if self.default == 'yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'],
                                  value[self.design_type]['out_ht'], value[self.design_type]['out_rad'], value[self.design_type]['out_layers'], value[self.design_type]['out_dist'],
                                  value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par2 = in_pa.return_data(self.design_type)
            input_par3 = 'design type ' + self.design_type
        if self.default == 'no':
            input_par2 = {'inn coil_height':18, 'inn coil_radius':0, 'inn coil_layers':6, 'inn coil_distance':0, 'out coil_height':5.2, 'out coil_radius':10, 'out coil_layers':1, 'out coil_distance':0, 'mag_length':40, 'mag_diameter':10, 'ver_shi':0}
            geo = design.Geometry(input_par2['inn coil_height'], input_par2['inn coil_radius'], input_par2['inn coil_layers'], input_par2['inn coil_distance'],
                                  input_par2['out coil_height'], input_par2['out coil_radius'], input_par2['out coil_layers'], input_par2['out coil_distance'],
                                  input_par2['mag_length'], input_par2['mag_diameter'], input_par2['ver_shi'])
            input_par3 = 'not a priliminary NIKHEF design'
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2],
                                 inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1],
                                 out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1],
                                 out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0],
                                 mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0],
                             inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3],
                             out_layers=geo.outcoil()[2], out_rad=geo.outcoil()[1],
                             out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1],
                             outwind_pr_layer=position.upp_outcoil()[3])
        print('coil config - [Coil_OutRadius, Coil_LowEnd, Coil_UppEnd, Coil_NrWind_p_Layer, Coil_NrWindings, Circuit_name]')
        print('outer coil config :', position.upp_outcoil())
        print(', outer coil material - ', wire.outcoil_material, ', magnet material - ', wire.mag_mat())
        out_dc = length.upp_outcoil() * wire.prop_out()[3]
        print('outer dc resistance as per catalog :', out_dc)
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                         circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=3, label1=wire.prop_out()[1], label2=geo.outcoil()[0], blockname=wire.prop_out()[2],
                                         turns_pr_layer=position.upp_outcoil()[4])
        magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')

        res = coil.Coil_prop(pre_simulation.parameters()[0])
        uppout_prop = res.uppout()
        mag_for = res.magnet()
        move_group = femm_model.Femm_move(groups=[3], x_dist=0, y_dist=pre_simulation.parameters()[2])
        for_def = []; for_imp = []; for_ana = []
        for i in range(0, pre_simulation.parameters()[0] + 1):
            print('coil position (from centre) : ', pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
            uppout_prop['UppOut_position'][i] = pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i
            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('VConly_ETpf_LIP.fem')
            femm.mi_analyze()
            femm.mi_loadsolution()

            femm.mo_groupselectblock(3)
            UppOut_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            femm.mo_groupselectblock(2)
            Magn_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()

            UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(position.upp_outcoil()[5])
            uppout_prop['UppOut_voltage'][i] = UppOutCoil_V
            uppout_prop['UppOut_current'][i] = UppOutCoil_I
            uppout_prop['UppOut_flux'][i] = UppOutCoil_FluxLink
            uppout_prop['UppOut_force'][i] = UppOut_Force19
            mag_for['Magnet_forces'][i] = Magn_Force19
            move_group = femm_model.Femm_move(groups=[3], x_dist=0, y_dist=pre_simulation.parameters()[1])

        Upp_Inductance = abs(uppout_prop['UppOut_flux'] / uppout_prop['UppOut_current'])
        Upp_resistance = abs(uppout_prop['UppOut_voltage'] / uppout_prop['UppOut_current'])
        print('upp out resistance as per femm :', abs(Upp_resistance))
        print('magnet force :', np.real(mag_for['Magnet_forces']))
        # inn_pos = np.array(uppout_prop["UppOut_position"])
        # nor_mag_force = np.real(mag_for['Magnet_forces']/uppout_prop['UppOut_current'])
        # a1, a2, a3 = np.polyfit(inn_pos, nor_mag_force, 2)
        # fit_for = (a1 * (inn_pos ** 2)) + (a2 * inn_pos) + a3
        plt.plot(np.real(uppout_prop['UppOut_position']),
                 abs(np.real(mag_for['Magnet_forces'] / uppout_prop['UppOut_current'])), 'o-')
        plt.xlabel('Coil (centre) Position relative to Magnet (centre) [mm]')
        plt.ylabel('Normalised Magnet Force [N/A]')
        plt.grid()
        plt.title('Simulated force [Type : I, {}layers_DC excitation]'.format(self.parameter1))
        plt.show()

        if self.save:
            if self.sim_type == 'FEMM+ana':
                np.savez_compressed(self.filename, Design_type=input_par3, Design = input_par2, Input_parameters=input_par1,
                                    UpperOutcoil_config=position.upp_outcoil(),
                                    UOC_positions=uppout_prop['UppOut_position'], UOC_forces=uppout_prop['UppOut_force'],
                                    Mag_forces=np.array(for_def), Mag_forces_imp=np.array(for_imp),
                                    UOC_flux=uppout_prop['UppOut_flux'], UOC_voltages=uppout_prop['UppOut_voltage'], UOC_currents=uppout_prop['UppOut_current'])
            if self.sim_type == 'math+ana':
                np.savez_compressed(self.filename, Design_type=input_par3, Design = input_par2, Input_parameters=input_par1,
                                    UpperOutcoil_config=position.upp_outcoil(),
                                    UOC_positions=uppout_prop['UppOut_position'], UOC_forces=uppout_prop['UppOut_force'], Mag_forces=np.array(for_ana),
                                    UOC_flux=uppout_prop['UppOut_flux'], UOC_voltages=uppout_prop['UppOut_voltage'], UOC_currents=uppout_prop['UppOut_current'])
            if self.sim_type == None:
                np.savez_compressed(self.filename, Design_type=input_par3, Design = input_par2, Input_parameters = input_par1, UpperOutcoil_config=position.upp_outcoil(),Input_config = other_par,
                                    UOC_positions = uppout_prop['UppOut_position'], UOC_forces = uppout_prop['UppOut_force'], Mag_forces = mag_for['Magnet_forces'],
                                    UOC_flux=uppout_prop['UppOut_flux'], UOC_voltages = uppout_prop['UppOut_voltage'], UOC_currents=uppout_prop['UppOut_current'])


