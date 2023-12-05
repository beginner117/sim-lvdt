import femm

class Femm_bc():
    def __init__(self, AirSpaceRadius_1, AirSpaceRadius_2, BC_Name, BC_Group, material:str):
        """
        This method defines and creates the boundary conditions for the FEMM model
        _____________INPUT_________
        AirSpaceRadius_1: radius of the selected space1_(float)
        AirSpaceRadius_2: radius of the selected space2_(float)
        BC_Name: name of the boundary region_(string)
        BC_Group: group number of the region_(integer)
        material: material of the boundary region, vacuum, air e.t.c_(string)___should be chosen from the material library in FEMM
        ____________OUTPUT_________
        creates boundary conditions with the above properties for simulation
        NO return values
        """
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
            """
            This method defines and creates a (circular) coil with defined current
            ____________________INPUT_______________
            x1:  x-coordinate of the edge of the rectangle [planar view of circular the coil is a rectangle]_(float)
            y1: y-coordinate of the edge of the rectangle [planar view of circular the coil is a rectangle]_(float)
            x2: x-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
            y2: y-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
            circ_name: name of the circuit_(string)
            circ_type: type of connection['0' for parallel and '1' for series]_(0 or 1)
            material: material of the coil/wire chosen from the FEMM library_(string)
            edit_mode: entities in the model block that can be edited when the block is selected_(0-nodes, 1-block labels
                        2-segments, 3-arcs, 4-all entity types)
            group: group of the coil_(integer)
            label1: x-coordinate of block label location
            label2: y-coordinate of block label location
            blockname: name of the block
            turns_pr_layer: number of turns per layer_(float)
            ___________________OUTPUT______________
            creates a coil with the defined properties and current
            NO return value
            """
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
            try:
                femm.mi_getmaterial(self.material)
            except:
                if self.material == "31 AWG":
                    femm.mi_addmaterial('31 AWG', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2261)
                if self.material == "electrisola_1a":
                    femm.mi_addmaterial('electrisola_1a', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.190)
                if self.material == "electrisola_2a":
                    femm.mi_addmaterial('electrisola_2a', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.200)
                if self.material == "electrisola_1b":
                    femm.mi_addmaterial('electrisola_1b', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.190)
                if self.material == "electrisola_2b":
                    femm.mi_addmaterial('electrisola_2b', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.200)
                if self.material == "electrisola_2c":
                    femm.mi_addmaterial('electrisola_2c', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.200)
                if self.material == "32 AWG_corrected_1":
                    femm.mi_addmaterial('32 AWG_corrected_1', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2032)
                if self.material == "32 AWG_corrected_2":
                    femm.mi_addmaterial('32 AWG_corrected_2', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2032)
                if self.material == "RS":
                    femm.mi_addmaterial('RS', 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, 0.2)



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
            """
            This method defines and creates a magnet
            ____________________INPUT_______________
            x1: x-coordinate of the edge of the rectangle [planar view of cylindrical magnet is a rectangle]_(float)
            y1: y-coordinate of the edge of the rectangle [planar view of cylindrical magnet is a rectangle]_(float)
            x2: x-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
            y2: y-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
            material: material of the magnet chosen from the FEMM library_(string)
            edit_mode:
            group: group of the magnet_(integer)
            label1:
            label2:
            ___________________OUTPUT______________
            modells a magnet with the defined properties
            NO return value
            """
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
            try:
                femm.mi_getmaterial(self.material)
            except:
                if self.material == "low":
                    femm.mi_addmaterial('low', 1.05, 1.05, 860000, 0, 0.667, 0, 0, 1, 0, 0, 0, 1, 0)
                if self.material == "high":
                    femm.mi_addmaterial('high', 1.05, 1.05, 955000, 0, 0.667, 0, 0, 1, 0, 0, 0, 1, 0)

            femm.mi_clearselected()
            femm.mi_selectrectangle(self.x1, self.y1, self.x2, self.y2, self.edit_mode)
            femm.mi_setgroup(self.group)
            femm.mi_clearselected()
            femm.mi_addblocklabel(self.x1+self.label1, self.y2+(self.label2/2))
            femm.mi_selectlabel(self.x1+self.label1, self.y2+(self.label2/2))
            femm.mi_setblockprop(self.material, 0, 0.1, "", 90, self.group, 0)
            femm.mi_clearselected()

class Femm_move:
    def __init__(self, groups:list, x_dist, y_dist):
        """
        moves the selected groups/blocks to the specified coordinates
        __________INPUT__________
        groups : groups that need to be translated_(list)
        x_dist : target x-coordinate_(float)
        y_dist : target y-coordinate_(float)
        __________OUTPUT_______
        output : moves the selected blocks (no return values)

        """
        self.group = groups
        self.x_dist = x_dist
        self.y_dist = y_dist

        for i in range(len(self.group)):
            femm.mi_selectgroup(self.group[i])
        femm.mi_movetranslate(self.x_dist, self.y_dist)
        femm.mi_clearselected()

class Femm_block():
    def __init__(self, x1, y1, x2, y2, material, edit_mode, group, label1, label2):
        """
        This method defines and creates a metal block
        ____________________INPUT_______________
        x1: x-coordinate of the edge of the rectangle [planar view of cylindrical block is a rectangle]_(float)
        y1: y-coordinate of the edge of the rectangle [planar view of cylindrical block is a rectangle]_(float)
        x2: x-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
        y2: y-coordinate of the diagonally opposite edge of (x1,y1) on the rectangle _ (float)
        material: material of the block chosen from the FEMM library_(string)
        edit_mode:
        group: group of the block_(integer)
        label1:
        label2:
        ___________________OUTPUT______________
        models a block with the defined properties
        NO return value
        """
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

class Load_coil:
    def __init__(self, coil_name):
        self.name = coil_name
        femm.mi_zoom(-2, -50, 50, 50)
        femm.mi_refreshview()
        femm.mi_saveas('LVDT position_ETpf_LIP.fem')  # We have to give the geometry a name before we can analyze it.
        femm.mi_analyze()  # Now,analyze the problem and load the solution when the analysis is finished
        femm.mi_loadsolution()
    def simulate(self):
        Coil_I, Coil_V, Coil_FluxLink = femm.mo_getcircuitproperties(self.name)
        return [Coil_I, Coil_V, Coil_FluxLink]
