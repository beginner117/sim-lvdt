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
        femm.openfemm()   # The package must be initialized with the openfemm command.
        femm.newdocument(0)   # We need to create a new Magnetostatics document to work on.
        value = feed.data
        pre_simulation = design.Simulation(Nsteps=self.sim_range[0], stepsize=self.sim_range[1], inncoil_offset=self.sim_range[2], data_file =self.filename)
        sensor = design.Sensortype(InnCoilCurrent = 0.02, Simfreq = 10000, OutCoilCurrent = 0) # can be changed
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1e-10)
        wire = design.Wiretype(outcoil_material="32 AWG", inncoil_material="32 AWG") # can be changed
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par = 'design type : '+self.design_type
        else:
            input_par = {'IC_height':18, 'IC_radius':21, 'IC_layers':6, 'IC_distance':0, 'OC_height':13.5, 'OC_radius':31.5, 'OC_layers':self.parameter1, 'OC_distance':14.5, 'mag_len':0, 'mag_dia':0, 'ver_shi':0}
            geo = design.Geometry(input_par['IC_height'], input_par['IC_radius'], input_par['IC_layers'], input_par['IC_distance'], input_par['OC_height'], input_par['OC_radius'],
                                  input_par['OC_layers'], input_par['OC_distance'], input_par['mag_len'], input_par['mag_dia'], input_par['ver_shi'])
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2], inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1], out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0], mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3], out_layers=geo.outcoil()[2], out_rad=geo.outcoil()[1],
                             out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], outwind_pr_layer=position.upp_outcoil()[3])
        print(position.inncoil(), position.upp_outcoil())

        inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1], circ_name=position.inncoil()[5],
                                           circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material, edit_mode=4, group=1, label1=wire.prop_inn()[1],
                                           label2=geo.inncoil()[0], blockname=wire.prop_inn()[2], turns_pr_layer=position.inncoil()[4])
        uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1], circ_name=position.upp_outcoil()[5],
                                         circ_current=sensor.para()[2], circ_type=1, material=wire.outcoil_material, edit_mode=4, group=3, label1=wire.prop_out()[1],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.upp_outcoil()[4])
        lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2], circ_name=position.low_outcoil()[5],
                                         circ_current=-sensor.para()[2], circ_type=1, material=wire.outcoil_material, edit_mode=4, group=4, label1=wire.prop_out()[0],
                                         label2=geo.outcoil()[0], blockname=wire.prop_out()[2], turns_pr_layer=position.low_outcoil()[4])

        if geo.mag()[0]>1:
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
        bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')

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

        for i in range(0, pre_simulation.parameters()[0] + 1):
            print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
            InnCoil_Positions[i] = pre_simulation.parameters()[2] + (pre_simulation.parameters()[1] * i)

            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview() # We have to give the geometry a name before we can analyze it.
            femm.mi_saveas('LVDT position_ETpf_LIP.fem')  # Now,analyze the problem and load the solution when the analysis is finished
            femm.mi_analyze()
            femm.mi_loadsolution()

            UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(position.upp_outcoil()[5])
            UppOutCoil_Voltages[i] = UppOutCoil_V
            UppOutCoil_Currents[i] = UppOutCoil_I
            UppOutCoil_Flux[i] = UppOutCoil_FluxLink

            LowOutCoil_I, LowOutCoil_V, LowOutCoil_FluxLink = femm.mo_getcircuitproperties(position.low_outcoil()[5])
            LowOutCoil_Voltages[i] = LowOutCoil_V
            LowOutCoil_Currents[i] = LowOutCoil_I
            LowOutCoil_Flux[i] = LowOutCoil_FluxLink

            InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
            InnCoil_Voltages[i] = InnCoil_V
            InnCoil_Currents[i] = InnCoil_I
            InnCoil_Flux[i] = InnCoil_FluxLink

            femm.mi_selectgroup(1)
            femm.mi_selectgroup(2)
            femm.mi_movetranslate(0, pre_simulation.parameters()[1])  # Translate inner coil to different distance
            femm.mi_clearselected()

        OutCoil_Signals = (abs(UppOutCoil_Voltages) - abs(LowOutCoil_Voltages))
        Norm_OutCoil_Signals = OutCoil_Signals / abs(InnCoil_Currents)


        # if self.save:
        #     np.savez_compressed(self.filename, Input_Parameters = input_par, IC_positions = InnCoil_Positions, IC_voltages = coi.inncoil()['Inncoil_voltage'], UOC_voltages = coi.uppout()['UppOut_voltage'], LOC_voltages = coi.lowout()['LowOut_voltage'],
        #        IC_currents = coi.inncoil()['Inncoil_current'], UOC_currents=coi.uppout()['UppOut_current'], LOC_currents = coi.lowout()['LowOut_current'], IC_flux = InnCoil_Flux )

        if self.save:  # Only save the data when the save argument is specified
            np.savez('../dataMap/FEMM_data/' + self.filename, IC_positions=InnCoil_Positions, IC_voltages=InnCoil_Voltages,
                     UOC_voltages=UppOutCoil_Voltages, LOC_voltages=LowOutCoil_Voltages,
                     UOC_flux=UppOutCoil_Flux, LOC_flux=LowOutCoil_Flux)
            print('data saved')