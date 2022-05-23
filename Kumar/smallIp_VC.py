import femm
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil
import design
import os


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
        NSteps = 20
        StepSize = 0.5
        InnCoil_Offset = -5

        sensor = design.Sensortype(0, 0, 1)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=self.parameter, inn_rad=9, inn_layers=6, inn_dist=0, out_ht=13.5, out_rad=20,
                              out_layers=5, out_dist=28.5, mag_len=40, mag_dia=10, ver_shi=0)

        data_file = self.filename
        multiple_fit = 1
        save = 0
        if save == 1:
            directory = data_file
            parent_dir = "C:\\Users\\kumar\\OneDrive\\Desktop\\pi\\bench"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            save_plot = path

        class Position():
            def __init__(self):
                pass

            def inncoil(self):
                InnCoil_OutRadius = geo.inncoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.inncoil()[2])
                InnCoil_Lowend = (geo.inncoil()[3] - geo.inncoil()[0]) / 2
                InnCoil_Uppend = InnCoil_Lowend + geo.inncoil()[0]
                InnCoil_NrWind_p_Layer = (geo.inncoil()[0]) / (wire.prop32()[0] + wire.prop32()[1] * 2)
                InnCoil_NrWindings = InnCoil_NrWind_p_Layer * geo.inncoil()[2]
                InnCoil_Circuit = "InnCoil_Circuit"
                return [InnCoil_OutRadius, InnCoil_Lowend, InnCoil_Uppend, InnCoil_NrWind_p_Layer, InnCoil_NrWindings,
                        InnCoil_Circuit]

            def upp_outcoil(self):
                UppOutCoil_OutRadius = geo.outcoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.outcoil()[2])
                UppOutCoil_LowEnd = (geo.outcoil()[3] - geo.outcoil()[0]) / 2
                UppOutCoil_UppEnd = UppOutCoil_LowEnd + geo.outcoil()[0]
                UppOutCoil_NrWind_p_Layer = (geo.outcoil()[0]) / (wire.prop32()[0] + wire.prop32()[1] * 2)
                UppOutCoil_NrWindings = UppOutCoil_NrWind_p_Layer * geo.outcoil()[2]
                UppOutCoil_Circuit = "UppOutCoil_Circuit"
                return [UppOutCoil_OutRadius, UppOutCoil_LowEnd, UppOutCoil_UppEnd, UppOutCoil_NrWind_p_Layer,
                        UppOutCoil_NrWindings, UppOutCoil_Circuit]

            def low_outcoil(self):
                LowOutCoil_OutRadius = geo.outcoil()[1] + ((wire.prop32()[0] + wire.prop32()[1] * 2) * geo.outcoil()[2])
                LowOutCoil_UppEnd = -1 * ((geo.outcoil()[3] - geo.outcoil()[0]) / 2)
                LowOutCoil_LowEnd = LowOutCoil_UppEnd - geo.outcoil()[0]
                LowOutCoil_NrWind_p_Layer = (LowOutCoil_UppEnd - LowOutCoil_LowEnd) / (
                        wire.prop32()[0] + wire.prop32()[1] * 2)
                LowOutCoil_NrWindings = LowOutCoil_NrWind_p_Layer * geo.outcoil()[2]
                LowOutCoil_Circuit = "LowOutCoil_Circuit"
                return [LowOutCoil_OutRadius, LowOutCoil_UppEnd, LowOutCoil_LowEnd, LowOutCoil_NrWind_p_Layer,
                        LowOutCoil_NrWindings, LowOutCoil_Circuit]

            def magnet(self):
                Magnet_UppEnd = geo.mag()[0] / 2 + geo.mag()[2]
                Magnet_LowEnd = -geo.mag()[0] / 2 + geo.mag()[2]
                Magnet_Radius = geo.mag()[1] / 2
                return [Magnet_UppEnd, Magnet_LowEnd, Magnet_Radius]
        position = Position()

        class Length():
            def __init__(self):
                pass

            def inncoil(self):
                InnCoil_TotalWire = 0
                for i in range(0, geo.inncoil()[2]):
                    # circ = 2*np.pi*InnCoil_InRadius+i*(InnCoil_WireDiam+InnCoil_WireInsul)
                    circ = 2 * np.pi * (geo.inncoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
                    InnCoil_TotalWire += circ * position.inncoil()[3]
                print("Total length of wire (mm):", InnCoil_TotalWire)
                print("\n")
                return InnCoil_TotalWire

            def upp_outcoil(self):
                UppOutCoil_TotalWire = 0
                for i in range(0, geo.outcoil()[2]):
                    # circ = 2*np.pi*(UppOutCoil_InRadius+i*(UppOutCoil_WireDiam+UppOutCoil_WireInsul))
                    circ = 2 * np.pi * (geo.outcoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
                    UppOutCoil_TotalWire += circ * position.upp_outcoil()[3]
                print("Total length of wire (mm):", UppOutCoil_TotalWire)
                print("\n")
                return UppOutCoil_TotalWire

            def low_outcoil(self):
                LowOutCoil_TotalWire = 0
                for i in range(0, geo.outcoil()[2]):
                    # circ = 2*np.pi*LowOutCoil_InRadius+i*(LowOutCoil_WireDiam+LowOutCoil_WireInsul)
                    circ = 2 * np.pi * (geo.outcoil()[1] + i * (wire.prop32()[0] + wire.prop32()[1] * 2))
                    LowOutCoil_TotalWire += circ * position.low_outcoil()[3]
                print("Total length of wire (mm):", LowOutCoil_TotalWire)
                print("\n")
                return LowOutCoil_TotalWire
        length = Length()

        class Modelling():
            def __init__(self):
                pass

            # InnerCoil Structure
            femm.mi_drawrectangle(geo.inncoil()[1], position.inncoil()[2], position.inncoil()[0], position.inncoil()[1])
            femm.mi_addcircprop(position.inncoil()[5], sensor.para()[0], 1)

            if wire.inncoil_material == "31 AWG":
                femm.mi_addmaterial('31 AWG', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2261)
            if wire.inncoil_material == "32 AWG":
                femm.mi_getmaterial(wire.inncoil_material)

            femm.mi_clearselected()
            femm.mi_selectrectangle(geo.inncoil()[1], position.inncoil()[2], position.inncoil()[0],
                                    position.inncoil()[1], 4)
            femm.mi_setgroup(1)
            femm.mi_clearselected()
            femm.mi_addblocklabel(geo.inncoil()[1] + wire.prop32()[1], position.inncoil()[1] + (geo.inncoil()[0] / 2))
            femm.mi_selectlabel(geo.inncoil()[1] + wire.prop32()[1], position.inncoil()[1] + (geo.inncoil()[0] / 2))
            femm.mi_setblockprop(wire.prop32()[2], 1, 0, position.inncoil()[5], 0, 1, position.inncoil()[4])
            femm.mi_clearselected()

            # UpperOutCoil Structure
            femm.mi_drawrectangle(geo.outcoil()[1], position.upp_outcoil()[2], position.upp_outcoil()[0],
                                  position.upp_outcoil()[1])
            femm.mi_addcircprop(position.upp_outcoil()[5], sensor.para()[2], 1)

            if wire.outcoil_material == "31 AWG":
                femm.mi_addmaterial('31 AWG', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2261)
            if wire.outcoil_material == "32 AWG":
                femm.mi_getmaterial(wire.inncoil_material)

            femm.mi_clearselected()
            femm.mi_selectrectangle(geo.outcoil()[1], position.upp_outcoil()[2], position.upp_outcoil()[0],
                                    position.upp_outcoil()[1], 4)
            femm.mi_setgroup(3)
            femm.mi_clearselected()
            femm.mi_addblocklabel(geo.outcoil()[1] + wire.prop32()[1],
                                  position.upp_outcoil()[2] - (geo.outcoil()[0] * 0.5))
            femm.mi_selectlabel(geo.outcoil()[1] + wire.prop32()[1],
                                position.upp_outcoil()[2] - (geo.outcoil()[0] * 0.5))
            femm.mi_setblockprop(wire.prop32()[2], 0, 0.1, position.upp_outcoil()[5], 0, 3, position.upp_outcoil()[4])
            femm.mi_clearselected()

            # LowerOutCoil Structure
            femm.mi_drawrectangle(geo.outcoil()[1], position.low_outcoil()[1], position.low_outcoil()[0],
                                  position.low_outcoil()[2])
            femm.mi_addcircprop(position.low_outcoil()[5], -sensor.para()[2], 1)

            if wire.outcoil_material == "31 AWG":
                femm.mi_addmaterial('31 AWG', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2261)
            if wire.outcoil_material == "32 AWG":
                femm.mi_getmaterial(wire.inncoil_material)

            femm.mi_clearselected()
            femm.mi_selectrectangle(geo.outcoil()[1], position.low_outcoil()[1], position.low_outcoil()[0],
                                    position.low_outcoil()[2], 4)
            femm.mi_setgroup(4)
            femm.mi_clearselected()
            femm.mi_addblocklabel(geo.outcoil()[1] + wire.prop32()[0],
                                  position.low_outcoil()[2] + (geo.outcoil()[0] * 0.5))
            femm.mi_selectlabel(geo.outcoil()[1] + wire.prop32()[0],
                                position.low_outcoil()[2] + (geo.outcoil()[0] * 0.5))
            femm.mi_setblockprop(wire.prop32()[2], 0, 0.1, position.low_outcoil()[5], 0, 4, position.low_outcoil()[4])
            femm.mi_clearselected()

            # Magnet Structure
            femm.mi_drawrectangle(0, position.magnet()[0], position.magnet()[2], position.magnet()[1])
            femm.mi_getmaterial(wire.mag_mat())
            femm.mi_clearselected()
            femm.mi_selectrectangle(0, position.magnet()[0], position.magnet()[2], position.magnet()[1], 4)
            femm.mi_setgroup(2)
            femm.mi_clearselected()
            femm.mi_addblocklabel(position.magnet()[2] * 0.5, position.magnet()[1] + (geo.mag()[0] * 0.5))
            femm.mi_selectlabel(position.magnet()[2] * 0.5, position.magnet()[1] + (geo.mag()[0] * 0.5))
            femm.mi_setblockprop(wire.mag_mat(), 0, 0.1, "", 90, 2, 0)
            femm.mi_clearselected()

            # AirSurrounding Structure
            AirSpaceRadius_1 = 100
            AirSpaceRadius_2 = 300
            BC_Name = "Outside"
            BC_Group = 10
            # Airspace1
            femm.mi_drawline(0, AirSpaceRadius_1, 0, -AirSpaceRadius_1)
            femm.mi_drawarc(0, -AirSpaceRadius_1, 0, AirSpaceRadius_1, 180, 2)
            femm.mi_getmaterial("Air")
            femm.mi_clearselected()
            femm.mi_addblocklabel(AirSpaceRadius_1 / 4, AirSpaceRadius_1 / 2)
            femm.mi_selectlabel(AirSpaceRadius_1 / 4, AirSpaceRadius_1 / 2)
            femm.mi_setblockprop("Air", 0, 0.5, '', 0, 0, 0)
            femm.mi_clearselected()
            # Airspace2
            femm.mi_drawline(0, AirSpaceRadius_2, 0, -AirSpaceRadius_2)
            femm.mi_drawarc(0, -AirSpaceRadius_2, 0, AirSpaceRadius_2, 180, 2)
            femm.mi_getmaterial("Air")
            femm.mi_clearselected()
            femm.mi_addblocklabel(AirSpaceRadius_2 / 2, AirSpaceRadius_2 / 1.2)
            femm.mi_selectlabel(AirSpaceRadius_2 / 2, AirSpaceRadius_2 / 1.2)
            femm.mi_setblockprop("Air", 1, 0, '', 0, 0, 0)
            femm.mi_clearselected()
            # Boundary properties
            femm.mi_addboundprop(BC_Name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            femm.mi_clearselected()
            femm.mi_selectarcsegment(0, AirSpaceRadius_2)
            femm.mi_setarcsegmentprop(2, BC_Name, 0, BC_Group)
            femm.mi_clearselected()

            UppOutCoil_Forces = np.zeros(NSteps + 1)
            LowOutCoil_Forces = np.zeros(NSteps + 1)
            Magnet_Forces = np.zeros(NSteps + 1)
            InnCoil_Positions = np.zeros(NSteps + 1)
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
        print(modelled.UppOutCoil_Forces)
        print(modelled.LowOutCoil_Forces)
        print(modelled.Magnet_Forces)

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

            plt.style.use(['science', 'grid', 'notebook'])

            plt.plot(modelled.InnCoil_Positions, modelled.LowOutCoil_Forces, 'o-')
            plt.ylabel('Lower Outer Coil Force [N]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("low for.png")
                shutil.move("low for.png", save_plot)
            plt.show()

            plt.plot(modelled.InnCoil_Positions, modelled.UppOutCoil_Forces, 'o-')
            plt.ylabel('Upper Outer Coil Force [N]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("upp for.png")
                shutil.move("upp for.png", save_plot)
            plt.show()

            plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces, 'o-')
            plt.ylabel('Magnet Force [N]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("mf.png")
                shutil.move("mf.png", save_plot)
            plt.show()

            plt.plot(modelled.InnCoil_Positions, modelled.LowOutCoil_Forces + modelled.UppOutCoil_Forces, 'o-')
            plt.ylabel('Sum of Outer Coil Force [N]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("outsum.png")
                shutil.move("outsum.png", save_plot)
            plt.show()

            plt.plot(modelled.InnCoil_Positions,
                     modelled.Magnet_Forces - abs(modelled.LowOutCoil_Forces + modelled.UppOutCoil_Forces), 'o-')
            plt.ylabel('Force on Magnet - Force on Outer Coils [N]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("mf - inn for.png")
                shutil.move("mf - inn for.png", save_plot)
            plt.show()

            plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100, 'o-')
            plt.ylabel('Magnet Forces/max force [%]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("nmf.png")
                shutil.move("nmf.png", save_plot)
            plt.show()
            lin = modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100

            def polyfunc(x, a, b, c):
                return a * x ** 2 + b * x + c

            Norm_Magnet_Forces = modelled.Magnet_Forces / sensor.para()[2]
            optimizedParameters, pcov = opt.curve_fit(polyfunc, modelled.InnCoil_Positions, Norm_Magnet_Forces)
            print("Fitted parameters of function:", optimizedParameters)
            fitted_Norm_Magnet_Forces = polyfunc(modelled.InnCoil_Positions, *optimizedParameters)
            print(Norm_Magnet_Forces)

            InnCoil_Positions1 = modelled.InnCoil_Positions[8:13]
            Norm_Magnet_Forces1 = Norm_Magnet_Forces[8:13]
            optimizedParameters1, pcov = opt.curve_fit(polyfunc, InnCoil_Positions1, Norm_Magnet_Forces1)
            print("Fitted parameters of function at (-0.5,0.5):", optimizedParameters1)
            fitted_Norm_Magnet_Forces1 = polyfunc(InnCoil_Positions1, *optimizedParameters1)
            print(Norm_Magnet_Forces1)

            fiterr1 = Norm_Magnet_Forces - optimizedParameters1[0]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[1]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[2]

            plt.plot(modelled.InnCoil_Positions, Norm_Magnet_Forces, label="simulation")
            plt.plot(modelled.InnCoil_Positions, fitted_Norm_Magnet_Forces, '--', label="poly2 fit")
            plt.plot(modelled.InnCoil_Positions,
                     optimizedParameters1[0]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters1[1]*(
                         np.array(modelled.InnCoil_Positions)) - optimizedParameters1[2], '--', label="0.5 fit")
            plt.ylabel('Normalised Magnet Force [N/A]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            if save == 1:
                plt.savefig("fit for.png")
                shutil.move("fit for.png", save_plot)
            plt.show()

            print(Norm_Magnet_Forces - fitted_Norm_Magnet_Forces)
            plt.plot(modelled.InnCoil_Positions, Norm_Magnet_Forces - fitted_Norm_Magnet_Forces)
            plt.plot(modelled.InnCoil_Positions, fiterr1)
            plt.ylabel('Fit error [N/A]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("fit err.png")
                shutil.move("fit err.png", save_plot)
            plt.show()

            print((abs(Norm_Magnet_Forces - fitted_Norm_Magnet_Forces) / abs(Norm_Magnet_Forces)) * 100)
            plt.plot(modelled.InnCoil_Positions, abs(fiterr1) / abs(Norm_Magnet_Forces) * 100)
            plt.ylabel('Normalised Fit error [%]')
            plt.xlabel('Inner Coil Position [mm]')
            if save == 1:
                plt.savefig("norfit.png")
                shutil.move("norfit.png", save_plot)
            # plt.ylim(0.0,0.01)
            plt.show()
            nor_fit1 = abs(fiterr1) / abs(Norm_Magnet_Forces)
        results = Results()

        class Save_data():
            def __init__(self):
                pass

            data = np.column_stack((modelled.InnCoil_Positions, modelled.UppOutCoil_Forces,
                                    modelled.LowOutCoil_Forces, modelled.Magnet_Forces,
                                    results.Norm_Magnet_Forces, results.fiterr1, results.nor_fit1, results.lin))
            np.savetxt(data_file, data)
        saved_data = Save_data()
