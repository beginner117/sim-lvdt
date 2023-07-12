import femm
import design
import femm_model
import coil
import feed
import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self,save, sim_range: list, default, filename: str, design_type=None, parameter1=None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
    def simulate(self):
        print(self.parameter1)
        femm.openfemm()  # The package must be initialized with the openfemm command.
        femm.newdocument(0)  # We need to create a new Magnetostatics document to work on.
        value = feed.data
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=self.parameter1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        input_par1 = {'TotalSteps_StepSize_Offset': self.sim_range, 'uppercoil Diameter_Insulation_Wiretype': wire.prop_out(),
                      'innercoil Diameter_Insulation_Wiretype': wire.prop_inn(), 'Innercoil_current': sensor.para()[0], 'Frequency': sensor.para()[1],
                      'Outercoil_current': sensor.para()[2], 'Magnet_material':wire.mag_mat()}
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par2 = 'type'+self.design_type
        else:
            input_par2 = {'inn coil_height':5.2, 'inn coil_radius':10, 'inn coil_layers':1, 'inn coil_distance':0, 'out coil_height':5.2, 'out coil_radius':10, 'out coil_layers':1,
                          'out coil_distance':0, 'mag_length':40, 'mag_diameter':10, 'ver_shi':0}
            geo = design.Geometry(input_par2['inn coil_height'], input_par2['inn coil_radius'], input_par2['inn coil_layers'], input_par2['inn coil_distance'],
                                  input_par2['out coil_height'], input_par2['out coil_radius'], input_par2['out coil_layers'], input_par2['out coil_distance'],
                                  input_par2['mag_length'], input_par2['mag_diameter'], input_par2['ver_shi'])
        other_par = {'inner coil current_frequency_wire': [sensor.para()[0], sensor.para()[1], wire.inncoil_material],
                     'outer coil_current_frequency_wire': [sensor.para()[2], sensor.para()[1], wire.outcoil_material]}
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2], inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1], out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0], mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3], out_layers=geo.outcoil()[2],
                             out_rad=geo.outcoil()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], outwind_pr_layer=position.upp_outcoil()[3])
        print(position.inncoil(), position.upp_outcoil())
        if wire.prop_out()[3] and wire.prop_inn()[3]:
            inn_dc = length.inncoil() * wire.prop_inn()[3]
            out_dc = length.upp_outcoil() * wire.prop_out()[3]
            lowout_dc = length.low_outcoil() * wire.prop_out()[3]

        inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                           circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material,
                                           edit_mode=4, group=1, label1=wire.prop_inn()[1], label2=geo.inncoil()[0], blockname=wire.prop_inn()[2],
                                           turns_pr_layer=position.inncoil()[4])
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                         circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=3, label1=wire.prop_out()[1], label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.upp_outcoil()[4])
        lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                         circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=4, label1=wire.prop_out()[0],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.low_outcoil()[4])
        magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4,
                                           group=2, label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')

        res = coil.Coil_prop(pre_simulation.parameters()[0])
        inn_prop = res.inncoil()
        uppout_prop = res.uppout()
        lowout_prop = res.lowout()

        move_group = femm_model.Femm_move(groups = [1,2], x_dist=0, y_dist=pre_simulation.parameters()[2])
        for_def = []
        for_imp = []

        for i in range(0, pre_simulation.parameters()[0] + 1):
            print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
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
            #lowout_prop['LowOut_force'][i] = LowOut_Force19
            inn_prop['Inncoil_force'][i] = Magn_Force19

            mag_fie_x_lower = [] ; mag_fie_y_lower = [] ; gri_x_lower = [] ; gri_y_lower = []
            gri_x = [] ; mag_fie_x = [] ; mag_fie_y = [] ; gri_y = []
            def_force = [] ; imp_force = [] ; def_force_ver = [] ; imp_force_ver = []
            rot_x = [] ; rot_y = [] ; rot_x_lower = [] ; rot_y_lower= []
            turns_per_layer = int(position.upp_outcoil()[3])

            for item in range(0, geo.outcoil()[2]):
                for j in range(0, turns_per_layer):
                    grid_pt = [geo.outcoil()[1] + (item * (wire.prop_out()[0]+2*wire.prop_out()[1])), (geo.outcoil()[3]+geo.outcoil()[0])/2 - (j * (wire.prop_out()[0]+2*wire.prop_out()[1]))]
                    grid_pt_lower = [geo.outcoil()[1] + (item * (wire.prop_out()[0]+2*wire.prop_out()[1])), -(geo.outcoil()[3]+geo.outcoil()[0])/2 + (j * (wire.prop_out()[0]+2*wire.prop_out()[1]))]

                    b_field = femm.mo_getb(grid_pt[0], grid_pt[1])
                    b_field_lower = femm.mo_getb(grid_pt_lower[0], grid_pt_lower[1])

                    gri_x.append(grid_pt[0])
                    gri_x_lower.append(grid_pt_lower[0])
                    gri_y.append(grid_pt[1])
                    gri_y_lower.append(grid_pt_lower[1])

                    mag_fie_x.append(b_field[0])
                    mag_fie_y.append(b_field[1])
                    mag_fie_x_lower.append(b_field_lower[0])
                    mag_fie_y_lower.append(b_field_lower[1])

                    g = (2*np.pi * grid_pt[0] * b_field[0]*sensor.para()[2]) / (10 ** 3)
                    g_lower = (2*np.pi * grid_pt_lower[0] * b_field_lower[0]*sensor.para()[2]) / (10 ** 3)
                    def_force.append(g - g_lower)

                    angle = 0
                    theta = (angle / 180) * np.pi
                    rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                    c = np.dot(rotMatrix, np.array(b_field))
                    c_lower = np.dot(rotMatrix, np.array(b_field_lower))

                    rot_x.append(c[0])
                    rot_y.append(c[1])
                    rot_x_lower.append(c_lower[0])
                    rot_y_lower.append(c_lower[1])
                    f = (6.28 * grid_pt[0] * c[0]*sensor.para()[2]) / (10 ** 3)
                    f_lower = (6.28 * grid_pt_lower[0] * c_lower[0]*sensor.para()[2]) / (10 ** 3)
                    imp_force.append(f-f_lower)

            print('default force:', sum(def_force), 'updated force:', sum(imp_force))

            for_def.append(sum(def_force))
            for_imp.append(sum(imp_force))

            move_group = femm_model.Femm_move(groups=[1, 2], x_dist=0, y_dist=pre_simulation.parameters()[1])
        print('angle:',self.parameter1, 'default force1 :', for_def, 'updated force1:', for_imp)

        plt.quiver(gri_x, gri_y, mag_fie_x, np.zeros(turns_per_layer*geo.outcoil()[2]), color='g', label='default', alpha=0.5)
        plt.quiver(gri_x, gri_y, rot_x, np.zeros(turns_per_layer*geo.outcoil()[2]),color = 'b', label = 'rotated', alpha = 0.3)
        plt.quiver(gri_x_lower, gri_y_lower, mag_fie_x_lower,  np.zeros(turns_per_layer*geo.outcoil()[2]), color = 'g', alpha = 0.5)
        plt.quiver(gri_x_lower, gri_y_lower, rot_x_lower, np.zeros(turns_per_layer*geo.outcoil()[2]), color = 'b', alpha = 0.3)
        plt.title('Magnetic Field (rotated anticlockwise {})'.format(angle))
        plt.legend()
        plt.grid()
        plt.show()

        if self.save:
            np.savez_compressed(self.filename, Design=input_par2, Input_parameters=input_par1, Input_config=other_par, Innercoil_config=position.inncoil(), UpperOutcoil_config=position.upp_outcoil(),
                                LowerOutercoil_config=position.low_outcoil(), UOC_forces=uppout_prop['UppOut_force'], LOC_forces=lowout_prop['LowOut_force'], Mag_forces=inn_prop['Inncoil_force'],
                                IC_currents=inn_prop['Inncoil_current'], UOC_currents=uppout_prop['UppOut_current'], LOC_currents=lowout_prop['LowOut_current'], UOC_voltages=uppout_prop['UppOut_voltage'],
                                LOC_voltages=lowout_prop['LowOut_voltage'], IC_voltages=inn_prop['Inncoil_voltage'], IC_positions=inn_prop['Inncoil_position'], IC_flux=inn_prop['Inncoil_flux'],
                                UOC_flux=uppout_prop['UppOut_flux'], LOC_flux=lowout_prop['LowOut_flux'], Inn_Uppout_Lowout_DCR_as_per_catalog=[inn_dc, out_dc, lowout_dc])
