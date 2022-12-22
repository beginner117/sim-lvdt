import sys
sys.path.insert(1, "C://Users//kumar//PycharmProjects//lvdtsimulations//Kumar//modules")
import design
import femm
import numpy as np
import matplotlib.pyplot as plt
import femm_model
import coil
import shutil
femm.openfemm()
femm.newdocument(0)

outputfile = 'small_F0_MirrorTower_1mA_32AWG_6_5_5.out'
NSteps = 6
StepSize = 1
Upp_Inncoil_Offset = -5.5
save = 0

sensor = design.Sensortype(1, 0, 0)
femm.mi_probdef(sensor.para()[1], 'millimeters', 'axi', 1.0e-10)
wire = design.Wiretype("32 AWG", "32 AWG")
block = design.Blocks()
geo = design.Geometry1(innUP_ht=18, innLOW_ht=23, inn_rad=21, inn_layers=6, inn_dist=60.5, out_ht=13.5, out_rad=31.5,
                       out_layers=5, out_dist=14.5, mag_ht=6.35, mag_rad=12.80, ver_shi=0)

class Position():
    def __init__(self):
        pass
    def Low_Inncoil(self):
        Low_Inncoil_OutRadius = geo.Low_Inncoil()[1] + ((wire.prop31()[0] + wire.prop31()[1] * 2) * geo.Low_Inncoil()[2])
        Low_Inncoil_Lowend = -1 * (geo.Low_Inncoil()[3] + (geo.Low_Inncoil()[0]) / 2)
        Low_Inncoil_Uppend = Low_Inncoil_Lowend + geo.Low_Inncoil()[0]
        Low_Inncoil_NrWind_p_Layer = (geo.Upp_Inncoil()[0]) / (wire.prop31()[0] + wire.prop31()[1] * 2)
        Low_Inncoil_NrWindings = Low_Inncoil_NrWind_p_Layer * geo.Upp_Inncoil()[2]
        Low_Inncoil_Circuit = "Low_Inncoil_Circuit"
        return [Low_Inncoil_OutRadius, Low_Inncoil_Lowend, Low_Inncoil_Uppend, Low_Inncoil_NrWind_p_Layer, Low_Inncoil_NrWindings, Low_Inncoil_Circuit]
position = Position()

class Yoke():
    def __init__(self):
        pass

    def block1(self):
        b1_lowend = -1 * (geo.Low_Inncoil()[3] + (block.b3()[1]) / 2 + block.b4()[1] + geo.mag()[0] + block.b6()[1])
        b1_uppend = b1_lowend + block.b1()[1]
        b1_innrad = block.yokeinnrad
        b1_outrad = b1_innrad + block.b1()[0]
        return [b1_innrad, b1_uppend, b1_outrad, b1_lowend]

    def block2(self):
        b2_innrad = block.yokeinnrad + block.b1_l
        b2_uppend = block.yokeuppend
        b2_lowend = b2_uppend - block.b2_h
        b2_outrad = b2_innrad + block.b2_l
        return [b2_innrad, b2_uppend, b2_outrad, b2_lowend]

    def block3(self):
        b3_innrad = geo.Low_Inncoil()[1] + block.innyoke_gap
        b3_outrad = b3_innrad + block.b3_l
        b3_uppend = block.yokeuppend
        b3_lowend = b3_uppend - block.b3_h
        return [b3_innrad, b3_uppend, b3_outrad, b3_lowend]

    def block4(self):
        b4_innrad = block.yokeoutrad - block.b4_l
        b4_uppend = block.yokeuppend - block.b3_h
        b4_outrad = b4_innrad + block.b4_l
        b4_lowend = b4_uppend - block.b4_h
        return [b4_innrad, b4_uppend, b4_outrad, b4_lowend]

    def block5(self):
        b5_innrad = block.yokeoutrad - geo.mag_rad - block.b5_l
        b5_uppend = block.yokeuppend - block.b3_h - block.b4_h
        b5_outrad = b5_innrad + block.b5_l
        b5_lowend = b5_uppend - block.b5_h
        return [b5_innrad, b5_uppend, b5_outrad, b5_lowend]

    def block6(self):
        b6_innrad = block.yokeoutrad - geo.mag()[1]
        b6_uppend = block.yokeuppend - block.b3_h - block.b4_h - geo.mag()[0]
        b6_outrad = b6_innrad + block.b6_l
        b6_lowend = b6_uppend - block.b6_h
        return [b6_innrad, b6_uppend, b6_outrad, b6_lowend]

    def block7(self):
        b7_innrad = block.yokeinnrad + block.b1_l
        b7_outrad = b7_innrad + block.b7_l
        b7_lowend = block.yokeuppend - block.b3_h - block.b4_h - geo.mag()[0] - block.b6_h
        b7_uppend = b7_lowend + block.b7_h
        return [b7_innrad, b7_uppend, b7_outrad, b7_lowend]

    def mag(self):
        mag_innrad = block.yokeoutrad - geo.mag()[1]
        mag_outrad = mag_innrad + geo.mag()[1]
        mag_uppend = block.yokeuppend - block.b3_h - block.b4_h
        mag_lowend = mag_uppend - geo.mag()[0]
        #mag_lowend = block.yokeuppend - (block.b1()[1])/2 - (geo.mag()[0])/2
        # mag_uppend = block.yokeuppend - (block.b1()[1])/2 + (geo.mag()[0])/2
        return [mag_innrad, mag_uppend, mag_outrad, mag_lowend]
