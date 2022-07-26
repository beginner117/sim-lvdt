import design
import femm
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil
import pickle
import dataplot_condition
import coil
import femm_model

class Analysis():
    def __init__(self, parameter1, filename: str):
        self.parameter1 = parameter1
        #self.parameter2 = parameter2
        self.filename = filename

    def simulate(self):
        femm.openfemm()
        femm.newdocument(0)

        outputfile = 'F1,F2_benchtower_10kHz_20mA_32AWG_10mm_6_5_5.out'
        NSteps = 20
        StepSize = 0.25
        InnCoil_Offset = -2.5

        sensor = design.Sensortype(0.02, 10000, 0)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=self.parameter1, inn_rad=21, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=31.5, out_layers=5,
                              out_dist=14.5, mag_len=40, mag_dia=10, ver_shi=0)
        req_plots = dataplot_condition.Req_plots(out_vol=0, inn_vol=0, phase=0, norm_signal=1, fit_error=1, Norm_fiterror=1, impedance=1)
        print_data = dataplot_condition.Print_data(phase=0, slope=1)

        inn_area = np.pi * (wire.prop32()[0]) * (wire.prop32()[0]) / 4
        uppout_area = np.pi * (wire.prop32()[0]) * (wire.prop32()[0]) / 4
        lowout_area = np.pi * (wire.prop32()[0]) * (wire.prop32()[0]) / 4

        data_file = self.filename
        parent_directory = "C:\\Users\\kumar\\OneDrive\\Desktop\\pi\\f0miror_lv\\textdata"
        save = 0
        save_data = 0
        if save_data == 1:
            data_save = dataplot_condition.Data_save(parent_directory, data_file)
            save_plot = data_save.path

        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3], geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3], geo.mag()[2], wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1], geo.mag()[0], geo.mag()[1])
        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1], position.inncoil()[3], geo.outcoil()[2], geo.outcoil()[1], wire.prop32()[0], wire.prop32()[1], position.upp_outcoil()[3])

        class Impedance():
            def __init__(self):
                #self.length.inncoil()
                #self.length.upp_outcoil()
                #self.length.low_outcoil()
                pass
            def resistance(self):
                inncoil_res = ((length.inncoil()*wire.prop32()[4])/inn_area)*1000
                uppout_res = ((length.upp_outcoil()*wire.prop32()[4])/uppout_area)*1000
                lowout_res = ((length.low_outcoil() * wire.prop32()[4]) / lowout_area)*1000
                return [inncoil_res, uppout_res, lowout_res]
            def inductance(self):
                inncoil_ind = ((wire.prop32()[5]*((position.inncoil()[4])**2)*inn_area)/geo.inncoil()[0])/1000
                uppout_ind = ((wire.prop32()[5] * ((position.inncoil()[4]) ** 2) * uppout_area) / geo.outcoil()[0])/1000
                lowout_ind = ((wire.prop32()[5] * ((position.inncoil()[4]) ** 2) * lowout_area) / geo.outcoil()[0])/1000
                return [inncoil_ind, uppout_ind, lowout_ind]
            def reactance(self):
                inncoil_rea = 2*(np.pi)*(sensor.para()[1])*self.inductance()[0]
                uppout_rea = 2 * (np.pi) * (sensor.para()[1]) * self.inductance()[1]
                lowout_rea = 2 * (np.pi) * (sensor.para()[1]) * self.inductance()[2]
                return [inncoil_rea, uppout_rea, lowout_rea]
        impedance = Impedance()
        print("resistance of inn coil is : ", impedance.resistance()[0])
        print("reactance of inn coil is : ", impedance.reactance()[0])
        print("inductance of inn coil is : ", impedance.inductance()[0])

        class Modelling():
            def __init__(self):
                pass
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0],
                                              y2=position.inncoil()[1],
                                              circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material, edit_mode=4, group=1,
                                              label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                              turns_pr_layer=position.inncoil()[4])
            inncoil_str
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2],
                                            x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                            circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1,
                                            material=wire.inncoil_material, edit_mode=4, group=3, label1=wire.prop32()[1],
                                            label2=geo.outcoil()[0], blockname=wire.prop32()[2], turns_pr_layer=position.upp_outcoil()[4])
            uppoutstr
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1],
                                            x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                            circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1,
                                            material=wire.inncoil_material, edit_mode=4, group=4, label1=wire.prop32()[0],
                                            label2=geo.outcoil()[0], blockname=wire.prop32()[2], turns_pr_layer=position.low_outcoil()[4])

            lowoutstr
            bc = femm_model.Femm_bc()
            bc

            UppOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Voltages = np.zeros(NSteps + 1).astype(complex)

            UppOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Currents = np.zeros(NSteps + 1).astype(complex)

            UppOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Flux = np.zeros(NSteps + 1).astype(complex)

            InnCoil_Positions = np.zeros(NSteps + 1)
            MetaData = np.zeros(NSteps + 1)

            femm.mi_selectgroup(1)
            femm.mi_selectgroup(2)
            femm.mi_movetranslate(0, InnCoil_Offset)
            femm.mi_clearselected()
        modelled = Modelling()

        class Computation_loop():
            def __init__(self):
                pass
            for i in range(0, NSteps + 1):
                print(InnCoil_Offset + StepSize * i)
                modelled.InnCoil_Positions[i] = InnCoil_Offset + (StepSize * i)

                femm.mi_zoom(-2, -50, 50, 50)
                femm.mi_refreshview()

                # We have to give the geometry a name before we can analyze it.
                femm.mi_saveas('bench_tower position_ETpf_LIP.fem')

                # Now,analyze the problem and load the solution when the analysis is finished
                femm.mi_analyze()
                femm.mi_loadsolution()

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

                femm.mi_selectgroup(1)
                femm.mi_selectgroup(2)
                femm.mi_movetranslate(0, StepSize)
                femm.mi_clearselected()
        loop = Computation_loop()

        print("Inn coil positions :", modelled.InnCoil_Positions)
        print("Upp out coil voltages :", modelled.UppOutCoil_Voltages)
        print("Low out coil voltages :", modelled.LowOutCoil_Voltages)
        print("Upp out current :", modelled.UppOutCoil_Currents)
        print("low out current :", modelled.LowOutCoil_Currents)
        print("Upp out flux :", modelled.UppOutCoil_Flux)
        print("low out flux :", modelled.LowOutCoil_Flux)
        print("Inn coil voltages :", modelled.InnCoil_Voltages)

        Inn_Inductance = abs(modelled.InnCoil_Flux/modelled.InnCoil_Currents)
        Inn_resistance = abs(modelled.InnCoil_Voltages/modelled.InnCoil_Currents)
        #Uppout_Inductance = abs(modelled.UppOutCoil_Flux/modelled.InnCoil_Currents)
        print("average Inn coil Inductance is :", sum(Inn_Inductance) / len(Inn_Inductance))
        print("average Inn coil resistance is :", sum(Inn_resistance) / len(Inn_resistance))

        if NSteps > 2:
            modelled.MetaData[0] = NSteps
            modelled.MetaData[1] = StepSize
            modelled.MetaData[2] = sensor.para()[2]
            np.savetxt(outputfile,
                       (modelled.InnCoil_Positions, modelled.UppOutCoil_Voltages, modelled.LowOutCoil_Voltages,
                        modelled.InnCoil_Voltages, modelled.MetaData))

        plt.style.use(['science', 'grid', 'notebook'])
        class Results():
            def __init__(self):
                pass
            if req_plots.impedance == 1:
                inn_resistance = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, abs(modelled.InnCoil_Voltages)/abs(modelled.InnCoil_Currents), 'Inner Coil Position [mm]', 'Inner Coil resistance [ohms]',0)
                inn_resistance
                inn_inductance = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, (abs(modelled.InnCoil_Flux)/abs(modelled.InnCoil_Currents))*1000, 'Inner Coil Position [mm]', 'Inn coil inductance [mH]',0)
                inn_inductance
            if req_plots.inn_vol == 1:
                inn_voltage = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, abs(modelled.InnCoil_Voltages), 'Inner Coil Position [mm]', 'Magnitude Inner Coil Voltages [V]', 0)
                inn_voltage

            if req_plots.out_vol == 1:
                plt.plot(modelled.InnCoil_Positions, abs(modelled.LowOutCoil_Voltages), 'o-', label="Lower outer coil")
                plt.plot(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages), 'o-', label="Upper outer coil")
                plt.ylabel('Magnitude Outer Coil Voltages [V]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.legend(frameon=False)
                if save == 1:
                    plt.savefig("abs_low,out_vol.png")
                    shutil.move("abs_low,out_vol.png", save_plot)
                plt.show()

                outvolt_diff = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages), 'Inner Coil Position [mm]', 'Diff. of Magnitude Outer Coil Voltages [V]', 0)
                outvolt_diff

            if print_data.phase == 1:
                InnCoil_Phases = np.angle(modelled.InnCoil_Voltages)
                LowOutCoil_Phases = np.angle(modelled.LowOutCoil_Voltages)
                UppOutCoil_Phases = np.angle(modelled.UppOutCoil_Voltages)
                print("Phase offset:", InnCoil_Phases[0] - LowOutCoil_Phases[0],
                      InnCoil_Phases[NSteps] - UppOutCoil_Phases[NSteps])

            if req_plots.phase == 1:
                plt.plot(modelled.InnCoil_Positions, InnCoil_Phases, 'o-', label="Inner coil")
                plt.plot(modelled.InnCoil_Positions, LowOutCoil_Phases, 'o-', label="Lower outer coil")
                plt.plot(modelled.InnCoil_Positions, UppOutCoil_Phases, 'o-', label="Upper outer coil")
                plt.ylabel('Phase [rad]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.legend()
                if save == 1:
                    plt.savefig("phase.png")
                    shutil.move("phase.png", save_plot)
                plt.show()

            Norm_OutCoil_Signals = (abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages)) / sensor.para()[0]
            def linfunc(x, a, b):
                return a * x + b
                # ydata: Norm_OutCoil_Signals, xdata: InnCoil_Position

            optimizedParameters, pcov = opt.curve_fit(linfunc, modelled.InnCoil_Positions, Norm_OutCoil_Signals);
            print("Fitted slope of the function:", optimizedParameters[0])
            fitted_Norm_OutCoil_Signals = linfunc(modelled.InnCoil_Positions, *optimizedParameters)
            print(optimizedParameters)

            InnCoil_Positions1 = modelled.InnCoil_Positions[8:13]
            Norm_OutCoil_Signals1 = Norm_OutCoil_Signals[8:13]
            optimizedparameters1, pcov = opt.curve_fit(linfunc, InnCoil_Positions1, Norm_OutCoil_Signals1)
            print("Fitted slope of the function around 0 (-0.5,0.5):", optimizedparameters1[0])
            fitted_Norm_OutCoil_Signals1 = linfunc(InnCoil_Positions1, *optimizedparameters1)
            print("fit (-0.5,0.5) is", format(optimizedparameters1))

            if req_plots.norm_signal == 1:
                norm_sig = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, Norm_OutCoil_Signals, 'Inner Coil Position [mm]', 'Diff. Magnitude Outer Coil Voltages [V/A]', 0)
                norm_sig
            if req_plots.fit_error == 1:
                fit = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions,Norm_OutCoil_Signals - optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) +optimizedparameters1[1], 'Inner Coil Position [mm]', 'Fit error [V/A]', 0)
                fit
            fiterror1 = Norm_OutCoil_Signals - optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) + optimizedparameters1[1]
            norm_fit_error1 = (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals))) * 100

            #print(fitted_Norm_OutCoil_Signals)
            print("Normalised out coil signals :", Norm_OutCoil_Signals)
            fiterror = np.array(Norm_OutCoil_Signals) - np.array(fitted_Norm_OutCoil_Signals)
            norm_fit_error = (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100

            if req_plots.Norm_fiterror == 1:
                #plt.plot(modelled.InnCoil_Positions, (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100)
                plt.plot(modelled.InnCoil_Positions,  (abs(fiterror1)/ abs(np.array(Norm_OutCoil_Signals))) * 100, label="fit (-0.5,0.5)")
                plt.ylabel('Normalised Fit error[%]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.ylim(0, 0.7)
                plt.legend()
                if save == 1:
                    plt.savefig("normfiterr_def.png")
                    shutil.move("normfiterr_def.png", save_plot)
                plt.show()
        results = Results()

        class Save_data():
            def __init__(self):
                pass
            norm_fit_error = (abs(np.array(results.Norm_OutCoil_Signals) - np.array(results.fitted_Norm_OutCoil_Signals)) / abs(np.array(results.Norm_OutCoil_Signals)))*100
            fit1 = results.optimizedparameters1[0]*(np.array(modelled.InnCoil_Positions))+results.optimizedparameters1[1]
            data = np.column_stack((modelled.InnCoil_Positions, modelled.UppOutCoil_Voltages, modelled.LowOutCoil_Voltages, modelled.InnCoil_Voltages,  results.Norm_OutCoil_Signals, results.fiterror1, results.norm_fit_error1, Inn_Inductance, Inn_resistance))
            np.savetxt(data_file, data)
            if save_data==1:
                with open(data_save.path, "w") as f:
                    f.write(data)
            pname = "pick"+self.filename
            pickle_out = open(pname, "wb")
            pickle.dump(data, pickle_out)
            pickle_out.close()
        saved_data = Save_data()


