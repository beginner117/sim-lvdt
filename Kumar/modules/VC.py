import femm
import design
import femm_model
import coil
import feed
import fields
import numpy as np
import matplotlib.pyplot as plt
import sys

class Analysis:
    def __init__(self,save, sim_range: list, default, filename=None, design_type= None, parameter1=None, simulation_type=None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.sim_type = simulation_type
        self.design_type = design_type
        self.default = default
    def simulate(self):
        femm.openfemm()  # The package must be initialized with the openfemm command.
        femm.newdocument(0)  # We need to create a new Magnetostatics document to work on.
        value = feed.data
        in_pa = feed.Input()
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "31 AWG", magnet_material='N40')
        input_par1 = {'TotalSteps_StepSize_Offset': self.sim_range, 'outercoil Diameter(mm)_Insulation(mm)_Wiretype': wire.prop_out(), 'innercoil Diameter(mm)_Insulation(mm)_Wiretype': wire.prop_inn(),
                      'Innercoil_current(A)': sensor.para()[0], 'Frequency(Hz)': sensor.para()[1], 'Outercoil_current(A)': sensor.para()[2], 'Magnet_material':wire.mag_mat()}
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par2 = in_pa.return_data(self.design_type)
            input_par3 = 'NIKHEF design type : ' + self.design_type
        if self.default == 'no':
            input_par2 = {'IC_height': 24, 'IC_radius': 11, 'IC_layers': 6, 'IC_distance': 0, 'OC_height': 13.5, 'OC_radius': 35, 'OC_layers': self.parameter1,
                         'OC_distance': 54.5, 'mag_len': 40, 'mag_dia': 10, 'ver_shi': 0}
            geo = design.Geometry(input_par2['IC_height'], input_par2['IC_radius'], input_par2['IC_layers'], input_par2['IC_distance'], input_par2['OC_height'], input_par2['OC_radius'],
                                  input_par2['OC_layers'], input_par2['OC_distance'], input_par2['mag_len'], input_par2['mag_dia'], input_par2['ver_shi'])
            input_par3 = 'not a priliminary NIKHEF design'
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2], inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1], out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0], mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3], out_layers=geo.outcoil()[2],
                             out_rad=geo.outcoil()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], outwind_pr_layer=position.upp_outcoil()[3])
        print('coil config - [Coil_OutRadius, Coil_LowEnd, Coil_UppEnd, Coil_NrWind_p_Layer, Coil_NrWindings, Circuit_name]')
        print('inner coil config :', position.inncoil(), '\nupper outer coil config :', position.upp_outcoil(),'\nlower out coil config :', position.low_outcoil())
        print('inner coil material - ', wire.inncoil_material, ', outer coil material - ', wire.outcoil_material, ', magnet material - ', wire.mag_mat())
        print('inner, upper outer, total coil lengths : ', length.inncoil(), length.upp_outcoil(),length.inncoil() + (2 * length.upp_outcoil()))
        if wire.prop_out()[3] and wire.prop_inn()[3]:
            inn_dc = length.inncoil() * wire.prop_inn()[3]
            out_dc = length.upp_outcoil() * wire.prop_out()[3]
            lowout_dc = length.low_outcoil() * wire.prop_out()[3]
            print('inner, upper outer coil Dc resistance as per datasheet (in ohms) :', inn_dc, out_dc)
        inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                           circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material,
                                           edit_mode=4, group=1, label1=wire.prop_inn()[1], label2=geo.inncoil()[0], blockname=wire.prop_inn()[2],
                                           turns_pr_layer=position.inncoil()[4], simulation_type=self.sim_type)
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                         circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=3, label1=wire.prop_out()[1],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.upp_outcoil()[4], simulation_type=self.sim_type)
        lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[2], x2=position.low_outcoil()[0], y2=position.low_outcoil()[1],
                                         circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=4, label1=wire.prop_out()[0],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.low_outcoil()[4], simulation_type=self.sim_type)
        magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')

        res = coil.Coil_prop(pre_simulation.parameters()[0])
        inn_prop = res.inncoil()
        uppout_prop = res.uppout()
        lowout_prop = res.lowout()
        mag_prop = res.magnet()

        move_group = femm_model.Femm_move(groups = [1,2], x_dist=0, y_dist=pre_simulation.parameters()[2])

        for i in range(0, pre_simulation.parameters()[0] + 1):
            print('coil position (from centre) : ', pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
            inn_prop['Inncoil_position'][i] = pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i
            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('VC_ETpf_LIP.fem')
            femm.mi_analyze()
            femm.mi_loadsolution()

            femm.mo_groupselectblock(3)
            UppOut_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            femm.mo_groupselectblock(4)
            LowOut_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            femm.mo_groupselectblock(2)
            Magn_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()

            UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(position.upp_outcoil()[5])
            uppout_prop['UppOut_voltage'][i] = UppOutCoil_V
            uppout_prop['UppOut_current'][i] = UppOutCoil_I
            uppout_prop['UppOut_flux'][i] = UppOutCoil_FluxLink

            LowOutCoil_I, LowOutCoil_V, LowOutCoil_FluxLink = femm.mo_getcircuitproperties(position.low_outcoil()[5])
            lowout_prop['LowOut_voltage'][i] = LowOutCoil_V
            lowout_prop['LowOut_current'][i] = LowOutCoil_I
            lowout_prop['LowOut_flux'][i] = LowOutCoil_FluxLink

            InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
            inn_prop['Inncoil_voltage'][i] = InnCoil_V
            inn_prop['Inncoil_current'][i] = InnCoil_I
            inn_prop['Inncoil_flux'][i] = InnCoil_FluxLink

            uppout_prop['UppOut_force'][i] = UppOut_Force19
            lowout_prop['LowOut_force'][i] = LowOut_Force19
            mag_prop['Magnet_forces'][i] = Magn_Force19

            if self.sim_type == 'semi_analytical':
                mag_field = fields.B_field(40, 45, 0.01, 0.1, self.filename, input_par3, input_par2, input_par1, inn_prop['Inncoil_voltage'][0], inn_prop['Inncoil_flux'][0]
                                           ,uppout_prop['UppOut_voltage'][0], uppout_prop['UppOut_flux'][0])
                mag_field.calculate()
                print('field calculation completed')
                sys.exit()

            move_group = femm_model.Femm_move(groups=[1, 2], x_dist=0, y_dist=pre_simulation.parameters()[1])

        Upp_Inductance = abs(uppout_prop['UppOut_flux'] / uppout_prop['UppOut_current'])
        Upp_resistance = abs(uppout_prop['UppOut_voltage'] / uppout_prop['UppOut_current'])
        print("magnet force :", mag_prop['Magnet_forces'])
        print('upper coil ind, imp :', Upp_Inductance[1], Upp_resistance[1])
        plt.plot(inn_prop['Inncoil_position'], abs(mag_prop['Magnet_forces']), 'o-')
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylabel('Magnet Force [N]')
        plt.show()

        if self.save:
            np.savez_compressed(self.filename,Design_type=input_par3, Design = input_par2, Input_parameters = input_par1,
                                Innercoil_config=position.inncoil(), UpperOutcoil_config=position.upp_outcoil(), LowerOutercoil_config=position.low_outcoil(),
                                UOC_forces = uppout_prop['UppOut_force'], LOC_forces = lowout_prop['LowOut_force'], Mag_forces = mag_prop['Magnet_forces'],
                                IC_currents = inn_prop['Inncoil_current'], UOC_currents=uppout_prop['UppOut_current'], LOC_currents = lowout_prop['LowOut_current'],
                                UOC_voltages = uppout_prop['UppOut_voltage'], LOC_voltages = lowout_prop['LowOut_voltage'], IC_voltages = inn_prop['Inncoil_voltage'],
                                IC_positions = inn_prop['Inncoil_position'], IC_flux=inn_prop['Inncoil_flux'], UOC_flux=uppout_prop['UppOut_flux'], LOC_flux=lowout_prop['LowOut_flux'],
                                Inn_Uppout_Lowout_DCR_as_per_catalog = [inn_dc, out_dc, lowout_dc])
