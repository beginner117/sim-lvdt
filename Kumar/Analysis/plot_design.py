import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import shutil
import warnings
warnings.filterwarnings('ignore')

slopes = []
files = []
res = []
ind = []
rea_err = []
rea_mean = []
ind_err = []
ind_mean = []
imp_err = []
imp_mean = []

a1 = ['inn30_out30','inn30_out31','inn30_out32','inn30_out34',
    'inn31_out30','inn31_out31','inn31_out32','inn31_out34']
a2 = ['inn32_out30','inn32_out31','inn32_out32','inn32_out34',
    'inn34_out30','inn34_out31','inn34_out32','inn34_out34']
output_files=["C:/Users/kumar/PycharmProjects/lvdtsimulations/Kumar/Analysis/typeB/mix_wire/{}.npz".format(i)
              for i in a2]

legends =  ['1.25\n(32_30)','1.112\n(32_31)','1\n(32_32)','0.788\n(32_34)',
    '1.585\n(34_30)','1.414\n(34_31)','1.268\n(34_32)','1\n(34_34)'] #b2
# legends =  ['1\n(30_30)','0.890\n(30_31)','0.8\n(30_32)','0.63\n(30_34)',
#     '1.12\n(31_30)','1\n(31_31)','0.898\n(31_32)','0.708\n(31_34)'] #b1
ind = np.array([8.1, 8.7, 9.3, 9.6, 9.9, 10.6, 11.3])  #a1
turns = []  #a1

imp = np.array([510.2, 547.7, 587.3, 606.4, 627.9, 669.9, 713.4])  #type F
#imp = np.array()
dcr = [25.62*2]
# correction =[1.1319839174340767, 1.1709069817548114, 1.2145003094076183, 1.3510842829538579,  #a1
#              1.1320069232065757, 1.170942460760361, 1.2146522865034355, 1.3511269163325477]
# correction = [1.1320088557766808, 1.1709021633862942, 1.214675238070608, 1.3511251602241567, #a2
#               1.132048602290738, 1.170926928116232, 1.2147308881064387, 1.3510785383299613]

# correction = [1.0940403750973609, 1.1222100346902188, 1.1525487564160242, 1.2457952269743158, #b1
#               1.0940649207480795, 1.12216331949018, 1.1526811009761644, 1.2458134067030815]

correction = [1.0940663144488774, 1.1221680912744298, 1.152529369624771, 1.2458226085640776, #b2
              1.0940526002880402, 1.1221735251611102, 1.1525277456055116, 1.2457838462211068]
for i in range(0,len(output_files)):
    b = np.load(output_files[i], allow_pickle=True)

    #print(b['Input_config'])
    files.append(b)
