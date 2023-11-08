import femm
import design
import femm_model
import coil
import feed
import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, save, sim_range:list, default, filename:str, design_type:None, parameter1:None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
    def simulate(self):
        femm.openfemm()
        femm.newdocument(0)
        value = feed.data
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=self.parameter1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        block = design.Blocks()
        if self.default == 'yes':
            geo = design.Geometry_yoke(value[self.design_type]["inn_ht"], value[self.design_type]["lowinn_ht"], value[self.design_type]["inn_rad"], value[self.design_type]["inn_layers"], value[self.design_type]["inn_dist"], value[self.design_type]["out_ht"], value[self.design_type]["out_rad"],
                                   value[self.design_type]["out_layers"], value[self.design_type]["out_dist"], value[self.design_type]["mag_len"], value[self.design_type]["mag_dia"], value[self.design_type]["ver_shi"])
            input_par = 'design type : ' + self.design_type + 'with YOKE'
        else:
            input_par = {'inn_ht': 18, 'lowinn_ht': 23, 'inn_rad': 21, 'inn_layers': 6, 'inn_dist': 60.5, 'out_ht': 13.5,
     'out_rad': 31.5, 'out_layers': 5, 'out_dist': 14.5, 'mag_len': 0, 'mag_rad': 0, 'ver_shi': 0}
            geo = design.Geometry_yoke(innUP_ht=input_par['inn_ht'], innLOW_ht=input_par['lowinn_ht'],  inn_rad=input_par['IC_radius'],
                                  inn_layers=input_par['IC_layers'], inn_dist=input_par['IC_distance'],
                                  out_ht=input_par['OC_height'], out_rad=input_par['OC_radius'],
                                  out_layers=input_par['OC_layers'], out_dist=input_par['OC_distance'],
                                  mag_ht=input_par['mag_len'], mag_rad=input_par['mag_rad'],
                                  ver_shi=input_par['ver_shi'])

        Low_Inncoil_OutRadius = geo.Low_Inncoil()[1] + (
                    (wire.prop31()[0] + wire.prop31()[1] * 2) * geo.Low_Inncoil()[2])
        Low_Inncoil_Lowend = -1 * (geo.Low_Inncoil()[3] + (geo.Low_Inncoil()[0]) / 2)
        Low_Inncoil_Uppend = Low_Inncoil_Lowend + geo.Low_Inncoil()[0]
        Low_Inncoil_NrWind_p_Layer = (geo.Upp_Inncoil()[0]) / (wire.prop31()[0] + wire.prop31()[1] * 2)
        Low_Inncoil_NrWindings = Low_Inncoil_NrWind_p_Layer * geo.Upp_Inncoil()[2]
        Low_Inncoil_Circuit = "Low_Inncoil_Circuit"

        class Yoke():
            def __init__(self):
                pass
            def block1(self):
                b1_lowend = -1 * (
                            geo.Low_Inncoil()[3] + (block.b3()[1]) / 2 + block.b4()[1] + geo.mag()[0] + block.b6()[1])
                b1_uppend = b1_lowend + block.b1()[1]
                b1_innrad = block.yokeinnrad
                b1_outrad = b1_innrad + block.b1()[0]
                return [b1_innrad, b1_uppend, b1_outrad, b1_lowend]

            def block2(self):
                b2_innrad = block.yokeinnrad + block.b1_l
                b2_uppend = block.yokeuppend
                b2_lowend = b2_uppend - block.b2_h
                b2_outrad = b2_innrad + block.b2_l
                return [b2_innrad, b2_uppend, b2_outrad, b2_lowend]

            def block3(self):
                b3_innrad = geo.Low_Inncoil()[1] + block.innyoke_gap
                b3_outrad = b3_innrad + block.b3_l
                b3_uppend = block.yokeuppend
                b3_lowend = b3_uppend - block.b3_h
                return [b3_innrad, b3_uppend, b3_outrad, b3_lowend]

            def block4(self):
                b4_innrad = block.yokeoutrad - block.b4_l
                b4_uppend = block.yokeuppend - block.b3_h
                b4_outrad = b4_innrad + block.b4_l
                b4_lowend = b4_uppend - block.b4_h
                return [b4_innrad, b4_uppend, b4_outrad, b4_lowend]

            def block5(self):
                b5_innrad = block.yokeoutrad - geo.mag_rad - block.b5_l
                b5_uppend = block.yokeuppend - block.b3_h - block.b4_h
                b5_outrad = b5_innrad + block.b5_l
                b5_lowend = b5_uppend - block.b5_h
                return [b5_innrad, b5_uppend, b5_outrad, b5_lowend]

            def block6(self):
                b6_innrad = block.yokeoutrad - geo.mag()[1]
                b6_uppend = block.yokeuppend - block.b3_h - block.b4_h - geo.mag()[0]
                b6_outrad = b6_innrad + block.b6_l
                b6_lowend = b6_uppend - block.b6_h
                return [b6_innrad, b6_uppend, b6_outrad, b6_lowend]

            def block7(self):
                b7_innrad = block.yokeinnrad + block.b1_l
                b7_outrad = b7_innrad + block.b7_l
                b7_lowend = block.yokeuppend - block.b3_h - block.b4_h - geo.mag()[0] - block.b6_h
                b7_uppend = b7_lowend + block.b7_h
                return [b7_innrad, b7_uppend, b7_outrad, b7_lowend]

            def mag(self):
                mag_innrad = block.yokeoutrad - geo.mag()[1]
                mag_outrad = mag_innrad + geo.mag()[1]
                mag_uppend = block.yokeuppend - block.b3_h - block.b4_h
                mag_lowend = mag_uppend - geo.mag()[0]
                # mag_lowend = block.yokeuppend - (block.b1()[1])/2 - (geo.mag()[0])/2
                # mag_uppend = block.yokeuppend - (block.b1()[1])/2 + (geo.mag()[0])/2
                return [mag_innrad, mag_uppend, mag_outrad, mag_lowend]

        yoke = Yoke()
        material = wire.yoke_mat()
        inncoil_str = femm_model.Femm_coil(x1=geo.Low_Inncoil()[1], y1=Low_Inncoil_Uppend, x2=Low_Inncoil_OutRadius,
                                           y2=Low_Inncoil_Lowend, circ_name=Low_Inncoil_Circuit,
                                           circ_current=sensor.para()[0], circ_type=1,
                                           material=wire.inncoil_material, edit_mode=4, group=1,
                                           label1=wire.prop_inn()[1],
                                           label2=geo.Low_Inncoil()[1], blockname=wire.prop_inn()[2],
                                           turns_pr_layer=Low_Inncoil_NrWind_p_Layer)
        print("startpoint is ", geo.Low_Inncoil()[1])
        block1 = femm_model.Femm_block(x1=yoke.block1()[0], y1=yoke.block1()[1], x2=yoke.block1()[2],
                                           y2=yoke.block1()[3], material=material, edit_mode=4, group=3,
                                           label1=block.b1_l, label2=block.b1_h)
        print('simulating block 2')
        block2 = femm_model.Femm_block(x1=yoke.block2()[0], y1=yoke.block2()[1], x2=yoke.block2()[2],
                                       y2=yoke.block2()[3], material=material, edit_mode=4, group=4,
                                       label1=block.b2_l, label2=block.b2_h)
        print('simulating block 3')
        block3 = femm_model.Femm_block(x1=yoke.block3()[0], y1=yoke.block3()[1], x2=yoke.block3()[2],
                                       y2=yoke.block3()[3], material=material, edit_mode=4, group=5,
                                       label1=block.b3_l, label2=block.b3_h)
        print('simulating block 4')
        block4 = femm_model.Femm_block(x1=yoke.block4()[0], y1=yoke.block4()[1], x2=yoke.block4()[2],
                                       y2=yoke.block4()[3], material=material, edit_mode=4, group=6,
                                       label1=block.b4_l, label2=block.b4_h)
        print('simulating block 5')
        block5 = femm_model.Femm_block(x1=yoke.block5()[0], y1=yoke.block5()[1], x2=yoke.block5()[2],
                                       y2=yoke.block5()[3], material=material, edit_mode=4, group=7,
                                       label1=block.b5_l, label2=block.b5_h)
        print('simulating block 6')
        block6 = femm_model.Femm_block(x1=yoke.block6()[0], y1=yoke.block6()[1], x2=yoke.block6()[2],
                                       y2=yoke.block6()[3], material=material, edit_mode=4, group=8,
                                       label1=block.b6_l, label2=block.b6_h)
        print('simulating block 7')
        block7 = femm_model.Femm_block(x1=yoke.block7()[0], y1=yoke.block7()[1], x2=yoke.block7()[2],
                                       y2=yoke.block7()[3], material=material, edit_mode=4, group=9,
                                       label1=block.b7_l, label2=block.b7_h)
        print('simulating magnet')
        magnet = femm_model.Femm_magnet(x1=yoke.mag()[0], y1=yoke.mag()[1], x2=yoke.mag()[2],
                                       y2=yoke.mag()[3], material=wire.mag_mat(), edit_mode=4, group=10,
                                       label1=geo.mag()[1], label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=200, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10,
                                material='Air')

        Magnet_Forces1 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces_m = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces_c = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces2 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces3 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces4 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces5 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces6 = np.zeros(self.sim_range[0] + 1)
        Magnet_Forces7 = np.zeros(self.sim_range[0]+ 1)
        tot_mag = np.zeros(self.sim_range[0] + 1)
        InnCoil_Positions = np.zeros(self.sim_range[0] + 1)
        MetaData = np.zeros(self.sim_range[0] + 1)
        femm.mi_selectgroup(3)
        femm.mi_movetranslate(0, self.sim_range[2])
        femm.mi_clearselected()

        for i in range(0, self.sim_range[0] + 1):
            print(self.sim_range[2] + self.sim_range[1] * i)
            InnCoil_Positions[i] = self.sim_range[2] + (self.sim_range[1] * i)
            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('Yoke position_ETpf_LIP.fem')
            femm.mi_analyze()
            femm.mi_loadsolution()

            femm.mo_groupselectblock(5)
            Magn_Force_m = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces_m[i] = Magn_Force_m

            femm.mo_groupselectblock(3)
            Magn_Force_c = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces_c[i] = Magn_Force_c

            femm.mo_groupselectblock(6)
            Magn_Force1 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces1[i] = Magn_Force1

            femm.mo_groupselectblock(7)
            Magn_Force2 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces2[i] = Magn_Force2

            femm.mo_groupselectblock(8)
            Magn_Force3 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces3[i] = Magn_Force3

            femm.mo_groupselectblock(9)
            Magn_Force4 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces4[i] = Magn_Force4

            femm.mo_groupselectblock(10)
            Magn_Force5 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces5[i] = Magn_Force5

            femm.mo_groupselectblock(11)
            Magn_Force6 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces6[i] = Magn_Force6

            femm.mo_groupselectblock(12)
            Magn_Force7 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            Magnet_Forces7[i] = Magn_Force7

            femm.mo_groupselectblock(6)
            femm.mo_groupselectblock(7)
            femm.mo_groupselectblock(8)
            femm.mo_groupselectblock(9)
            femm.mo_groupselectblock(10)
            femm.mo_groupselectblock(11)
            femm.mo_groupselectblock(12)
            total = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            tot_mag[i] = total

            femm.mi_selectgroup(3)
            femm.mi_movetranslate(0, self.sim_range[1])
            femm.mi_clearselected()

        plt.style.use(['science', 'grid', 'notebook'])

        #plt.plot(np.array(InnCoil_Positions), np.array(Magnet_Forces_c), "o--", label="inn")
        plt.plot(np.array(InnCoil_Positions), np.array(Magnet_Forces_m), "o--", label="mag")
        plt.ylabel('Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        plt.show()