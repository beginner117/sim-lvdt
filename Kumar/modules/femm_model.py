import femm
import numpy as np

class Femm_bc():
    def __init__(self):
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

class Femm_coil():
        def __init__(self, x1, y1, x2, y2, circ_name, circ_current, circ_type, material, edit_mode, group, label1, label2, blockname, turns_pr_layer):
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
                self.circ_name = circ_name
                self.circ_current = circ_current
                self.circ_type = circ_type
                self.material = material
                self.edit_mode = edit_mode
                self.group = group
                self.label1 = label1
                self.label2 = label2
                self.blockname = blockname
                self.turns_pr_layer = turns_pr_layer
                femm.mi_drawrectangle(self.x1, self.y1, self.x2, self.y2)
                femm.mi_addcircprop(self.circ_name, self.circ_current, self.circ_type)
                if self.material == "31 AWG":
                    femm.mi_addmaterial('31 AWG', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2261)
                if self.material == "32 AWG":
                    femm.mi_getmaterial(self.material)
                femm.mi_clearselected()
                femm.mi_selectrectangle(self.x1, self.y1, self.x2,
                                        self.y2, self.edit_mode)
                femm.mi_setgroup(self.group)
                femm.mi_clearselected()
                femm.mi_addblocklabel(self.x1+self.label1, self.y2+(self.label2/2))
                femm.mi_selectlabel(self.x1+self.label1, self.y2+(self.label2/2))
                femm.mi_setblockprop(self.blockname, 1, 0, self.circ_name, 0, self.group, self.turns_pr_layer)
                femm.mi_clearselected()

class Femm_magnet():
        def __init__(self, x1, y1, x2, y2, material, edit_mode, group, label1, label2):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.material = material
            self.edit_mode = edit_mode
            self.group = group
            self.label1 = label1
            self.label2 = label2

            femm.mi_drawrectangle(self.x1, self.y1, self.x2, self.y2)
            femm.mi_getmaterial(self.material)
            femm.mi_clearselected()
            femm.mi_selectrectangle(self.x1, self.y1, self.x2, self.y2, self.edit_mode)
            femm.mi_setgroup(self.group)
            femm.mi_clearselected()
            femm.mi_addblocklabel(self.x1+self.label1, self.y2+(self.label2/2))
            femm.mi_selectlabel(self.x1+self.label1, self.y2+(self.label2/2))
            femm.mi_setblockprop(self.material, 0, 0.1, "", 90, self.group, 0)
            femm.mi_clearselected()

class Output():
    def __init__(self, Nsteps):
        self.Nsteps = Nsteps
    def currents(self):
        UppOutCoil_Currents = np.zeros(self.Nsteps + 1).astype(complex)
        LowOutCoil_Currents = np.zeros(self.Nsteps + 1).astype(complex)
        InnCoil_Currents = np.zeros(self.Nsteps + 1).astype(complex)
        return [InnCoil_Currents, UppOutCoil_Currents, LowOutCoil_Currents]
    def voltages(self):
        UppOutCoil_Voltages = np.zeros(self.Nsteps + 1).astype(complex)
        LowOutCoil_Voltages = np.zeros(self.Nsteps + 1).astype(complex)
        InnCoil_Voltages = np.zeros(self.Nsteps + 1).astype(complex)
        InnCoil_Positions = np.zeros(self.Nsteps + 1)
        return [InnCoil_Voltages, UppOutCoil_Voltages, LowOutCoil_Voltages]
    def flux(self):
        UppOutCoil_Flux = np.zeros(self.Nsteps + 1).astype(complex)
        LowOutCoil_Flux = np.zeros(self.Nsteps + 1).astype(complex)
        InnCoil_Flux = np.zeros(self.Nsteps + 1).astype(complex)
        return [InnCoil_Flux, UppOutCoil_Flux, LowOutCoil_Flux]
    def metadata(self):
        metadata = np.zeros(self.Nsteps + 1)
        return metadata

class EM():
    def __init__(self, steps, current=None, voltage=None, flux=None):
        self.steps = steps
        self.current = current
        self.voltage = voltage
        self.flux = flux
        if self.current:
            return
            UppOutCoil_Voltages = np.zeros(self.steps + 1).astype(complex)
            LowOutCoil_Voltages = np.zeros(self.steps + 1).astype(complex)
            InnCoil_Voltages = np.zeros(self.steps + 1).astype(complex)



'''
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
'''
'''
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
'''
