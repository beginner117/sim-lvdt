import femm
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil
import design
import os
import pickle
import dataplot_condition
import coil
import femm_model

class Analysis():
    def __init__(self, parameter, filename: str):
        self.parameter = parameter
        # self.parameter2 = parameter2
        self.filename = filename

    def simulate(self):
        # The package must be initialized with the openfemm command.
        femm.openfemm()
        # We need to create a new Magnetostatics document to work on.
        femm.newdocument(0)

        outputfile = 'LVDT_10kHz_20mA_31AWG_10mm_6_7_7.out'
        NSteps = 10
        StepSize = 1
        InnCoil_Offset = -5

        sensor = design.Sensortype(0, 0, 1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=24, inn_rad=self.parameter, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=35,
                              out_layers=5, out_dist=54.5, mag_len=40, mag_dia=10, ver_shi=0)
        req_plots = dataplot_condition.Req_plots(out_vol=0, inn_vol=1, phase=0, norm_signal=1, fit_error=0,
                                                 Norm_fiterror=1, impedance=0)
        fit = 0

        data_file = self.filename
        save = 0
        data_save = 0
        if data_save == 1:
            directory = data_file
            parent_dir = "C:\\Users\\kumar\\OneDrive\\Desktop\\pi\\lvdt\\small_IP\\datavc"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            save_plot = path

        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3],
                                 geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3], geo.mag()[2],
                                 wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1], geo.mag()[0],
                                 geo.mag()[1])

        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1],
                             position.inncoil()[3], geo.outcoil()[2], geo.outcoil()[1], wire.prop32()[0],
                             wire.prop32()[1], position.upp_outcoil()[3])

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
                                            circ_name=position.upp_outcoil()[5], circ_current=sensor.para()[2],
                                            circ_type=1,
                                            material=wire.inncoil_material, edit_mode=4, group=3,
                                            label1=wire.prop32()[1],
                                            label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.upp_outcoil()[4])
            uppoutstr
            lowoutstr = femm_model.Femm_coil(x1=geo.outcoil()[1], y1=position.low_outcoil()[1],
                                            x2=position.low_outcoil()[0], y2=position.low_outcoil()[2],
                                            circ_name=position.low_outcoil()[5], circ_current=-sensor.para()[2],
                                            circ_type=1,
                                            material=wire.inncoil_material, edit_mode=4, group=4,
                                            label1=wire.prop32()[0],
                                            label2=geo.outcoil()[0], blockname=wire.prop32()[2],
                                            turns_pr_layer=position.low_outcoil()[4])

            lowoutstr
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.magnet()[0], x2=position.magnet()[2], y2=position.magnet()[1], material=wire.mag_mat(), edit_mode=4, group=2, label1=0.5, label2=geo.mag()[0])
            magnetstr
            bc = femm_model.Femm_bc()
            bc

            UppOutCoil_Forces = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Forces = np.zeros(NSteps + 1).astype(complex)
            Magnet_Forces = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Positions = np.zeros(NSteps + 1)

            UppOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Voltages = np.zeros(NSteps + 1).astype(complex)

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

        class Computational_loop():
            def __init__(self):
                pass
            for i in range(0, NSteps + 1):
                print(InnCoil_Offset + StepSize * i)
                modelled.InnCoil_Positions[i] = InnCoil_Offset + StepSize * i

                # Now, the finished input geometry can be displayed.
                # femm.mi_zoomnatural()
                femm.mi_zoom(-2, -50, 50, 50)
                femm.mi_refreshview()

                # We have to give the geometry a name before we can analyze it.
                femm.mi_saveas('RevLVDT_VC_ETpf_LIP.fem')

                # Now,analyze the problem and load the solution when the analysis is finished
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

                UppOutCoil_I, UppOutCoil_V, UppOutCoil_FluxLink = femm.mo_getcircuitproperties(
                    position.upp_outcoil()[5])
                modelled.UppOutCoil_Voltages[i] = UppOutCoil_V
                modelled.UppOutCoil_Currents[i] = UppOutCoil_I
                modelled.UppOutCoil_Flux[i] = UppOutCoil_FluxLink

                LowOutCoil_I, LowOutCoil_V, LowOutCoil_FluxLink = femm.mo_getcircuitproperties(
                    position.low_outcoil()[5])
                modelled.LowOutCoil_Voltages[i] = LowOutCoil_V
                modelled.LowOutCoil_Currents[i] = LowOutCoil_I
                modelled.LowOutCoil_Flux[i] = LowOutCoil_FluxLink

                InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
                modelled.InnCoil_Voltages[i] = InnCoil_V
                modelled.InnCoil_Currents[i] = InnCoil_I
                modelled.InnCoil_Flux[i] = InnCoil_FluxLink

                print("Upper Outer Coil force = ", UppOut_Force19, "Lower Outer Coil force = ", LowOut_Force19,
                      "Magnet force = ", Magn_Force19)
                modelled.UppOutCoil_Forces[i] = UppOut_Force19
                modelled.LowOutCoil_Forces[i] = LowOut_Force19
                modelled.Magnet_Forces[i] = Magn_Force19

                femm.mi_selectgroup(1)
                femm.mi_selectgroup(2)
                femm.mi_movetranslate(0, StepSize)
                femm.mi_clearselected()

        loop = Computational_loop()
        print(modelled.InnCoil_Positions)
        print("Upp Out Forces :", modelled.UppOutCoil_Forces)
        print("Low Out Forces :", modelled.LowOutCoil_Forces)
        print("Magnet Forces :", modelled.Magnet_Forces)
        print("Upp Out voltages :", modelled.UppOutCoil_Voltages)
        print("Low Out voltages :", modelled.LowOutCoil_Voltages)
        print("Inn voltages :", modelled.InnCoil_Voltages)
        Upp_Inductance = abs(modelled.UppOutCoil_Flux / modelled.UppOutCoil_Currents)
        Upp_resistance = abs(modelled.UppOutCoil_Voltages / modelled.UppOutCoil_Currents)
        Low_Inductance = abs(modelled.LowOutCoil_Flux / modelled.LowOutCoil_Currents)
        Low_resistance = abs(modelled.LowOutCoil_Voltages / modelled.LowOutCoil_Currents)
        print("average Low out coil Inductance is :", sum(Low_Inductance) / len(Low_Inductance))
        print("average Low out coil resistance is :", sum(Low_resistance) / len(Low_resistance))
        print("average upp out coil Inductance is :", sum(Upp_Inductance) / len(Upp_Inductance))
        print("average upp out coil resistance is :", sum(Upp_resistance) / len(Upp_resistance))

        if NSteps > 2:
            modelled.MetaData[0] = NSteps
            modelled.MetaData[1] = StepSize
            modelled.MetaData[2] = sensor.para()[2]
            np.savetxt(outputfile, (
            modelled.InnCoil_Positions, modelled.UppOutCoil_Forces, modelled.LowOutCoil_Forces, modelled.Magnet_Forces,
            modelled.MetaData))

        class Results():
            def __init__(self):
                pass

            #plt.style.use(['science', 'grid', 'notebook'])
            if req_plots.out_vol == 1:
                plt.plot(modelled.InnCoil_Positions, modelled.LowOutCoil_Forces, 'o-', label = "lower")
                plt.plot(modelled.InnCoil_Positions, modelled.UppOutCoil_Forces, 'o-', label = "upper")
                plt.ylabel('Outer Coil Force [N]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.legend()
                plt.show()

            if req_plots.inn_vol == 1:
                plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces, 'o-')
                plt.ylabel('Magnet Force [N]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.show()

            plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100, 'o-', color = "blue")
            plt.ylabel('Stability [%]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.show()
            lin = modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100

            def polyfunc(x, a, b, c):
                return a * x ** 2 + b * x + c
            renormalised_Forces = modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100
            optimizedParameters, pcov = opt.curve_fit(polyfunc, modelled.InnCoil_Positions, renormalised_Forces)
            print("Fitted parameters of function:", optimizedParameters)
            fitted_renormalised_Forces = polyfunc(modelled.InnCoil_Positions, *optimizedParameters)
            print(renormalised_Forces)
            plt.plot(modelled.InnCoil_Positions, fitted_renormalised_Forces, 'o-', color = "blue", label="poly2 fit")
            plt.ylabel('Stability [%]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            plt.show()

            def polyfunc(x, a, b, c):
                return a * x ** 2 + b * x + c
            Norm_Magnet_Forces = modelled.Magnet_Forces / sensor.para()[2]
            optimizedParameters, pcov = opt.curve_fit(polyfunc, modelled.InnCoil_Positions, Norm_Magnet_Forces)
            print("Fitted parameters of function:", optimizedParameters)
            fitted_Norm_Magnet_Forces = polyfunc(modelled.InnCoil_Positions, *optimizedParameters)
            print(Norm_Magnet_Forces)

            if fit == 1:
                InnCoil_Positions1 = modelled.InnCoil_Positions[8:13]
                Norm_Magnet_Forces1 = Norm_Magnet_Forces[8:13]
                optimizedParameters1, pcov = opt.curve_fit(polyfunc, InnCoil_Positions1, Norm_Magnet_Forces1)
                print("Fitted parameters of function at (-0.5,0.5):", optimizedParameters1)
                fitted_Norm_Magnet_Forces1 = polyfunc(InnCoil_Positions1, *optimizedParameters1)
                print(Norm_Magnet_Forces1)

                fiterr1 = Norm_Magnet_Forces - optimizedParameters1[0]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[1]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[2]
                print((abs(Norm_Magnet_Forces - fitted_Norm_Magnet_Forces) / abs(Norm_Magnet_Forces)) * 100)
                plt.plot(modelled.InnCoil_Positions, abs(fiterr1) / abs(Norm_Magnet_Forces) * 100)
                plt.ylabel('Normalised Fit error [%]')
                plt.xlabel('Inner Coil Position [mm]')
                # plt.ylim(0.0,0.01)
                plt.show()
                nor_fit1 = abs(fiterr1) / abs(Norm_Magnet_Forces)

                print(Norm_Magnet_Forces - fitted_Norm_Magnet_Forces)
                plt.plot(modelled.InnCoil_Positions, Norm_Magnet_Forces - fitted_Norm_Magnet_Forces)
                plt.plot(modelled.InnCoil_Positions, fiterr1)
                plt.ylabel('Fit error [N/A]')
                plt.xlabel('Inner Coil Position [mm]')
                plt.show()

            plt.plot(modelled.InnCoil_Positions, Norm_Magnet_Forces, "o-", color = "blue", label="simulation")
            #plt.plot(modelled.InnCoil_Positions, fitted_Norm_Magnet_Forces, 'o-', label="poly2 fit")
            #plt.plot(modelled.InnCoil_Positions, optimizedParameters1[0]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[1]*(
                         #np.array(modelled.InnCoil_Positions)) - optimizedParameters1[2], 'o--', label="fit")
            plt.ylabel('Normalised VC Force [N/A]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            plt.show()


        results = Results()

        class Save_data():
            def __init__(self):
                pass
            data = np.column_stack((modelled.InnCoil_Positions, modelled.UppOutCoil_Forces,
                                    modelled.LowOutCoil_Forces, modelled.Magnet_Forces,
                                    results.Norm_Magnet_Forces, results.fiterr, results.nor_fit, results.lin))
            np.savetxt(data_file, data)
            if data_save==1:
                with open(path, "w") as f:
                    f.write(data)
            pname = "pick" + self.filename
            pickle_out = open(pname, "wb")
            pickle.dump(data, pickle_out)
            pickle_out.close()
        #saved_data = Save_data()
