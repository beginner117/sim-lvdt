import design
import femm
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import pickle
import dataplot_condition
import femm_model
import coil

class Analysis():
    def __init__(self, parameter1, filename: str):
        self.parameter1 = parameter1
        self.filename = filename
    def simulate(self):
        # The package must be initialized with the openfemm command.
        femm.openfemm()
        # We need to create a new Magnetostatics document to work on.
        femm.newdocument(0)

        outputfile = 'LVDT_10kHz_20mA_31AWG_10mm_6_7_7.out'
        NSteps = 20
        StepSize = 0.5
        InnCoil_Offset = -5

        sensor = design.Sensortype(0.02, 10000, 0)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=24, inn_rad=11, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=35, out_layers=5, out_dist=self.parameter1, mag_len=40, mag_dia=10, ver_shi=0)
        req_plots = dataplot_condition.Req_plots(out_vol=0, inn_vol=0, phase=0, norm_signal=1, fit_error=1, Norm_fiterror=1, impedance=0)
        zero_fit = 1
        print_data = dataplot_condition.Print_data(phase=1, slope=1)

        data_file = self.filename
        save = 0
        data_save = 0
        if data_save == 1:
            directory = data_file
            parent_dir = "C:\\Users\\kumar\\OneDrive\\Desktop\\pi\\lvdt\\small_IP\\lvdtdata"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)

        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3],
                                 geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3], geo.mag()[2],
                                 wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1], geo.mag()[0], geo.mag()[1])

        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1],
                             position.inncoil()[3], geo.outcoil()[2], geo.outcoil()[1], wire.prop32()[0],
                             wire.prop32()[1], position.upp_outcoil()[3])
        length

        class Modelling():
            def __init__(self):
                pass
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0],
                                              y2=position.inncoil()[1],
                                              circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material, edit_mode=4, group=1,
                                              label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                              turns_pr_layer=position.inncoil()[4])
            inncoil_str
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                            circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2],
                                            circ_type=1, material=wire.inncoil_material, edit_mode=4, group=3,
                                            label1=wire.prop32()[1], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.upp_outcoil()[4])
            uppoutstr
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                            circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2],
                                            circ_type=1, material=wire.inncoil_material, edit_mode=4, group=4,
                                            label1=wire.prop32()[0], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.low_outcoil()[4])

            lowoutstr
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            magnetstr
            bc = femm_model.Femm_bc()
            bc

            UppOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Positions = np.zeros(NSteps + 1)

            UppOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Currents = np.zeros(NSteps + 1).astype(complex)

            UppOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Flux = np.zeros(NSteps + 1).astype(complex)
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

                # Now, the finished input geometry can be displayed.
                # femm.mi_zoomnatural()
                femm.mi_zoom(-2, -50, 50, 50)
                femm.mi_refreshview()

                # We have to give the geometry a name before we can analyze it.
                femm.mi_saveas('LVDT position_ETpf_LIP.fem')

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

                # Translate inner coil to different distance
                femm.mi_selectgroup(1)
                femm.mi_selectgroup(2)
                femm.mi_movetranslate(0, StepSize)
                femm.mi_clearselected()
        loop = Computation_loop()

        print(modelled.InnCoil_Positions)
        print("Upp Out voltages :", modelled.UppOutCoil_Voltages)
        print("Low Out voltages :", modelled.LowOutCoil_Voltages)
        print("Inn voltages :", modelled.InnCoil_Voltages)
        Inn_Inductance = abs(modelled.InnCoil_Flux / modelled.InnCoil_Currents)
        Inn_resistance = abs(modelled.InnCoil_Voltages / modelled.InnCoil_Currents)
        print("average Inn coil Inductance is :", sum(Inn_Inductance)/len(Inn_Inductance))
        print("average Inn coil resistance is :", sum(Inn_resistance)/len(Inn_resistance))

        if NSteps > 2:
            modelled.MetaData[0] = NSteps
            modelled.MetaData[1] = StepSize
            modelled.MetaData[2] = sensor.para()[2]
            np.savetxt(outputfile,
                       (modelled.InnCoil_Positions, modelled.UppOutCoil_Voltages, modelled.LowOutCoil_Voltages, modelled.InnCoil_Voltages, modelled.MetaData))

        #plt.style.use(['science', 'grid', 'notebook'])
        class Results():
            def __init__(self):
                pass
            if req_plots.impedance == 1:
                inn_resistance = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions,
                                                                    abs(modelled.InnCoil_Voltages) / abs(
                                                                        modelled.InnCoil_Currents),
                                                                    'Inner Coil Position [mm]',
                                                                    'Inner Coil resistance [ohms]', 0)
                inn_resistance
                inn_inductance = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, (
                            abs(modelled.InnCoil_Flux) / abs(modelled.InnCoil_Currents)) * 1000,
                                                                    'Inner Coil Position [mm]', 'Inn coil inductance [mH]',
                                                                    0)
                inn_inductance

            plt.plot(modelled.InnCoil_Positions, modelled.InnCoil_Voltages.real, 'o-')
            plt.ylabel('Inner Coil Voltage [V]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.show()

            if req_plots.out_vol == 1:
                plt.plot(modelled.InnCoil_Positions, abs(modelled.InnCoil_Voltages), 'o-')
                plt.ylabel('Magnitude Inner Coil Voltages [V]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.show()

                plt.plot(modelled.InnCoil_Positions, abs(modelled.LowOutCoil_Voltages), 'o-', label="Lower outer coil")
                plt.plot(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages), 'o-', label="Upper outer coil")
                plt.ylabel('Magnitude Outer Coil Voltages [V]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.legend(frameon=False)
                plt.show()

                plt.plot(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages), 'o-',
                         label="Upper - Lower outer coil", )
                plt.ylabel('Diff. of Magnitude Outer Coil Voltages [V]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.legend(frameon=False)
                plt.show()

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
                plt.show()

            Norm_OutCoil_Signals = (abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages)) / sensor.para()[0]
            def linfunc(x, a, b):
                return a * x + b
                # ydata: Norm_OutCoil_Signals, xdata: InnCoil_Position
            optimizedParameters, pcov = opt.curve_fit(linfunc, modelled.InnCoil_Positions, Norm_OutCoil_Signals);
            print("Fitted slope of the function:", optimizedParameters[0])
            fitted_Norm_OutCoil_Signals = linfunc(modelled.InnCoil_Positions, *optimizedParameters)
            print(optimizedParameters)
            plt.plot(modelled.InnCoil_Positions, fitted_Norm_OutCoil_Signals, 'o-', color = "blue",  label="linear fit")
            plt.ylabel('Response [V/A]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            plt.show()
            if zero_fit == 1:
                InnCoil_Positions1 = modelled.InnCoil_Positions[8:13]
                Norm_OutCoil_Signals1 = Norm_OutCoil_Signals[8:13]
                optimizedparameters1, pcov = opt.curve_fit(linfunc, InnCoil_Positions1, Norm_OutCoil_Signals1)
                print("Fitted slope of the function (-0.5,0.5):", optimizedparameters1[0])
                fitted_Norm_OutCoil_Signals1 = linfunc(InnCoil_Positions1, *optimizedparameters1)
                print("fit (-0.5,0.5) is", format(optimizedparameters1))

                if req_plots.norm_signal == 1:
                    norm_sig = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions, Norm_OutCoil_Signals, 'Inner Coil Position [mm]', 'Diff. Magnitude Outer Coil Voltages [V/A]', 0)
                    norm_sig
                if req_plots.fit_error == 1:
                    fit = dataplot_condition.Plot_parameters(modelled.InnCoil_Positions,Norm_OutCoil_Signals - optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) +optimizedparameters1[1], 'Inner Coil Position [mm]', 'Fit error [V/A]', 0)
                    fit
                fiterror1 = Norm_OutCoil_Signals - (optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) + optimizedparameters1[1])
                norm_fit_error1 = (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals))) * 100
                fiterror = np.array(Norm_OutCoil_Signals) - np.array(fitted_Norm_OutCoil_Signals)
                norm_fit_error = (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100
                if req_plots.Norm_fiterror == 1:
                    c1 = NSteps/2
                    c2 = (NSteps/2)+1
                    c3 = (NSteps/2)-1
                    # plt.plot(modelled.InnCoil_Positions,  (abs(fiterror1)/ abs(np.array(Norm_OutCoil_Signals))) * 100, label="fit (-0.5,0.5)")
                    plt.plot(modelled.InnCoil_Positions[:10],
                             (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals)))[:10] * 100, 'o-',
                             color='blue')
                    plt.plot(modelled.InnCoil_Positions[11:],
                             (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals)))[11:] * 100, 'o-',
                             color='blue')
                    plt.plot([modelled.InnCoil_Positions[9], modelled.InnCoil_Positions[11]],
                             [norm_fit_error1[9], norm_fit_error1[11]],
                             "--", color='black')
                    plt.ylabel('Linearity [%]')
                    plt.xlabel('Inner Coil Position [mm]')
                    plt.ylim(0, 0.76)
                    # plt.legend()
                    plt.show()

            #print(fitted_Norm_OutCoil_Signals)
            print("Normalised out coil signals :", Norm_OutCoil_Signals)
            fiterror = np.array(Norm_OutCoil_Signals) - np.array(fitted_Norm_OutCoil_Signals)
            norm_fit_error = (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100
        results = Results()

        class Save_data():
            def __init__(self):
                pass
            norm_fit_error = (abs(np.array(results.Norm_OutCoil_Signals) - np.array(
                results.fitted_Norm_OutCoil_Signals)) / abs(np.array(results.Norm_OutCoil_Signals))) * 100
            fit1 = results.optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) + \
                   results.optimizedparameters1[1]
            data = np.column_stack((modelled.InnCoil_Positions, modelled.UppOutCoil_Voltages,
                                    modelled.LowOutCoil_Voltages, modelled.InnCoil_Voltages,
                                    results.Norm_OutCoil_Signals, results.fiterror1, results.norm_fit_error1,
                                    Inn_Inductance, Inn_resistance))
            np.savetxt(data_file, data)
            if data_save == 1:
                with open(data_save.path, "w") as f:
                    f.write(data)
            pname = "pick" + self.filename
            pickle_out = open(pname, "wb")
            pickle.dump(data, pickle_out)
            pickle_out.close()
        #saved_data = Save_data()