n = len(output_files)
gain = 70.02
class Lvdt():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def vol(self, par):
        for i in range(0,n):
            upp_out = np.array(files[i]["UOC_voltages"])
            low_out = np.array(files[i]["LOC_voltages"])
            inner = np.array(files[i]["IC_voltages"])
            if par == 'inner':
                plt.plot(np.array(files[i]["IC_positions"]), abs(inner), 'o-', label=legends[i])
            if par == 'upp_out':
                plt.plot(np.array(files[i]["IC_positions"]), abs(upp_out), 'o-', label=legends[i])
            if par == 'low_out':
                plt.plot(np.array(files[i]["IC_positions"]), abs(low_out), 'o-', label=legends[i])
        plt.ylabel('{} Coil Voltage [V] '.format(par))
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("upp_out.png")
            shutil.move("upp_out.png", self.path1)
        plt.show()
    def norm_sig(self):
        for i in range(0,n):
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            #norm_sig = out_sig / abs(np.array(files[i]["IC_currents"]))
            plt.plot(np.array(files[i]["IC_positions"]), abs(norm_sig)*gain, 'o-', label=legends[i])
        plt.legend()
        plt.grid()
        plt.ylabel('Normalised Out Coil signal [V/v]')
        plt.xlabel('Inner Coil Position [mm]')
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def norm_fit(self, par:str):
        out_dia = np.zeros(n)
        inn_dia = np.zeros(n)
        for i in range(0,n):
            inn_pos = np.array(files[i]["IC_positions"])
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            norm_sig_c = out_sig / abs(np.array(files[i]["IC_currents"]))
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig*gain*correction[i], 1)
            m_fem_c, co_fem_c = np.polyfit(inn_pos, norm_sig_c, 1)
            sim_fit = (m_fem * np.array(inn_pos))+ (co_fem)
            sim_fit_c = (abs(m_fem_c) * np.array(inn_pos))+ (co_fem_c)
            relerr_fem = (abs(sim_fit - norm_sig*gain*correction[i]) / abs(norm_sig*gain*correction[i])) * (100)
            relerr_fem_c = ((abs(sim_fit_c - (norm_sig_c))) / abs(norm_sig_c)) * (100)
            fiterr_fem = (sim_fit - norm_sig)
            g1 = files[i]['Input_parameters'].item()
            out_dia[i] = g1['outercoil Diameter_Insulation_Wiretype'][0]
            inn_dia[i] = g1['innercoil Diameter_Insulation_Wiretype'][0]
            if par == 'signal':
                plt.plot(inn_pos, sim_fit, 'o-', label=legends[i])
            if par == 'rel_error' :
                plt.plot(inn_pos, abs(relerr_fem), 'o-', label=legends[i])
            if par == 'error' :
                plt.plot(inn_pos, abs(sim_fit - norm_sig), 'o-', label=legends[i])
            if par == 'slope':
                print("femm signal slope, constant :", abs(m_fem), co_fem)
                print("femm signal with current slope, constant :", abs(m_fem_c), co_fem_c)
                slopes.append(m_fem)
        if par == 'signal' :
            plt.ylabel('LVDT response  [V/v]')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'rel_error':
            plt.ylim(0, 1.5)
            plt.ylabel('Relative error [%]')  #[$\dfrac{abs(fit error)}{actual}$]
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'error':
            plt.ylabel('Error (fit-actual)')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'slope':
            dia_ratio = np.round(out_dia/inn_dia, decimals = 4)
            print(dia_ratio)
            #plt.plot(legends, (-slopes[3]+np.array(slopes))*100/slopes[3], "o--")
            plt.plot(legends, slopes, "o--", label = 'simulation')
            #plt.plot(legends, (-ind[3] + ind) * 100 / ind[3], "o--")
            plt.ylabel('normalised response slope [V/mmV]')
            plt.xlabel('wire size ratio [$\dfrac{outer}{inner}$], inn coil wire_out coil wire')
            plt.xticks(rotation=15)
        #plt.ylim(0,0.1)
        plt.legend()
        if self.sav == 1:
            plt.savefig("normfiterr.png")
            shutil.move("normfiterr.png", self.path1)
        plt.grid()
        #plt.legend(title='size ratio\n[$\dfrac{outer}{inner}$]', loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('type:B, Sensitivity, gain:70.02\n(20mA excitation, sim range:5mm,0.25mm step, full fit)')
        plt.tight_layout()
        plt.show()
    def resitance(self, par:str):
        inductance = np.zeros(n)
        impedance = np.zeros(n)
        for i in range(0,n):
            indu = np.array(files[i]["IC_flux"])/np.array(files[i]["IC_currents"])
            inductance[i] = abs(sum(indu*1000)/len(indu))
            resi = np.array(files[i]["IC_voltages"])/np.array(files[i]["IC_currents"])
            impedance[i] = abs(sum(resi) / len(resi))
        print(abs(impedance))
        if par == "inductance" :
            plt.plot(legends, inductance, "o-")
            plt.ylabel("Flux/current [mH]")
        else :
            plt.plot(legends, impedance, "o-")
            plt.ylabel('Inner coil impedance [Ω]')
        if self.sav == 1:
            plt.savefig("inn_ind.png")
            shutil.move("inn_ind.png", self.path1)
        plt.xlabel("Inn coil position")
        plt.grid()
        plt.show()
    def lin_imp(self):
        for i in range(0,n):
            gain = 65
            inn_pos = np.array(files[i]["IC_positions"])
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig*gain, 1)
            print("femm signal slope :", m_fem, co_fem)
            slopes.append(m_fem)
            sim_fit = m_fem * np.array(inn_pos) + co_fem
            relerr_fem = ((abs(sim_fit - norm_sig)) / abs(norm_sig)) * 100
        ref_slope = []
        plt.plot(legends, (slopes-slopes[3])*100/slopes[3], "o--")
        #plt.xlabel('Inner Coil Position [mm]')
        plt.ylabel('slope improvement [%]')
        plt.xlabel('type of coil')
        #plt.ylim(-33, 33)
        plt.legend()
        if self.sav == 1:
            plt.savefig("linfit.png")
            shutil.move("linfit.png", self.path1)
        plt.show()
    def power(self):
        for i in range(0,n):
            power = files[i]['IC_currents']*files[i]['IC_voltages']
            plt.plot(np.array(files[i]["IC_positions"]), power, "o--", label = legends[i])
        plt.ylabel('Inner coil Power [W]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()

class VC:
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def force(self, para=None):
        for i in range(0,n):
            inn_pos = np.array(files[i]["UOC_positions"])
            mag_force = (np.array(files[i]["Mag_forces"]))
            coil_force = (np.array(files[i]["UOC_forces"]))
            currents = np.array(files[i]["UOC_currents"])
            if para == 'coil_norm':
                plt.plot(inn_pos, (coil_force)/currents, 'o-', label = legends[i])

                plt.ylabel('Normalised Coil Force [N/A]')
                plt.title('Outer Coil Forces \n [Type : I with type_A magnet, RS-wire, 1 layer]')
                #plt.ylim(-0.75, 0.75)
            if para == 'mag_norm':
                plt.plot(inn_pos, abs(mag_force)/currents, 'o-', label = legends[i])
                print(abs(mag_force))
                plt.ylabel('Normalised Magnet Force [N/A]')
                plt.title(' Magnet Forces  \n [Type : I with type_A magnet, RS-wire, 1 layer]')
            if para == 'mag':
                plt.plot(inn_pos, mag_force, 'o-', label = legends[i])
                plt.ylabel('Magnet Force [N]')
                plt.title('Magnet Forces \n [Type : I with type_A magnet, 32 AWG-wire, 1 layer]')
            if para == 'coil':
                plt.plot(inn_pos, coil_force, 'o-', label = legends[i])
                plt.ylabel('Coil Force [N]')
                plt.title('Sum of Outer Coil Forces \n [Type : A, 32 AWG-wire]')
            if para == 'diff':
                plt.plot(inn_pos, abs(abs(mag_force)-abs(coil_force))/currents, 'o-', label = legends[i])
                plt.ylabel('absolute force difference (magnet force-coil force) [N/A]')
                #plt.ylim(-0.05, 0.2)
                plt.title('Forces difference [Type : I with type A magnet,] \n RS-wire')
        plt.xlabel('Coil Position relative to magnet [mm]')
        plt.legend(title = 'Magnet\nCoercivity [A/m]')
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.grid()
        plt.show()
    def force_fit(self, para=None):
        forc = []
        for i in range(0, n):
            inn_pos = np.array(files[i]["IC_positions"])
            #inn_pos = np.array(files[i]["UOC_positions"])
            mag_force = (np.array(files[i]["Mag_forces"]))
            coil_force1 = (np.array(files[i]["UOC_forces"]))
            coil_force2 = (np.array(files[i]["LOC_forces"]))

            coil_force = coil_force1+coil_force2
            currents = np.array(files[i]["UOC_currents"])
            p1 = 1; p2 = 101
            a1, a2, a3 = np.polyfit(inn_pos, abs(coil_force),2)
            fit_for = (a1*(inn_pos**2))+(a2*inn_pos)+a3
            b1, b2, b3 = np.polyfit(inn_pos, abs(mag_force), 2)
            fit_for_mag = (b1 * (inn_pos ** 2)) + (b2 * inn_pos) + b3
            if para == 'mag_norm':
                plt.plot(inn_pos, fit_for_mag/currents, 'o-', label = legends[i])
                plt.ylabel(' Magnet Force (absolute) [N/A]')
                plt.title('Type : A, Magnet Forces (full fit) \n [inner coil - 31AWG(6 layers), outer coil - 32AWG(7 layers)]')
            if para == 'coil_norm':
                plt.plot(inn_pos, fit_for/currents, 'o-', label = legends[i])
                plt.ylabel(' Fitted normalised coil Force (absolute) [N/A]')
                plt.title('Outer Coil Forces \n [Type : I with type A magnet, 1 layer, RS-wire, full fit]')
                #plt.title('Outer Coil Forces \n [Type : A, full fit, wire - 32 AWG]')
            if para == 'diff':
                plt.plot(inn_pos, (mag_force+coil_force)/currents, 'o-', label = legends[i])
                plt.ylabel('norm force difference (magnet force+coil force) [N/A]')
                plt.title('Force difference \n [Type : A, full fit, wire - 32 AWG]')
            if para == 'error':
                plt.plot(inn_pos[p1:p2], abs(fit_for[p1:p2]-coil_force[p1:p2])/currents[p1:p2], 'o-', label = legends[i])
                plt.ylabel('Fit Force error [N/A]')
                plt.title('Fit error \n [Type : I with type A magnet, 1 layer, RS-wire, full fit]')
            if para == 'rel_error':
                plt.plot(inn_pos[p1:p2], (abs(fit_for[p1:p2]-coil_force[p1:p2])/abs(coil_force[p1:p2]))*100, 'o-', label = legends[i])
                plt.ylim(0, 1000)
                plt.ylabel('relative fit Force error [%]')
                plt.title('Relative error \n [Type : I with type A magnet, 1 layer, RS-wire, full fit]')
        plt.xlabel('Coil Position relative to magnet [mm]')
        #plt.legend(title = 'Outer coil \nexcitations')
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.grid()
        plt.show()
        print(forc)
    def linearity(self, par:list):

        for j in range(len(par)):
            force = []
            for i in range(0,n):
                currents = np.array(files[i]["UOC_currents"])
                mag_force = abs(np.array(files[i]["Mag_forces"]))
                force.append(mag_force[par[j]])
            plt.plot(legends, force, 'o--', label = par[j]-40)
        #plt.xticks(rotation = 15)
        plt.xlabel('outer coil current')
        plt.ylabel('Force [N]')
        plt.title('force at various positions ')
        plt.legend(title = 'position(mm)')
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.grid()
        plt.show()
    def stability(self):
        for i in range(0,n):
            #coil_force1 = (np.array(files[i]["UOC_forces"]))
            #coil_force2 = (np.array(files[i]["LOC_forces"]))
            #coil_force2 = np.zeros(len(files[i]["UOC_positions"]))
            #coil_force = coil_force1 + coil_force2
            inn_pos = np.array(files[i]["IC_positions"])
            renormalised_forces = (abs(np.array(files[i]["Mag_forces"]))/max(abs(np.array(files[i]["Mag_forces"]))))*100
            #renormalised_forces = (abs(coil_force) / max(abs(coil_force))) * 100
            a1, a2, a3 = np.polyfit(inn_pos, renormalised_forces, 2)
            fit_renormalised_forces = (a1*(inn_pos**2))+(a2*(inn_pos))+a3
            plt.plot(inn_pos, fit_renormalised_forces, "o--", label = legends[i])
        plt.ylabel('Force stability fit (Coil force/Maximum coil force)*100 [%]')
        plt.xlabel('Inner Coil Position [mm]')
        #plt.legend(title='Outer coil \nexcitations')
        plt.grid()
        plt.title('Stability \n [Type : A, full fit, wire - 32 AWG]')
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
    def power(self):
        po = []
        for i in range(0,n):
            power = (files[i]['LOC_currents']*files[i]['LOC_voltages'])/1000000
            po.append(max(power))
            plt.plot(np.array(files[i]["IC_positions"]), power, "o--", label = legends[i])
        plt.ylabel('Lower out coil Power [W]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
        print(po)




