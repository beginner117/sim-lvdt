import femm

class Femm_bc():
    def __init__(self, AirSpaceRadius_1, AirSpaceRadius_2, BC_Name, BC_Group, material:str):
        self.AirSpaceRadius_1 = AirSpaceRadius_1
        self.AirSpaceRadius_2 = AirSpaceRadius_2
        self.BC_Name = BC_Name
        self.BC_Group = BC_Group
        self.material = material

        # Airspace1
        femm.mi_drawline(0, self.AirSpaceRadius_1, 0, -self.AirSpaceRadius_1)
        femm.mi_drawarc(0, -self.AirSpaceRadius_1, 0, self.AirSpaceRadius_1, 180, 2)
        femm.mi_getmaterial("Air")
        femm.mi_clearselected()
        femm.mi_addblocklabel(self.AirSpaceRadius_1 / 4, self.AirSpaceRadius_1 / 2)
        femm.mi_selectlabel(self.AirSpaceRadius_1 / 4, self.AirSpaceRadius_1 / 2)
        femm.mi_setblockprop("Air", 0, 0.5, '', 0, 0, 0)
        femm.mi_clearselected()
        # Airspace2
        femm.mi_drawline(0, self.AirSpaceRadius_2, 0, -self.AirSpaceRadius_2)
        femm.mi_drawarc(0, -self.AirSpaceRadius_2, 0, self.AirSpaceRadius_2, 180, 2)
        femm.mi_getmaterial("Air")
        femm.mi_clearselected()
        femm.mi_addblocklabel(self.AirSpaceRadius_2 / 2, self.AirSpaceRadius_2 / 1.2)
        femm.mi_selectlabel(self.AirSpaceRadius_2 / 2, self.AirSpaceRadius_2 / 1.2)
        femm.mi_setblockprop("Air", 1, 0, '', 0, 0, 0)
        femm.mi_clearselected()
        # Boundary properties
        femm.mi_addboundprop(self.BC_Name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        femm.mi_clearselected()
        femm.mi_selectarcsegment(0, self.AirSpaceRadius_2)
        femm.mi_setarcsegmentprop(2, self.BC_Name, 0, self.BC_Group)
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
                if self.material == "34 AWG":
                    femm.mi_getmaterial(self.material)
                if self.material == "32 AWG_corrected_1":
                    femm.mi_addmaterial('32 AWG_corrected_1', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2032)
                if self.material == "32 AWG_corrected_2":
                    femm.mi_addmaterial('32 AWG_corrected_2', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2032)
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

class Femm_block():
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
        femm.mi_addblocklabel(self.x1 + (self.label1/2), self.y2 + (self.label2 / 2))
        femm.mi_selectlabel(self.x1 + (self.label1/2), self.y2 + (self.label2 / 2))
        femm.mi_setblockprop(self.material, 0, 0.1, "", 0, self.group, 0)
        femm.mi_clearselected()
