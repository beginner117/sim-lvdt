import femm
import design
import femm_model
import coil
import feed
import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, save, sim_range:list, default, filename: str, design_type:None,  parameter1=None):
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
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype(outcoil_material='32 AWG', inncoil_material='32 AWG')
        if self.default == 'yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'],
                                  value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'],
                                  value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'],
                                  value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'],
                                  value[self.design_type]['ver_shi'])
            input_par = 'design type ' + self.design_type
        else:
            input_par = {'inn coil_height':18, 'inn coil_radius':self.parameter1, 'inn coil_layers':6, 'inn coil_distance':0, 'out coil_height':13.5, 'out coil_radius':31.5, 'out coil_layers':5, 'out coil_distance':14.5, 'mag_length':0, 'mag_diameter':0, 'ver_shi':0}
            geo = design.Geometry(input_par['IC_height'], input_par['IC_radius'], input_par['IC_layers'], input_par['IC_distance'],
                                  input_par['OC_height'], input_par['OC_radius'], input_par['OC_layers'], input_par['OC_distance'],
                                  input_par['mag_len'], input_par['mag_dia'], input_par['ver_shi'])
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
        print(position.upp_outcoil())
        print('out dc data :', (162 * length.upp_outcoil()) / 304800)
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2],
                                         x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                         circ_name=position.upp_outcoil()[5],
                                         circ_current=sensor.para()[2], circ_type=1, material=wire.outcoil_material,
                                         edit_mode=4, group=3, label1=wire.prop_out()[1],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2],
                                         turns_pr_layer=position.upp_outcoil()[4])

        magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')
        UppOutCoil_Forces = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
        Magnet_Forces = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
        UppOutCoil_Voltages = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
        UppOutCoil_Currents = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
        UppOutCoil_Flux = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
        UppCoil_Positions = np.zeros(pre_simulation.parameters()[0] + 1)

        femm.mi_selectgroup(3)
        femm.mi_movetranslate(0, pre_simulation.parameters()[2])
        femm.mi_clearselected()

        for i in range(0, pre_simulation.parameters()[0] + 1):
            print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
            UppCoil_Positions[i] = pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i
            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('VC_ETpf_LIP.fem')
            femm.mi_analyze()
            femm.mi_loadsolution()

            femm.mo_groupselectblock(3)
            UppOut_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            femm.mo_groupselectblock(2)
            Magn_Force19 = femm.mo_blockintegral(19)
            femm.mo_clearblock()

            UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(position.upp_outcoil()[5])
            UppOutCoil_Voltages[i] = UppOutCoil_V
            UppOutCoil_Currents[i] = UppOutCoil_I
            UppOutCoil_Flux[i] = UppOutCoil_FluxLink
            UppOutCoil_Forces[i] = UppOut_Force19
            Magnet_Forces[i] = Magn_Force19

            femm.mi_selectgroup(3)
            femm.mi_movetranslate(0, pre_simulation.parameters()[1])
            femm.mi_clearselected()

        Upp_Inductance = abs(UppOutCoil_Voltages / UppOutCoil_Currents)
        Upp_out_power = abs(UppOutCoil_Voltages) * sensor.para()[2]
        upp_power = abs(UppOutCoil_Voltages) * sensor.para()[2]
        print('upp power :', upp_power)
        Upp_Inductance = abs(UppOutCoil_Flux / UppOutCoil_Currents)
        Upp_resistance = abs(UppOutCoil_Voltages / UppOutCoil_Currents)
        print("average Upper out coil Ind, res is :", sum(Upp_Inductance) / len(Upp_resistance), sum(Upp_resistance) / len(Upp_resistance))
        print('upp out res :', abs(Upp_resistance))
        plt.plot(UppCoil_Positions, Magnet_Forces, 'o-')
        plt.xlabel('Coil (centre) Position relative to Magnet (centre) [mm]')
        plt.ylabel('Magnet Force [N]')
        #plt.grid()
        plt.title('Simulated force [Type : I, 1A_DC excitation]')
        plt.show()