yoke = Yoke()

material = wire.yoke_mat()

class Block_str():
    def __init__(self, b1, b2, b3, b4, b5, b6, b7):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
blo = Block_str(b1=1, b2=1, b3=1, b4=1, b5=1, b6=1, b7=1)

class Modelling():
    def __init__(self):
        pass
    # LowInnerCoil Structure

    femm.mi_drawrectangle(geo.Low_Inncoil()[1], position.Low_Inncoil()[2], position.Low_Inncoil()[0],
                          position.Low_Inncoil()[1])
    femm.mi_addcircprop(position.Low_Inncoil()[5], sensor.para()[0], 1)
    if wire.inncoil_material == "32 AWG":
        femm.mi_getmaterial(wire.inncoil_material)
    femm.mi_clearselected()
    femm.mi_selectrectangle(geo.Low_Inncoil()[1], position.Low_Inncoil()[2], position.Low_Inncoil()[0],
                            position.Low_Inncoil()[1], 4)
    femm.mi_setgroup(3)
    femm.mi_clearselected()
    femm.mi_addblocklabel(geo.Low_Inncoil()[1] + wire.prop32()[1],
                          position.Low_Inncoil()[1] + (geo.Low_Inncoil()[0] / 2))
    femm.mi_selectlabel(geo.Low_Inncoil()[1] + wire.prop32()[1], position.Low_Inncoil()[1] + (geo.Low_Inncoil()[0] / 2))
    femm.mi_setblockprop(wire.prop32()[2], 1, 0, position.Low_Inncoil()[5], 0, 3, position.Low_Inncoil()[4])
    femm.mi_clearselected()
    print("startpoint is ", geo.Low_Inncoil()[1])

    # block1
    if blo.b1 == 1:
        femm.mi_drawrectangle(yoke.block1()[0], yoke.block1()[1], yoke.block1()[2], yoke.block1()[3])
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block1()[0], yoke.block1()[1], yoke.block1()[2], yoke.block1()[3], 4)
        femm.mi_setgroup(6)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block1()[0] + (block.b1_l * 0.5), yoke.block1()[3] + (block.b1_h * 0.5))
        femm.mi_selectlabel(yoke.block1()[0] + (block.b1_l * 0.5), yoke.block1()[3] + (block.b1_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 6, 0)
        femm.mi_clearselected()
        print("simulating b1")

    # block2 0.07
    if blo.b2 == 1:
        femm.mi_drawrectangle(yoke.block2()[0]+0.01, yoke.block2()[1], yoke.block2()[2], yoke.block2()[3])
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block2()[0]+0.01, yoke.block2()[1], yoke.block2()[2], yoke.block2()[3], 4)
        femm.mi_setgroup(7)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block2()[0] + (block.b2_l * 0.5), yoke.block2()[3] + (block.b2_h * 0.5))
        femm.mi_selectlabel(yoke.block2()[0] + (block.b2_l * 0.5), yoke.block2()[3] + (block.b2_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 7, 0)
        femm.mi_clearselected()
        print("simulating b2")

    # block3 0.1
    if blo.b3 == 1:
        femm.mi_drawrectangle(yoke.block3()[0], yoke.block3()[1], yoke.block3()[2], yoke.block3()[3]+0.01)
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block3()[0], yoke.block3()[1], yoke.block3()[2], yoke.block3()[3]+0.01, 4)
        femm.mi_setgroup(8)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block3()[0] + (block.b3_l * 0.5), yoke.block3()[3] + (block.b3_h * 0.5))
        femm.mi_selectlabel(yoke.block3()[0] + (block.b3_l * 0.5), yoke.block3()[3] + (block.b3_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 8, 0)
        femm.mi_clearselected()
        print("simulating b3")

    # block4
    if blo.b4 == 1:
        femm.mi_drawrectangle(yoke.block4()[0], yoke.block4()[1], yoke.block4()[2], yoke.block4()[3]+0.01)
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block4()[0], yoke.block4()[1], yoke.block4()[2], yoke.block4()[3]+0.01, 4)
        femm.mi_setgroup(9)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block4()[0] + (block.b4_l * 0.5), yoke.block4()[3] + (block.b4_h * 0.5))
        femm.mi_selectlabel(yoke.block4()[0] + (block.b4_l * 0.5), yoke.block4()[3] + (block.b4_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 9, 0)
        femm.mi_clearselected()
        print("simulating b4")

    # block5
    if blo.b5 == 1:
        femm.mi_drawrectangle(yoke.block5()[0], yoke.block5()[1], yoke.block5()[2]-0.01, yoke.block5()[3])
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block5()[0], yoke.block5()[1], yoke.block5()[2]-0.01, yoke.block5()[3], 4)
        femm.mi_setgroup(10)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block5()[0] + (block.b5_l * 0.5), yoke.block5()[3] + (block.b5_h * 0.5))
        femm.mi_selectlabel(yoke.block5()[0] + (block.b5_l * 0.5), yoke.block5()[3] + (block.b5_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 10, 0)
        femm.mi_clearselected()
        print("simulating b5")

    # block6
    if blo.b6 == 1:
        femm.mi_drawrectangle(yoke.block6()[0], yoke.block6()[1]-0.01, yoke.block6()[2], yoke.block6()[3])
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block6()[0], yoke.block6()[1]-0.01, yoke.block6()[2], yoke.block6()[3], 4)
        femm.mi_setgroup(11)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block6()[0] + (block.b6_l * 0.5), yoke.block6()[3] + (block.b6_h * 0.5))
        femm.mi_selectlabel(yoke.block6()[0] + (block.b6_l * 0.5), yoke.block6()[3] + (block.b6_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 11, 0)
        femm.mi_clearselected()
        print("simulating b6")

    # block7
    if blo.b7 == 1:
        femm.mi_drawrectangle(yoke.block7()[0]+0.01, yoke.block7()[1], yoke.block7()[2]-0.01, yoke.block7()[3])
        femm.mi_getmaterial(material)
        femm.mi_clearselected()
        femm.mi_selectrectangle(yoke.block7()[0]+0.01, yoke.block7()[1], yoke.block7()[2]-0.01, yoke.block7()[3], 4)
        femm.mi_setgroup(12)
        femm.mi_clearselected()
        femm.mi_addblocklabel(yoke.block7()[0] + (block.b7_l * 0.5), yoke.block7()[3] + (block.b7_h * 0.5))
        femm.mi_selectlabel(yoke.block7()[0] + (block.b7_l * 0.5), yoke.block7()[3] + (block.b7_h * 0.5))
        femm.mi_setblockprop(material, 0, 0.1, "", 0, 12, 0)
        femm.mi_clearselected()
        print("simulating b7")

    # magnet Structure
    femm.mi_drawrectangle(yoke.mag()[0], yoke.mag()[1], yoke.mag()[2], yoke.mag()[3])
    femm.mi_getmaterial(wire.mag_mat())
    femm.mi_clearselected()
    femm.mi_selectrectangle(yoke.mag()[0], yoke.mag()[1], yoke.mag()[2], yoke.mag()[3], 4)
    femm.mi_setgroup(5)
    femm.mi_clearselected()
    femm.mi_addblocklabel(yoke.mag()[0] + (geo.mag()[1] * 0.5), yoke.mag()[3] + (geo.mag()[0] * 0.5))
    femm.mi_selectlabel(yoke.mag()[0] + (geo.mag()[1] * 0.5), yoke.mag()[3] + (geo.mag()[0] * 0.5))
    femm.mi_setblockprop(wire.mag_mat(), 0, 0.1, "", 90, 5, 0)
    femm.mi_clearselected()

    # AirSurrounding Structure
    AirSpaceRadius_1 = 200
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
    #femm.mi_drawline(0, -200, 0, -AirSpaceRadius_2)
    femm.mi_drawarc(0, -AirSpaceRadius_2, 0, AirSpaceRadius_2, 180, 2)
    #femm.mi_drawarc(0, -200, 0, AirSpaceRadius_2, 180, 2)
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

    Magnet_Forces1 = np.zeros(NSteps + 1)
    Magnet_Forces_m = np.zeros(NSteps + 1)
    Magnet_Forces_c = np.zeros(NSteps + 1)
    Magnet_Forces2 = np.zeros(NSteps + 1)
    Magnet_Forces3 = np.zeros(NSteps + 1)
    Magnet_Forces4 = np.zeros(NSteps + 1)
    Magnet_Forces5 = np.zeros(NSteps + 1)
    Magnet_Forces6 = np.zeros(NSteps + 1)
    Magnet_Forces7 = np.zeros(NSteps + 1)
    tot_mag = np.zeros(NSteps + 1)
    InnCoil_Positions = np.zeros(NSteps + 1)
    MetaData = np.zeros(NSteps + 1)
    femm.mi_selectgroup(3)
    femm.mi_movetranslate(0, Upp_Inncoil_Offset)
    femm.mi_clearselected()
modelled = Modelling()

class Computation_loop():
    def __init__(self):
        pass
    for i in range(0, NSteps + 1):
        print(Upp_Inncoil_Offset + StepSize * i)
        modelled.InnCoil_Positions[i] = Upp_Inncoil_Offset + (StepSize * i)
        femm.mi_zoom(-2, -50, 50, 50)
        femm.mi_refreshview()
        femm.mi_saveas('Mirror_tower position_ETpf_LIP.fem')
        femm.mi_analyze()
        femm.mi_loadsolution()

        femm.mo_groupselectblock(5)
        Magn_Force_m = femm.mo_blockintegral(19)
        femm.mo_clearblock()
        modelled.Magnet_Forces_m[i] = Magn_Force_m

        femm.mo_groupselectblock(3)
        Magn_Force_c = femm.mo_blockintegral(19)
        femm.mo_clearblock()
        modelled.Magnet_Forces_c[i] = Magn_Force_c

        if blo.b1 == 1:
            femm.mo_groupselectblock(6)
            Magn_Force1 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces1[i] = Magn_Force1

        if blo.b2 == 1:
            femm.mo_groupselectblock(7)
            Magn_Force2 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces2[i] = Magn_Force2

        if blo.b3 == 1:
            femm.mo_groupselectblock(8)
            Magn_Force3 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces3[i] = Magn_Force3

        if blo.b4 == 1:
            femm.mo_groupselectblock(9)
            Magn_Force4 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces4[i] = Magn_Force4

        if blo.b5 == 1:
            femm.mo_groupselectblock(10)
            Magn_Force5 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces5[i] = Magn_Force5

        if blo.b6 == 1:
            femm.mo_groupselectblock(11)
            Magn_Force6 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces6[i] = Magn_Force6

        if blo.b7 == 1:
            femm.mo_groupselectblock(12)
            Magn_Force7 = femm.mo_blockintegral(19)
            femm.mo_clearblock()
            modelled.Magnet_Forces7[i] = Magn_Force7

        if blo.b1 == 1:
            femm.mo_groupselectblock(6)
        if blo.b2 == 1:
            femm.mo_groupselectblock(7)
        if blo.b3 == 1:
            femm.mo_groupselectblock(8)
        if blo.b4 == 1:
            femm.mo_groupselectblock(9)
        if blo.b5 == 1:
            femm.mo_groupselectblock(10)
        if blo.b6 == 1:
            femm.mo_groupselectblock(11)
        if blo.b7 == 1:
            femm.mo_groupselectblock(12)
        total = femm.mo_blockintegral(19)
        femm.mo_clearblock()
        modelled.tot_mag[i] = total

        # Translate inner coil to different distance
        femm.mi_selectgroup(3)
        femm.mi_movetranslate(0, StepSize)
        femm.mi_clearselected()
loop = Computation_loop()

print(modelled.InnCoil_Positions)
print(modelled.Magnet_Forces1)
print(modelled.Magnet_Forces2)
print(modelled.Magnet_Forces3)
print(modelled.Magnet_Forces4)
print(modelled.Magnet_Forces5)
print(modelled.Magnet_Forces6)
print(modelled.Magnet_Forces7)
print(modelled.Magnet_Forces_m)
print(modelled.Magnet_Forces_c)
print(modelled.tot_mag)
#print(modelled.Magnet_Forces3)
# print(modelled.block_forces)

if NSteps > 2:
    modelled.MetaData[0] = NSteps
    modelled.MetaData[1] = StepSize
    modelled.MetaData[2] = sensor.para()[2]
    np.savetxt(outputfile, (modelled.InnCoil_Positions, modelled.Magnet_Forces1,modelled.MetaData))

data_file = "f0bench_def_3"

class Results():
    def __init__(self):
        pass
    plt.style.use(['science', 'grid', 'notebook'])

    plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces_c), "o--", label="inn")
    #plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces_m), "o--", label="mag")
    plt.ylabel('Force [N]')
    plt.xlabel('Inner Coil Position [mm]')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if save == 1:
        plt.savefig("inn.png")
        shutil.move("inn.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\try")
    plt.show()

    if blo.b4 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces4), "o--", label="b4")
    if blo.b5 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces5), "o--", label="b5")
    if blo.b6 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces6), "o--", label="b6")
    if blo.b7 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces7), "o--", label="b7")
    plt.ylabel('Force [N]')
    plt.xlabel('Inner Coil Position [mm]')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if save == 1:
        plt.savefig("b4567.png")
        shutil.move("b4567.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\try")
    plt.show()

    if blo.b1 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces1), "o--", label="b1")
    if blo.b2 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces2), "o--", label="b2")
    if blo.b3 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces3), "o--", label="b3")
    if blo.b4 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces4), "o--", label="b4")
    if blo.b5 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces5), "o--", label="b5")
    if blo.b6 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces6), "o--", label="b6")
    if blo.b7 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces7), "o--", label="b7")
    plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.tot_mag), "o--", label="tot")
    plt.ylabel('Force [N]')
    plt.xlabel('Inner Coil Position [mm]')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if save == 1:
        plt.savefig("tot.png")
        shutil.move("tot.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\try")
    plt.show()

    plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces_c), "o--", label="inn")
    if blo.b1 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces1), "o--", label="b1")
    if blo.b2 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces2), "o--", label="b2")
    if blo.b3 == 1:
        plt.plot(np.array(modelled.InnCoil_Positions), np.array(modelled.Magnet_Forces3), "o--", label="b3")
    plt.ylabel('Force [N]')
    plt.xlabel('Inner Coil Position [mm]')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if save == 1:
        plt.savefig("b123.png")
        shutil.move("b123.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\try")
    plt.show()
results = Results()

class Save_data():
    def __init__(self):
        pass

    data = np.column_stack((modelled.InnCoil_Positions, modelled.Magnet_Forces_c, modelled.Magnet_Forces_m, modelled.Magnet_Forces1, modelled.Magnet_Forces2, modelled.Magnet_Forces3, modelled.Magnet_Forces4, modelled.Magnet_Forces5, modelled.Magnet_Forces6, modelled.Magnet_Forces7, modelled.tot_mag))
    np.savetxt(data_file, data)
saved_data = Save_data()