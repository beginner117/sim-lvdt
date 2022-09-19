import design
import femm
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import math
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
        StepSize = 0.25
        InnCoil_Offset = -2.5

        sensor = design.Sensortype(0.02, 10000, 0)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=24, inn_rad=11, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=35, out_layers=5, out_dist=self.parameter1, mag_len=40, mag_dia=10, ver_shi=0)
        req_plots = dataplot_condition.Req_plots(out_vol=0, inn_vol=0, phase=0, norm_signal=0, fit_error=0, Norm_fiterror=1, impedance=0)
        zero_fit = 1
        print_data = dataplot_condition.Print_data(phase=1, slope=1)
        data_file = self.filename
        data_save = 0

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
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                              circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material,
                                              edit_mode=4, group=1, label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                              turns_pr_layer=position.inncoil()[4])
            inncoil_str
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                            circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                            edit_mode=4, group=3, label1=wire.prop32()[1], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.upp_outcoil()[4])
            uppoutstr
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                            circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                            edit_mode=4, group=4, label1=wire.prop32()[0], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.low_outcoil()[4])

            lowoutstr
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            magnetstr
            bc = femm_model.Femm_bc()
            bc

            InnCoil_Positions = np.zeros(NSteps + 1)
            MetaData = np.zeros(NSteps + 1)
            UppOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            UppOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            UppOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Flux = np.zeros(NSteps + 1).astype(complex)

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
        Inn_Inductance = abs(modelled.InnCoil_Flux / modelled.InnCoil_Currents)
        Inn_resistance = abs(modelled.InnCoil_Voltages / modelled.InnCoil_Currents)
        print("average Inn coil Inductance is :", sum(Inn_Inductance)/len(Inn_Inductance))
        print("average Inn coil resistance is :", sum(Inn_resistance)/len(Inn_resistance))

        if NSteps > 2:
            modelled.MetaData[0] = NSteps
            modelled.MetaData[1] = StepSize
            modelled.MetaData[2] = sensor.para()[2]
            np.savetxt(outputfile, (modelled.InnCoil_Positions, modelled.UppOutCoil_Voltages, modelled.LowOutCoil_Voltages, modelled.InnCoil_Voltages, modelled.MetaData))
        class Results():
            def __init__(self):
                pass
            plt.plot(modelled.InnCoil_Positions, modelled.InnCoil_Voltages.real, 'o-')
            plt.ylabel('Inner Coil Voltage [V]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.show()

            if req_plots.out_vol == 1:
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
                pass
            Norm_OutCoil_Signals = (abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages)) / sensor.para()[0]
            def linfunc(x, a, b):
                return a * x + b   #ydata: Norm_OutCoil_Signals, xdata: InnCoil_Position
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
                InnCoil_Positions1 = modelled.InnCoil_Positions[7:14]
                Norm_OutCoil_Signals1 = Norm_OutCoil_Signals[7:14]
                optimizedparameters1, pcov = opt.curve_fit(linfunc, InnCoil_Positions1, Norm_OutCoil_Signals1)
                print("Fitted slope of the function (-1,1):", optimizedparameters1[0])
                fitted_Norm_OutCoil_Signals1 = linfunc(InnCoil_Positions1, *optimizedparameters1)
                print("fit (-1,1) is", format(optimizedparameters1))
                fiterror1 = Norm_OutCoil_Signals - (optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) + optimizedparameters1[1])
                norm_fit_error1 = (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals))) * 100

            print("Normalised out coil signals :", Norm_OutCoil_Signals)
            fiterror = np.array(Norm_OutCoil_Signals) - np.array(fitted_Norm_OutCoil_Signals)
            norm_fit_error = (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100
        results = Results()
        class Linearity():
            slopes = []
            theta = []
            def __init__(self):
                pass
            if req_plots.Norm_fiterror == 1:
                plt.plot(modelled.InnCoil_Positions[:10],
                         (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[:10] * 100, 'o-',
                         color='blue')
                plt.plot(modelled.InnCoil_Positions[11:],
                         (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[11:] * 100, 'o-',
                         color='blue')
                plt.plot([modelled.InnCoil_Positions[9], modelled.InnCoil_Positions[11]],
                         [results.norm_fit_error1[9], results.norm_fit_error1[11]],
                         "--", color='black')
                plt.ylabel('Linearity [%]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.ylim(0, 0.46)
                # plt.legend()
                plt.show()
            for i in range(0, len(results.Norm_OutCoil_Signals)):
                if i == len(results.Norm_OutCoil_Signals)-1:
                    break
                m = np.polyfit([modelled.InnCoil_Positions[i], modelled.InnCoil_Positions[i+1]], [results.Norm_OutCoil_Signals[i], results.Norm_OutCoil_Signals[i+1]], 1)[0]
                slopes.append(m)
                theta.append(math.atan(m))
            m1 = results.optimizedparameters1[0]
            y = (np.array(theta)-m1)/np.array(theta)
            y1 = (np.array(slopes)-np.tan(m1))/np.array(slopes)
            plt.plot(modelled.InnCoil_Positions[1:], theta, "o--")
            plt.ylabel("angle [θ]")
            plt.xlabel("position")
            plt.show()
            plt.plot(modelled.InnCoil_Positions[1:], slopes, "o--")
            plt.ylabel("slope [tan(θ)]")
            plt.xlabel("position")
            plt.show()
            plt.plot(modelled.InnCoil_Positions[1:], abs(np.array(y)*1), "o--")
            plt.ylabel("Relative angular error [$\dfrac{fit error}{θ}$]")
            plt.xlabel("position")
            plt.tight_layout()
            plt.show()
            plt.plot(modelled.InnCoil_Positions[1:], abs(np.array(y1) * 1), "o--")
            plt.ylabel("Relative slope error [$\dfrac{fit error}{tan(θ)}$]")
            plt.xlabel("position")
            plt.tight_layout()
            plt.show()
            plt.plot(modelled.InnCoil_Positions[1:], abs(np.array(theta)-m1), "o--")
            plt.ylabel("angular fit error [abs(θ-fit)]")
            plt.xlabel("position")
            plt.show()
        linearity = Linearity()
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

