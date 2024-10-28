import femm
import design
import femm_model
import coil
import feed
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

class Analysis:
    def __init__(self,save, sim_range: list, default, filename: str, design_type, input_excitation, materials, coil_dimensions=None, parameter1=None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
        self.materials = materials
        self.des_dim = coil_dimensions
        self.input_excitation = input_excitation
    def simulate(self):
        print(self.parameter1)
        femm.openfemm()  # The package must be initialized with the openfemm command.
        femm.newdocument(0)  # We need to create a new Magnetostatics document to work on.
        value = feed.data
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=self.input_excitation[0], Simfreq=self.input_excitation[1], OutCoilCurrent=self.input_excitation[2])
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype(self.materials[1], self.materials[0], magnet_material=self.materials[2])
        input_par1 = {'TotalSteps_StepSize_Offset': self.sim_range, 'uppercoil Diameter_Insulation_Wiretype': wire.prop_out()[:3],
                      'innercoil Diameter_Insulation_Wiretype': wire.prop_inn()[:3], 'Innercoil_current': sensor.para()[0], 'Frequency': sensor.para()[1],
                      'Outercoil_current': sensor.para()[2], 'Magnet_material':wire.mag_mat()}
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par2 = 'type'+self.design_type
        if self.default == 'no':
            try:
                input_par2 = {'IC_height': self.des_dim['inner'][0], 'IC_radius': self.des_dim['inner'][1],
                              'IC_layers': self.des_dim['inner'][2], 'IC_distance': self.des_dim['inner'][3],
                              'OC_height': self.des_dim['outer'][0], 'OC_radius': self.des_dim['outer'][1],
                              'OC_layers': self.des_dim['outer'][2], 'OC_distance': self.des_dim['outer'][3],
                              'mag_len': self.des_dim['magnet'][0], 'mag_dia': self.des_dim['magnet'][1], 'ver_shi': 0}
            except:
                input_par2 = {'IC_height': self.parameter1[0], 'IC_radius': 7, 'IC_layers': 6, 'IC_distance': 0,
                              'OC_height': self.parameter1[1], 'OC_radius': 17, 'OC_layers': 7,
                              'OC_distance': self.parameter1[2], 'mag_len': 30, 'mag_dia': 8, 'ver_shi': 0}
            geo = design.Geometry(input_par2['inn coil_height'], input_par2['inn coil_radius'], input_par2['inn coil_layers'], input_par2['inn coil_distance'],
                                  input_par2['out coil_height'], input_par2['out coil_radius'], input_par2['out coil_layers'], input_par2['out coil_distance'],
                                  input_par2['mag_length'], input_par2['mag_diameter'], input_par2['ver_shi'])
        other_par = {'inner coil current_frequency_wire': [sensor.para()[0], sensor.para()[1], wire.inncoil_material],
                     'outer coil_current_frequency_wire': [sensor.para()[2], sensor.para()[1], wire.outcoil_material]}
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2], inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1], out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0], mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3], out_layers=geo.outcoil()[2],
                             out_rad=geo.outcoil()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], outwind_pr_layer=position.upp_outcoil()[3])
        print('coil config - [Coil_OutRadius, Coil_LowEnd, Coil_UppEnd, Coil_NrWind_p_Layer, Coil_NrWindings, Circuit_name]')
        print('inner coil config :', position.inncoil(), '\nupper outer coil config :', position.upp_outcoil(), '\nlower out coil config :', position.low_outcoil())
        print('inner coil material - ', wire.inncoil_material, ', outer coil material - ', wire.outcoil_material,', magnet material - ', wire.magnet_material)
        print('inner, upper outer, total coil lengths : ', length.inncoil(), length.upp_outcoil(),
              length.inncoil() + (2 * length.upp_outcoil()))
        coil_con = ['Coil_OutRadius', 'Coil_Lowend', 'Coil_Uppend', 'Coil_turns(per layer)', 'Coil_turns total', 'coil_name']
        if wire.prop_out()[3] and wire.prop_inn()[3]:
            inn_dc = length.inncoil() * wire.prop_inn()[3]
            out_dc = length.upp_outcoil() * wire.prop_out()[3]
            lowout_dc = length.low_outcoil() * wire.prop_out()[3]
            print('inner, upper outer coil Dc resistance as per datasheet (in ohms) :', inn_dc, out_dc)
        inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0],
                                           y2=position.inncoil()[1],
                                           circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1,
                                           material=wire.inncoil_material,
                                           edit_mode=4, group=1, label1=wire.prop_inn()[1], label2=geo.inncoil()[0],
                                           blockname=wire.prop_inn()[2],
                                           turns_pr_layer=position.inncoil()[4])
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2],
                                         x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                         circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2][0],
                                         circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=3, label1=wire.prop_out()[1],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2],
                                         turns_pr_layer=position.upp_outcoil()[4])
        lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[2],
                                         x2=position.low_outcoil()[0], y2=position.low_outcoil()[1],
                                         circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2][1],
                                         circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=4, label1=wire.prop_out()[0],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2],
                                         turns_pr_layer=position.low_outcoil()[4])
        magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2],
                                           y2=position.magnet()[1], material=wire.magnet_material, edit_mode=4, group=2,
                                           label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10,
                                material='Air')

        res = coil.Coil_prop(pre_simulation.parameters()[0])
        inn_prop = res.inncoil()
        uppout_prop = res.uppout()
        lowout_prop = res.lowout()
        mag_prop = res.magnet()
        
        move_group = femm_model.Femm_move(groups = [1,2], x_dist=0, y_dist=pre_simulation.parameters()[2])
        for_def = []; for_imp = []; for_theo = []
        mag_field_uppercoil = []; mag_field_lowercoil = []
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
            femm.mo_groupselectblock(1)
            Innercoil_Force19 = femm.mo_blockintegral(19)
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
            inn_prop['Inncoil_force'][i] = Innercoil_Force19
            mag_prop['Magnet_forces'][i] = Magn_Force19

            mag_fie_x_lower = [] ; mag_fie_y_lower = [] ; gri_x_lower = [] ; gri_y_lower = []
            gri_x = [] ; mag_fie_x = [] ; mag_fie_y = [] ; gri_y = []
            def_force = [] ; def_force_ver = [] ; theo_force = []
            mag_field_upper = [] ; mag_field_lower = []
            turns_per_layer = int(position.upp_outcoil()[3])

            for item in range(0, geo.outcoil()[2]):
                for j in range(0, turns_per_layer):
                    grid_pt = [geo.outcoil()[1] + (item * (wire.prop_out()[0]+2*wire.prop_out()[1])), (geo.outcoil()[3]+geo.outcoil()[0])/2 - (j * (wire.prop_out()[0]+2*wire.prop_out()[1]))]
                    grid_pt_lower = [geo.outcoil()[1] + (item * (wire.prop_out()[0]+2*wire.prop_out()[1])), -(geo.outcoil()[3]+geo.outcoil()[0])/2 + (j * (wire.prop_out()[0]+2*wire.prop_out()[1]))]

                    b_field = femm.mo_getb(grid_pt[0], grid_pt[1]); mag_field_upper.append([grid_pt[0], grid_pt[1], b_field[0], b_field[1]])
                    b_field_lower = femm.mo_getb(grid_pt_lower[0], grid_pt_lower[1]); mag_field_lower.append([grid_pt_lower[0], grid_pt_lower[1], b_field_lower[0], b_field_lower[1]])

                    gri_x.append(grid_pt[0])
                    gri_x_lower.append(grid_pt_lower[0])
                    gri_y.append(grid_pt[1])
                    gri_y_lower.append(grid_pt_lower[1])

                    mag_fie_x.append(b_field[0])
                    mag_fie_y.append(b_field[1])
                    mag_fie_x_lower.append(b_field_lower[0])
                    mag_fie_y_lower.append(b_field_lower[1])

                    g = (2*np.pi * grid_pt[0] * b_field[0]*sensor.para()[2][0]) / (10 ** 3)
                    g_lower = (2*np.pi * grid_pt_lower[0] * b_field_lower[0]*sensor.para()[2][1]) / (10 ** 3)
                    def_force.append(g - g_lower)

                    dis1 = ((geo.mag()[0] / 2 - grid_pt[1]) ** 2)/1000000; dis2 = ((geo.mag()[0] / 2 + grid_pt[1]) ** 2)/1000000  #conversion from mm to mts by dividing with 1000000
                    mu = 4*np.pi/1000000; M = 1.2
                    con = -mu * M / (4 * np.pi)
                    f1 = lambda r, theta: (r*(2 * (grid_pt[0]/1000) - (2*r * np.cos(theta))))/2*((r ** 2) + dis1 + ((grid_pt[0]/1000) ** 2) - (2*r * (grid_pt[0]/1000) * np.cos(theta)))**1.5
                    f2 = lambda r, theta: (r * (2 * (grid_pt[0]/1000) - (2 * r * np.cos(theta)))) / 2 * ((r ** 2) + dis2 + ((grid_pt[0]/1000) ** 2) - (2 * r * (grid_pt[0]/1000) * np.cos(theta))) ** 1.5
                    c1 = dblquad(f1, 0, 2*np.pi, 0, geo.mag()[1]/2)
                    c1_2 = dblquad(f2, 0, 2 * np.pi, 0, geo.mag()[1] / 2)
                    mat_for_upp = ((c1[0]+c1_2[0])*2*np.pi*grid_pt[0]*con)/1000
                    dis1_low = ((geo.mag()[0] / 2 - grid_pt_lower[1]) ** 2)/1000000
                    dis2_low = ((geo.mag()[0] / 2 + grid_pt_lower[1]) ** 2)/1000000
                    con = -mu * M / (4 * np.pi)
                    f1_low = lambda r, theta: (r * (2 * (grid_pt_lower[0]/1000) - (2 * r * np.cos(theta)))) / 2 * (
                                (r ** 2) + dis1 + ((grid_pt_lower[0]/1000) ** 2) - (2 * r * (grid_pt_lower[0]/1000) * np.cos(theta))) ** 1.5
                    f2_low = lambda r, theta: (r * (2 * (grid_pt_lower[0]/1000) - (2 * r * np.cos(theta)))) / 2 * (
                                (r ** 2) + dis2 + ((grid_pt_lower[0]/1000) ** 2) - (2 * r * (grid_pt_lower[0]/1000) * np.cos(theta))) ** 1.5
                    c1_low = dblquad(f1_low, 0, 2 * np.pi, 0, geo.mag()[1] / 2000)
                    c1_low_2 = dblquad(f2_low, 0, 2 * np.pi, 0, geo.mag()[1] / 2000)
                    mat_for_low = ((c1_low[0]+c1_low_2[0])*2 * np.pi * grid_pt_lower[0] * con)/1000

                    theo_force.append(mat_for_upp+mat_for_low)


            #print('default force:', sum(np.array(def_force)), 'updated force:', sum(np.array(imp_force)), 'int_for:')
            mag_field_uppercoil.append(mag_field_upper); mag_field_lowercoil.append(mag_field_lower)
            for_def.append(sum(def_force))
            for_theo.append(sum(theo_force))
            move_group = femm_model.Femm_move(groups=[1, 2], x_dist=0, y_dist=pre_simulation.parameters()[1])
        print('semi-analytical', '\nsemi analytical force :', for_def, '\nfemm force:', mag_prop['Magnet_forces'], '\nanalytical force :', for_theo)

        plt.quiver(gri_x, gri_y, mag_fie_x, np.zeros(turns_per_layer*geo.outcoil()[2]), color='g', label='default', alpha=0.5)
        # plt.quiver(gri_x, gri_y, rot_x, np.zeros(turns_per_layer*geo.outcoil()[2]),color = 'b', label = 'rotated', alpha = 0.3)
        plt.quiver(gri_x_lower, gri_y_lower, mag_fie_x_lower,  np.zeros(turns_per_layer*geo.outcoil()[2]), color = 'g', alpha = 0.5)
        # plt.quiver(gri_x_lower, gri_y_lower, rot_x_lower, np.zeros(turns_per_layer*geo.outcoil()[2]), color = 'b', alpha = 0.3)
        #plt.title('Magnetic Field (rotated anticlockwise {})'.format(angle))
        plt.legend()
        plt.grid()
        plt.show()

        plt.plot(np.real(inn_prop['Inncoil_position']), abs(mag_prop['Magnet_forces']), 'o-', label = 'femm')
        plt.plot(np.real(inn_prop['Inncoil_position']), for_def,'o-', label = 'semi-analytical')
        plt.plot(np.real(inn_prop['Inncoil_position']), for_theo, 'o-', label='analytical')
        plt.ylabel('Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        plt.grid()
        plt.show()

        if self.save:
            np.savez_compressed(self.filename, Design = input_par2, Input_parameters = input_par1, coil_config_parameters = coil_con,
                                Innercoil_config=position.inncoil(), UpperOutcoil_config=position.upp_outcoil(), LowerOutercoil_config=position.low_outcoil(),
                                UOC_forces = uppout_prop['UppOut_force'], LOC_forces = lowout_prop['LowOut_force'], IC_forces = inn_prop['Inncoil_force'],
                                Mag_forces=mag_prop['Magnet_forces'], semi_analytical_def = for_def,
                                Magnetic_field_upper = mag_field_uppercoil, Magnetic_field_lower = mag_field_lowercoil,
                                IC_currents = inn_prop['Inncoil_current'], UOC_currents=uppout_prop['UppOut_current'], LOC_currents = lowout_prop['LowOut_current'],
                                UOC_voltages = uppout_prop['UppOut_voltage'], LOC_voltages = lowout_prop['LowOut_voltage'], IC_voltages = inn_prop['Inncoil_voltage'],
                                IC_positions = abs(inn_prop['Inncoil_position']), IC_flux=inn_prop['Inncoil_flux'], UOC_flux=uppout_prop['UppOut_flux'], LOC_flux=lowout_prop['LowOut_flux'],
                                Inn_Uppout_Lowout_DCR_as_per_catalog = [inn_dc, out_dc, lowout_dc])

        return {'coil_positions': np.real(inn_prop['position']), 'magnet_forces': abs(mag_prop['Magnet_forces'])}