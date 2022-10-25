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

        femm.openfemm()   # The package must be initialized with the openfemm command.
        femm.newdocument(0)   # We need to create a new Magnetostatics document to work on.

        pre_simulation = design.Simulation(Nsteps=40, stepsize=1, inncoil_offset=-20, data_file =self.filename, fit_points=self.parameter1)
        sensor = design.Sensortype(InnCoilCurrent = 0.02, Simfreq = 10000, OutCoilCurrent = 0)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=24, inn_rad=11, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=35, out_layers=5, out_dist=54.5, mag_len=40, mag_dia=10, ver_shi=0)
        req_plots = dataplot_condition.Req_plots(out_vol=0, inn_vol=0, norm_signal=0, fit_error=0, Norm_fiterror=1, impedance=0)
        print_data = dataplot_condition.Print_data(phase=1, slope=1)

        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3],
                                 geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3], geo.mag()[2],
                                 wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1], geo.mag()[0], geo.mag()[1])
        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1],
                             position.inncoil()[3], geo.outcoil()[2], geo.outcoil()[1], wire.prop32()[0],
                             wire.prop32()[1], position.upp_outcoil()[3])
        class Modelling():
            def __init__(self):
                pass
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                              circ_name=position.inncoil()[5], circ_current=sensor.para()[0], circ_type=1, material=wire.inncoil_material,
                                              edit_mode=4, group=1, label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                              turns_pr_layer=position.inncoil()[4])
            uppoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.upp_outcoil()[2], x2=position.upp_outcoil()[0], y2=position.upp_outcoil()[1],
                                            circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                            edit_mode=4, group=3, label1=wire.prop32()[1], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.upp_outcoil()[4])
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1], x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                            circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                            edit_mode=4, group=4, label1=wire.prop32()[0], label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.low_outcoil()[4])
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            bc = femm_model.Femm_bc()

            InnCoil_Positions = np.zeros(pre_simulation.parameters()[0] + 1)
            MetaData = np.zeros(pre_simulation.parameters()[0] + 1)
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
        class Computation_loop():
            def __init__(self):
                pass
            for i in range(0, pre_simulation.parameters()[0] + 1):
                print(pre_simulation.parameters()[2] + pre_simulation.parameters()[1] * i)
                modelled.InnCoil_Positions[i] = pre_simulation.parameters()[2] + (pre_simulation.parameters()[1] * i)

                femm.mi_zoom(-2, -50, 50, 50)
                femm.mi_refreshview()     # We have to give the geometry a name before we can analyze it.
                femm.mi_saveas('LVDT position_ETpf_LIP.fem')   # Now,analyze the problem and load the solution when the analysis is finished
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
                femm.mi_movetranslate(0, pre_simulation.parameters()[1])  # Translate inner coil to different distance
                femm.mi_clearselected()
        loop = Computation_loop()
        Inn_Inductance = abs(modelled.InnCoil_Flux / modelled.InnCoil_Currents)
        Inn_resistance = abs(modelled.InnCoil_Voltages / modelled.InnCoil_Currents)
        print("avrg Inncoil Induc and Resist :", sum(Inn_Inductance)/len(Inn_Inductance), sum(Inn_resistance)/len(Inn_resistance))

        class Results():
            def __init__(self):
                pass
            print(np.array(modelled.InnCoil_Voltages))
            if req_plots.out_vol == 1:
                plt.plot(modelled.InnCoil_Positions, abs(modelled.LowOutCoil_Voltages), 'o-', label="Lower outer coil")
                plt.plot(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages), 'o-', label="Upper outer coil")
                voltage_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]',  y_lab='Magnitude Outer Coil Voltages [V]')
                plt.plot(modelled.InnCoil_Positions, abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages), 'o-', label="Upp - Low outer coil", )
                MVol_Mag_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]',  y_lab='Diff. of Magnitude Outer Coil Voltages [V]')
            if print_data.phase == 1:
                InnCoil_Phases = np.angle(modelled.InnCoil_Voltages)
                LowOutCoil_Phases = np.angle(modelled.LowOutCoil_Voltages)
                UppOutCoil_Phases = np.angle(modelled.UppOutCoil_Voltages)
                print("Phase offset:", InnCoil_Phases[0] - LowOutCoil_Phases[0], InnCoil_Phases[pre_simulation.parameters()[0]] - UppOutCoil_Phases[pre_simulation.parameters()[0]])
            Norm_OutCoil_Signals = (abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages)) / (sensor.para()[0])
            OutCoil_Signals1 = (abs(modelled.UppOutCoil_Voltages) - abs(modelled.LowOutCoil_Voltages))
            print("signal1 : ", OutCoil_Signals1)
            print("Normalised out coil signals :", Norm_OutCoil_Signals)
            def linfunc(x, a, b):
                return a * x + b   #ydata: Norm_OutCoil_Signals, xdata: InnCoil_Position
            optimizedParameters, pcov = opt.curve_fit(linfunc, modelled.InnCoil_Positions, Norm_OutCoil_Signals);
            print("Fitted slope of the function & const:", optimizedParameters[0], optimizedParameters[1])
            fitted_Norm_OutCoil_Signals = linfunc(modelled.InnCoil_Positions, *optimizedParameters)
            plt.plot(modelled.InnCoil_Positions, Norm_OutCoil_Signals, 'o-', label="actual response")
            plt.plot(modelled.InnCoil_Positions, fitted_Norm_OutCoil_Signals, 'o-',  label="linear fit response")
            res_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]', y_lab='Fitted Response [V/A]')
            fiterror = np.array(Norm_OutCoil_Signals) - np.array(fitted_Norm_OutCoil_Signals)
            norm_fit_error = (abs(fiterror) / abs(np.array(Norm_OutCoil_Signals))) * 100

            mid = int(pre_simulation.parameters()[0]/2)
            if pre_simulation.parameters()[4] > 0 :
                a = mid - int((pre_simulation.parameters()[4] - 1) / 2)
                b = mid + int((pre_simulation.parameters()[4] - 1) / 2) + 1
                InnCoil_Positions1 = modelled.InnCoil_Positions[a:b]
                Norm_OutCoil_Signals1 = Norm_OutCoil_Signals[a:b]
                optimizedparameters1, pcov = opt.curve_fit(linfunc, InnCoil_Positions1, Norm_OutCoil_Signals1)
                print("Fitted slope (-1,1) and const:", optimizedparameters1[0], optimizedparameters1[1])
                fitted_Norm_OutCoil_Signals1 = linfunc(InnCoil_Positions1, *optimizedparameters1)
                fiterror1 = Norm_OutCoil_Signals - (optimizedparameters1[0] * (np.array(modelled.InnCoil_Positions)) + optimizedparameters1[1])
                norm_fit_error1 = (abs(fiterror1) / abs(np.array(Norm_OutCoil_Signals))) * 100
        results = Results()
        class Linearity():
            slopes = []
            theta = []
            def __init__(self):
                pass
            if req_plots.Norm_fiterror == 1:
                plt.plot(modelled.InnCoil_Positions[:results.mid],
                         (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[:results.mid] * 100, 'o-', color='blue')
                plt.plot(modelled.InnCoil_Positions[results.mid+1:],
                         (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[results.mid+1:] * 100, 'o-', color='blue')
                plt.plot([modelled.InnCoil_Positions[results.mid-1], modelled.InnCoil_Positions[results.mid-1]],
                         [results.norm_fit_error1[results.mid+1], results.norm_fit_error1[results.mid+1]], "--", color='black')
                res_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]', y_lab='Linearity [%]')

                #plt.plot(modelled.InnCoil_Positions, np.array(np.rad2deg(np.arctan(results.norm_fit_error1))), "o--")
                #aape_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]', y_lab='AAPE [θ]')
                lin1 = (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[:results.mid] * 100
                lin2 = (abs(results.fiterror1) / abs(np.array(results.Norm_OutCoil_Signals)))[results.mid+1:] * 100
                lin3 = np.concatenate([lin1, lin2])
            for i in range(0, len(results.Norm_OutCoil_Signals)):
                if not i == results.mid:
                    m = np.polyfit([modelled.InnCoil_Positions[i], modelled.InnCoil_Positions[results.mid]], [results.Norm_OutCoil_Signals[i], results.Norm_OutCoil_Signals[results.mid]], 1)[0]
                    slopes.append(m)
                    theta.append(math.degrees(math.atan(m)))
            m1 = results.optimizedparameters1[0]
            y = (np.array(theta)-math.degrees(math.atan(m1)))/np.array(theta)
            y1 = (np.array(slopes)-m1)/np.array(slopes)
            plt.plot(modelled.InnCoil_Positions[results.mid+1:], slopes[results.mid:], "o--", color = 'b')
            plt.plot(modelled.InnCoil_Positions[:results.mid], slopes[:results.mid], "o--", color = 'b')
            slope_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]', y_lab="slope [tan(θ)]")
            plt.plot(modelled.InnCoil_Positions[:results.mid], abs(np.array(y1) * 1)[:results.mid], "o--", color = 'b')
            plt.plot(modelled.InnCoil_Positions[results.mid+1:], abs(np.array(y1) * 1)[results.mid:], "o--", color = 'b')
            rel_slope_plot = dataplot_condition.Plot_base(x_lab='Inner Coil Position [mm]', y_lab="Relative slope error [$\dfrac{abs(fit - actual)}{tan(θ)}$]")
        linearity = Linearity()
        #text_datafile = dataplot_condition.Save_data(pre_simulation.parameters()[3], modelled.InnCoil_Positions,
                                                    # modelled.UppOutCoil_Voltages, modelled.LowOutCoil_Voltages,
                                                    # modelled.InnCoil_Voltages, results.Norm_OutCoil_Signals,
                                                    # results.fiterror1, results.norm_fit_error1, Inn_Inductance,
                                                    # Inn_resistance, rough1=linearity.lin3, rough2=linearity.theta)

