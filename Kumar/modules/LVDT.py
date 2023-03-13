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
        sensor = design.Sensortype(InnCoilCurrent = 0.02, Simfreq = 10000, OutCoilCurrent = 0) #can be changed
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype(outcoil_material="32 AWG", inncoil_material="32 AWG") #can be changed
        if self.default=='yes':
            geo = design.Geometry(value[self.design_type]["inn_ht"], value[self.design_type]['inn_rad'], value[self.design_type]['inn_layers'], value[self.design_type]['inn_dist'], value[self.design_type]['out_ht'], value[self.design_type]['out_rad'],
                                  value[self.design_type]['out_layers'], value[self.design_type]['out_dist'], value[self.design_type]['mag_len'], value[self.design_type]['mag_dia'], value[self.design_type]['ver_shi'])
            input_par = 'design type : '+self.design_type
        else:
            input_par = {'IC_height':18, 'IC_radius':21, 'IC_layers':6, 'IC_distance':0, 'OC_height':13.5, 'OC_radius':31.5, 'OC_layers':self.parameter1, 'OC_distance':31.5, 'mag_len':0, 'mag_dia':0, 'ver_shi':0}
            geo = design.Geometry(input_par['IC_height'], input_par['IC_radius'], input_par['IC_layers'], input_par['IC_distance'], input_par['OC_height'], input_par['OC_radius'],
                                  input_par['OC_layers'], input_par['OC_distance'], input_par['mag_len'], input_par['mag_dia'], input_par['ver_shi'])
        position = coil.Position(inn_ht=geo.inncoil()[0], inn_rad=geo.inncoil()[1], inn_layers=geo.inncoil()[2], inn_dist=geo.inncoil()[3], out_ht=geo.outcoil()[0], out_rad=geo.outcoil()[1], out_layers=geo.outcoil()[2], out_dist=geo.outcoil()[3],
                                 ver_shi=geo.mag()[2], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], mag_len=geo.mag()[0], mag_dia=geo.mag()[1])
        length = coil.Length(inn_layers=geo.inncoil()[2], inn_rad=geo.inncoil()[1], inn_wiredia=wire.prop_inn()[0], inn_wireins=wire.prop_inn()[1], innwind_pr_layer=position.inncoil()[3], out_layers=geo.outcoil()[2], out_rad=geo.outcoil()[1],
                             out_wiredia=wire.prop_out()[0], out_wireins=wire.prop_out()[1], outwind_pr_layer=position.upp_outcoil()[3])
        print(position.inncoil(), position.upp_outcoil())
        print('inn, out, total coil lengths : ', length.inncoil(), length.upp_outcoil(), length.inncoil()+(2*length.upp_outcoil()))
        inn_dc = (length.inncoil()*162)/304800
        print('inner coil Dc resistance as per datasheet (in ohms) :', inn_dc)

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

        res = coil.Coil_prop(pre_simulation.parameters()[0])
        inn_prop = res.inncoil()
        uppout_prop = res.uppout()
        lowout_prop = res.lowout()

        move_group = femm_model.Femm_move(groups = [1,2], x_dist=0, y_dist=pre_simulation.parameters()[2])

        for i in range(0, pre_simulation.parameters()[0] + 1):
            print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
            inn_prop['Inncoil_position'][i] = pre_simulation.parameters()[2] + (pre_simulation.parameters()[1] * i)

            femm.mi_zoom(-2, -50, 50, 50)
            femm.mi_refreshview()
            femm.mi_saveas('LVDT position_ETpf_LIP.fem')   # We have to give the geometry a name before we can analyze it.
            femm.mi_analyze()   # Now,analyze the problem and load the solution when the analysis is finished
            femm.mi_loadsolution()

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

            move_group = femm_model.Femm_move(groups=[1, 2], x_dist=0, y_dist=pre_simulation.parameters()[1])

        if self.save:
            np.savez_compressed(self.filename, Input_Parameters = input_par, IC_positions = inn_prop['Inncoil_position'], IC_voltages = inn_prop['Inncoil_voltage'],
                                UOC_voltages = uppout_prop['UppOut_voltage'], LOC_voltages = lowout_prop['LowOut_voltage'], IC_currents = inn_prop['Inncoil_current'],
                                UOC_currents=uppout_prop['UppOut_current'], LOC_currents = lowout_prop['LowOut_current'], IC_flux = inn_prop['Inncoil_flux'],
                                UOC_flux = uppout_prop['UppOut_flux'], LOC_flux = lowout_prop['LowOut_flux'] )
