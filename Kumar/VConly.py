import modules.design as design
import femm
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import dataplot_condition
import modules.femm_model as femm_model
import modules.coil as coil


class Analysis():
    def __init__(self, parameter, filename: str):
        self.parameter = parameter
        # self.parameter2 = parameter2
        self.filename = filename

    def simulate(self):
        femm.openfemm()
        femm.newdocument(0)

        outputfile = 'LVDT_10kHz_20mA_31AWG_10mm_6_7_7.out'
        NSteps = 10
        StepSize = 1
        InnCoil_Offset = 5.5

        #sensor = design.Sensortype(0, 0, 1)
        sensor = design.Sensortype(0.02, 10000, 0)
        femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
        wire = design.Wiretype("32 AWG", "32 AWG")
        geo = design.Geometry(inn_ht=5.2, inn_rad=10, inn_layers=8, inn_dist=self.parameter, out_ht=10, out_rad=25,
                              out_layers=7, out_dist=36, mag_len=3, mag_dia=1.5, ver_shi=0)
        multiple_fit = 0
        '''
        position = coil.Position(geo.inncoil()[0], geo.inncoil()[1], geo.inncoil()[2], geo.inncoil()[3],
                                 geo.outcoil()[0], geo.outcoil()[1], geo.outcoil()[2], geo.outcoil()[3],
                                 geo.mag()[2], wire.prop32()[0], wire.prop32()[1], wire.prop32()[0], wire.prop32()[1],
                                 geo.mag()[0], geo.mag()[1])
        length = coil.Length(geo.inncoil()[2], geo.inncoil()[1], wire.prop32()[0], wire.prop32()[1],
                             position.inncoil()[3], geo.outcoil()[2], geo.outcoil()[1],
                             wire.prop32()[0], wire.prop32()[1], position.upp_outcoil()[3])
        '''

        class Position():
            def __init__(self):
                pass

            def inncoil(self):
                InnCoil_OutRadius = geo.inncoil()[1] + ((wire.prop_inn()[0] + wire.prop_inn()[1] * 2) * geo.inncoil()[2])
                InnCoil_Lowend = (geo.inncoil()[3] - geo.inncoil()[0]) / 2
                InnCoil_Uppend = InnCoil_Lowend + geo.inncoil()[0]
                InnCoil_NrWind_p_Layer = (geo.inncoil()[0]) / (wire.prop_inn()[0] + wire.prop_inn()[1] * 2)
                InnCoil_NrWindings = InnCoil_NrWind_p_Layer * geo.inncoil()[2]
                InnCoil_Circuit = "InnCoil_Circuit"
                return [InnCoil_OutRadius, InnCoil_Lowend, InnCoil_Uppend, InnCoil_NrWind_p_Layer, InnCoil_NrWindings,
                        InnCoil_Circuit]

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
        length = Length()

        class Modelling():
            def __init__(self):
                pass
            inncoil_str = femm_model.Femm_coil(x1=geo.inncoil()[1], y1=position.inncoil()[2], x2=position.inncoil()[0], y2=position.inncoil()[1],
                                              circ_name=position.inncoil()[5], circ_current=sensor.para()[2], circ_type=1, material=wire.inncoil_material,
                                              edit_mode=4, group=1, label1=wire.prop32()[1], label2=geo.inncoil()[0], blockname=wire.prop32()[2],
                                              turns_pr_layer=position.inncoil()[4])
            magnetstr = femm_model.Femm_magnet(x1=0, y1=position.inncoil()[1], x2=position.magnet()[2],
                                               y2=position.inncoil()[1]-geo.mag()[0], material=wire.mag_mat(), edit_mode=4, group=2,
                                               label1=position.magnet()[2] * 0.5, label2=geo.mag()[0])
            bc = femm_model.Femm_bc()


            InnCoil_Voltages = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Positions = np.zeros(NSteps + 1)
            InnCoil_Currents = np.zeros(NSteps + 1).astype(complex)
            InnCoil_Flux = np.zeros(NSteps + 1).astype(complex)
            Magnet_Forces = np.zeros(NSteps + 1).astype(complex)
            MetaData = np.zeros(NSteps + 1)

            #femm.mi_selectgroup(1)
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

                femm.mo_groupselectblock(2)
                Magn_Force19 = femm.mo_blockintegral(19)
                femm.mo_clearblock()

                modelled.Magnet_Forces[i] = Magn_Force19
                InnCoil_I, InnCoil_V, InnCoil_FluxLink = femm.mo_getcircuitproperties(position.inncoil()[5])
                modelled.InnCoil_Voltages[i] = InnCoil_V
                modelled.InnCoil_Currents[i] = InnCoil_I
                modelled.InnCoil_Flux[i] = InnCoil_FluxLink

                #femm.mi_selectgroup(1)
                femm.mi_selectgroup(2)
                femm.mi_movetranslate(0, StepSize)
                femm.mi_clearselected()

        loop = Computational_loop()
        print(modelled.InnCoil_Positions)
        print("magnet forces are: ", modelled.Magnet_Forces)
        print("Inn voltages :", modelled.InnCoil_Voltages)
        Inn_Inductance = abs(modelled.InnCoil_Flux / modelled.InnCoil_Currents)
        Inn_resistance = abs(modelled.InnCoil_Voltages / modelled.InnCoil_Currents)
        print("average Inn coil Inductance is :", sum(Inn_Inductance) / len(Inn_Inductance))
        print("average Inn coil resistance is :", sum(Inn_resistance) / len(Inn_resistance))



        plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces, 'o-')
        plt.ylabel('Magnet Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.show()

        plt.plot(modelled.InnCoil_Positions, modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100, 'o-')
        plt.ylabel('Magnet Forces/max force [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.show()
        lin = modelled.Magnet_Forces / max(modelled.Magnet_Forces) * 100

        def polyfunc(x, a, b, c):
            return a * x ** 2 + b * x + c

        Norm_Magnet_Forces = modelled.Magnet_Forces / sensor.para()[2]
        optimizedParameters, pcov = opt.curve_fit(polyfunc, modelled.InnCoil_Positions, Norm_Magnet_Forces)
        print("Fitted parameters of function:", optimizedParameters)
        fitted_Norm_Magnet_Forces = polyfunc(modelled.InnCoil_Positions, *optimizedParameters)
        fiterr = Norm_Magnet_Forces - optimizedParameters[0]*((np.array(modelled.InnCoil_Positions))**2) - optimizedParameters[1]*(np.array(modelled.InnCoil_Positions)) - optimizedParameters[2]

        plt.plot(modelled.InnCoil_Positions, Norm_Magnet_Forces, label="simulation")
        #plt.plot(modelled.InnCoil_Positions, fitted_Norm_Magnet_Forces, 'o--', label="poly2 fit")
        plt.plot(modelled.InnCoil_Positions,
                 optimizedParameters[0]*((np.array(modelled.InnCoil_Positions))**2) - optimizedParameters[1]*(
                     np.array(modelled.InnCoil_Positions)) - optimizedParameters[2], 'o--', label="fit")
        plt.ylabel('Normalised Magnet Force [N/A]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        plt.show()

        print((abs(Norm_Magnet_Forces - fitted_Norm_Magnet_Forces) / abs(Norm_Magnet_Forces)) * 100)
        plt.plot(modelled.InnCoil_Positions, abs(fiterr) / abs(Norm_Magnet_Forces) * 100)
        plt.ylabel('Normalised Fit error [%]')
        plt.xlabel('Inner Coil Position [mm]')
        # plt.ylim(0.0,0.01)
        plt.show()
        nor_fit1 = abs(fiterr) / abs(Norm_Magnet_Forces)


si = Analysis('tr', 0)
si.simulate()






