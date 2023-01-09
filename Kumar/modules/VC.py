import femm
import design
import femm_model
import coil
import feed
import numpy as np
import matplotlib.pyplot as plt

class Analysis():
    def __init__(self,save, sim_range: list, default, filename: str, design_type: None, parameter1=None):
        self.save = save
        self.sim_range = sim_range
        self.filename = filename
        self.parameter1 = parameter1
        self.design_type = design_type
        self.default = default
    def simulate(self):
        femm.openfemm()  # The package must be initialized with the openfemm command.
        femm.newdocument(0)  # We need to create a new Magnetostatics document to work on.
        value = feed.data
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file=self.filename)
        sensor = design.Sensortype(InnCoilCurrent=0, Simfreq=0, OutCoilCurrent=1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
        else:
            geo = design.Geometry(inn_ht=24, inn_rad=self.parameter1, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=35, out_layers=5, out_dist=54.5, mag_len=40, mag_dia=10, ver_shi=0)
        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3], geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3],
                                 geo.mag()[2], wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1], geo.mag()[0], geo.mag()[1])
        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1], position.inncoil()[3], geo.outcoil()[2],
                             geo.outcoil()[1], wire.prop32()[0], wire.prop32()[1], position.upp_outcoil()[3])
        class Modelling():
            def __init__(self):
                pass
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                               circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material,
                                               edit_mode=4, group=1, label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                               turns_pr_layer=position.inncoil()[4])
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                             circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                             edit_mode=4, group=3, label1=wire.prop32()[1],
                                             label2=geo.outcoil()[0], blockname=wire.prop32()[2], turns_pr_layer=position.upp_outcoil()[4])
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                             circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                             edit_mode=4, group=4, label1=wire.prop32()[0],
                                             label2=geo.outcoil()[0], blockname=wire.prop32()[2], turns_pr_layer=position.low_outcoil()[4])
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            bc = femm_model.Femm_bc()

            UppOutCoil_Forces = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            LowOutCoil_Forces = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            Magnet_Forces = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            InnCoil_Positions = np.zeros(pre_simulation.parameters()[0] + 1)
            UppOutCoil_Voltages = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            InnCoil_Voltages = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            UppOutCoil_Currents = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            LowOutCoil_Currents = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            InnCoil_Currents = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            UppOutCoil_Flux = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            LowOutCoil_Flux = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)
            InnCoil_Flux = np.zeros(pre_simulation.parameters()[0] + 1).astype(complex)

            femm.mi_selectgroup(1)
            femm.mi_selectgroup(2)
            femm.mi_movetranslate(0, pre_simulation.parameters()[2])
            femm.mi_clearselected()
        modelled = Modelling()
        class Computational_loop():
            def __init__(self):
                pass
            for i in range(0, pre_simulation.parameters()[0] + 1):
                print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
                modelled.InnCoil_Positions[i] = pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i
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
                modelled.UppOutCoil_Voltages[i] = UppOutCoil_V
                modelled.UppOutCoil_Currents[i] = UppOutCoil_I
                modelled.UppOutCoil_Flux[i] = UppOutCoil_FluxLink
                LowOutCoil_I, LowOutCoil_V, LowOutCoil_FluxLink = femm.mo_getcircuitproperties(position.low_outcoil()[5])
                modelled.LowOutCoil_Voltages[i] = LowOutCoil_V
                modelled.LowOutCoil_Currents[i] = LowOutCoil_I
                modelled.LowOutCoil_Flux[i] = LowOutCoil_FluxLink
                InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
                modelled.InnCoil_Voltages[i] = InnCoil_V
                modelled.InnCoil_Currents[i] = InnCoil_I
                modelled.InnCoil_Flux[i] = InnCoil_FluxLink
                modelled.UppOutCoil_Forces[i] = UppOut_Force19
                modelled.LowOutCoil_Forces[i] = LowOut_Force19
                modelled.Magnet_Forces[i] = Magn_Force19

                femm.mi_selectgroup(1)
                femm.mi_selectgroup(2)
                femm.mi_movetranslate(0, pre_simulation.parameters()[1])
                femm.mi_clearselected()
        loop = Computational_loop()
        Low_Inductance = abs(modelled.LowOutCoil_Flux / modelled.LowOutCoil_Currents)
        Low_resistance = abs(modelled.LowOutCoil_Voltages / modelled.LowOutCoil_Currents)
        print("average Low out coil Ind, res is :", sum(Low_Inductance) / len(Low_Inductance), sum(Low_resistance) / len(Low_resistance))
        class Results():
            def __init__(self):
                pass
            plt.plot(modelled.InnCoil_Positions, abs(modelled.Magnet_Forces), 'o-')
            plt.xlabel('Inner Coil Position [mm]')
            plt.ylabel('Magnet Force [N]')
            plt.show()
        results = Results()
        np.savez_compressed(self.filename, IC_positions = modelled.InnCoil_Positions, UOC_forces = modelled.UppOutCoil_Forces, LOC_forces = modelled.LowOutCoil_Forces, Mag_forces = modelled.Magnet_Forces, IC_flux = modelled.InnCoil_Flux,
          IC_currents = modelled.InnCoil_Currents, UOC_currents=modelled.UppOutCoil_Currents, LOC_currents = modelled.LowOutCoil_Currents, LOC_voltages = modelled.LowOutCoil_Voltages, IC_voltages = modelled.InnCoil_Voltages)
