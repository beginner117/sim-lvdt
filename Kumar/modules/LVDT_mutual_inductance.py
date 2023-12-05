import femm
import design
import femm_model
import coil
import feed
import numpy as np
class Analysis1:
    def __init__(self, save, default, offset, design_type=None, filename1=None,  parameter1=None):
        self.offset = offset
        self.save = save
        self.filename1 = filename1
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
    def simulate(self):
        if self.default=='yes':
            value = feed.data
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par2 = 'design type : '+self.design_type
        else:
            input_par2 = {'IC_height':18, 'IC_radius':21, 'IC_layers':self.parameter1, 'IC_distance':0, 'OC_height':13.5, 'OC_radius':31.5, 'OC_layers':5, 'OC_distance':14.5, 'mag_len':0, 'mag_dia':0, 'ver_shi':0}
            geo = design.Geometry(input_par2['IC_height'], input_par2['IC_radius'], input_par2['IC_layers'], input_par2['IC_distance'], input_par2['OC_height'], input_par2['OC_radius'],
                                  input_par2['OC_layers'], input_par2['OC_distance'], input_par2['mag_len'], input_par2['mag_dia'], input_par2['ver_shi'])
        wire = design.Wiretype(outcoil_material='electrisola_1b', inncoil_material='electrisola_2a', magnet_material="N40")  # can be changed
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

        other_par = {'current(amps)_AC frequency_inner wire_outer wire': [0.02, 10000, wire.inncoil_material, wire.outcoil_material]}
        #inner_outer_lower_current
        trials = [[0.02, 0, 0, 10000], [0, 0.02, 0, 10000], [0, 0, 0.02, 10000], [0.02, 0.02, 0, 10000], [0, 0.02, 0.02, 10000], [0.02, 0, 0.02, 10000], [1,1,1, 0]]
        self_ind = []
        mut_ind = []
        imp = []
        dc_r = []
        for i in range(len(trials)):
            femm.openfemm()   # The package must be initialized with the openfemm command.
            femm.newdocument(0)   # We need to create a new Magnetostatics document to work on.
            femm.mi_probdef(trials[i][3], 'millimeters', 'axi', 1.0e-10)

            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1], circ_name=position.inncoil()[5],
                                               circ_current=trials[i][0], circ_type=1, material=wire.inncoil_material, edit_mode=4, group=1, label1=wire.prop_inn()[1],
                                               label2=geo.inncoil()[0], blockname=wire.prop_inn()[2], turns_pr_layer=position.inncoil()[4])
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1], circ_name=position.upp_outcoil()[5],
                                             circ_current=trials[i][1], circ_type=1, material=wire.outcoil_material, edit_mode=4, group=3, label1=wire.prop_out()[1],
                                             label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.upp_outcoil()[4])
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[2], x2=position.low_outcoil()[0], y2=position.low_outcoil()[1], circ_name=position.low_outcoil()[5],
                                             circ_current=-trials[i][2], circ_type=1, material=wire.outcoil_material, edit_mode=4, group=4, label1=wire.prop_out()[0],
                                             label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.low_outcoil()[4])
            if geo.mag()[0]>1:
                magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')

            res = coil.Coil_prop(0)
            inn_prop = res.inncoil()
            uppout_prop = res.uppout()
            lowout_prop = res.lowout()
            move_group = femm_model.Femm_move(groups = [1,2], x_dist=0, y_dist=self.offset)

            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('LVDT position_ETpf_LIP.fem')   # We have to give the geometry a name before we can analyze it.
            femm.mi_analyze()   # Now,analyze the problem and load the solution when the analysis is finished
            femm.mi_loadsolution()

            UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(position.upp_outcoil()[5])
            uppout_prop['UppOut_voltage'] = UppOutCoil_V
            uppout_prop['UppOut_current'] = UppOutCoil_I
            uppout_prop['UppOut_flux'] = UppOutCoil_FluxLink

            LowOutCoil_I, LowOutCoil_V, LowOutCoil_FluxLink = femm.mo_getcircuitproperties(position.low_outcoil()[5])
            lowout_prop['LowOut_voltage'] = LowOutCoil_V
            lowout_prop['LowOut_current']= LowOutCoil_I
            lowout_prop['LowOut_flux'] = LowOutCoil_FluxLink

            InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
            inn_prop['Inncoil_voltage'] = InnCoil_V
            inn_prop['Inncoil_current'] = InnCoil_I
            inn_prop['Inncoil_flux'] = InnCoil_FluxLink

            if trials[i][1]==0 and trials[i][2] == 0:
                Inn_Inductance = abs(inn_prop['Inncoil_flux'] / inn_prop['Inncoil_current'])
                Inn_Impedance = abs(inn_prop['Inncoil_voltage'] / inn_prop['Inncoil_current'])
                self_ind.append(Inn_Inductance)
                imp.append(Inn_Impedance)
            if trials[i][0]==0 and trials[i][2] == 0:
                Out_Impedance = abs(uppout_prop['UppOut_voltage'] / uppout_prop['UppOut_current'])
                Out_Inductance = abs(uppout_prop['UppOut_flux'] / uppout_prop['UppOut_current'])
                self_ind.append(Out_Inductance)
                imp.append(Out_Impedance)
            if trials[i][0]==0 and trials[i][1] == 0:
                Low_Impedance = abs(lowout_prop['LowOut_voltage'] / lowout_prop['LowOut_current'])
                Low_Inductance = abs(lowout_prop['LowOut_flux'] / lowout_prop['LowOut_current'])
                self_ind.append(Low_Inductance)
                imp.append(Low_Impedance)
            if trials[i][0]!= 0 and trials[i][1] != 0 and trials[i][2] == 0:
                Inn_Inductance = abs(inn_prop['Inncoil_flux'] / inn_prop['Inncoil_current'])
                Out_Inductance = abs(uppout_prop['UppOut_flux'] / uppout_prop['UppOut_current'])
                mut_ind.append([Inn_Inductance, Out_Inductance])
                #print('Inner & Upper out coil inducatnces when excited :', Inn_Inductance, Out_Inductance)
            if trials[i][1]!= 0 and trials[i][2] != 0 and trials[i][0] == 0:
                Out_Inductance = abs(uppout_prop['UppOut_flux'] / uppout_prop['UppOut_current'])
                Low_Inductance = abs(lowout_prop['LowOut_flux'] / lowout_prop['LowOut_current'])
                mut_ind.append([ Out_Inductance, Low_Inductance])
                #print('Upper & Lower out coil inducatnces when excited :', Out_Inductance, Low_Inductance)
            if trials[i][2]!= 0 and trials[i][0] != 0 and trials[i][1] == 0:
                Low_Inductance = abs(lowout_prop['LowOut_flux'] / lowout_prop['LowOut_current'])
                Inn_Inductance = abs(inn_prop['Inncoil_flux'] / inn_prop['Inncoil_current'])
                mut_ind.append([Low_Inductance, Inn_Inductance])
                #print('Lower out & Inner coil inducatnces when excited :', Low_Inductance, Inn_Inductance)
            if trials[i][2] == 1 and trials[i][0] ==1 and trials[i][1] == 1:
                Inn_Impedance = abs(inn_prop['Inncoil_voltage'] / inn_prop['Inncoil_current'])
                Out_Impedance = abs(uppout_prop['UppOut_voltage'] / uppout_prop['UppOut_current'])
                Low_Impedance = abs(lowout_prop['LowOut_voltage'] / lowout_prop['LowOut_current'])
                dc_r = [Inn_Impedance, Out_Impedance, Low_Impedance]

        mut = []
        k_f = []
        for i in range(0,3):
            m = self_ind[i]+self_ind[(i+1)%3]-mut_ind[i][0]-mut_ind[i][1]
            k = m/(2*np.sqrt(self_ind[i]*self_ind[(i+1)%3]))
            mut.append(m)
            k_f.append(k)
        print('total mutual inductances btw 2 coils (IU, UL, LI) in Henries :', mut)
        print('self inductances (H):', self_ind)
        print('impedances (I, U, L) in ohms :', imp)
        print('dc resistance of coils (I, U, L) :', dc_r)
        print('k_factors :', k_f)

        if self.save:
            np.savez_compressed(self.filename1, Design = input_par2, Input_config = other_par, offset = self.offset, self_inductances_Inner_upper_lower = self_ind, mutual_ind_IU_UL_LI=mut, k_factors=k_f)

        return [mut, self_ind, k_f, dc_r]


