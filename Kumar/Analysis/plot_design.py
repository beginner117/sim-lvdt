import numpy as np
import matplotlib.pyplot as plt
import sys
#sys.path.insert(1, "C://Users//kumar//PycharmProjects//lvdtsimulations//Kumar//Analysis")
import os
import shutil
import warnings
warnings.filterwarnings('ignore')

# output_file data : [0]-Inncoil position, [1]-Inncoil vol [2]-Uppout vol [3]-lowout vol [4]-Inn coil curr [5]-uppout cur [6]-Lowout cu [7]-Inncoil flux

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

#output_files = ['tr_12.npz', 'tr_25.npz', 'tr_37.npz', 'tr4_50.npz', 'tr_62.npz']
output_files = ['tr_6m.npz', 'tr_12m.npz', 'tr_20m.npz', 'tr_50m.npz', 'tr_80m.npz', 'tr_100m.npz', 'tr_300m.npz', 'tr_700m.npz', 'tr_1000m.npz']
#legends = ["12.25mA", "25mA", "37.25mA", "50mA", "62.25mA"]
legends = ["6mA", "12mA", "20mA", "50mA", "80mA", "0.1A", "0.3A", "0.7A", "1A"]
for i in range(0,len(output_files)):
    b = np.load(output_files[i])
    files.append(b)
n = len(output_files)

class Lvdt():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def uppout_vol(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["UOC_voltages"])), 'o-', label=legends[i])
        plt.ylabel('Upper Out Coil Voltage [V] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("upp_out.png")
            shutil.move("upp_out.png", self.path1)
        plt.show()
    def lowout_vol(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["LOC_voltages"])), 'o-', label=legends[i])
        plt.ylabel('Lower Out Coil Voltage [V] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("low_out.png")
            shutil.move("low_out.png", self.path1)
        plt.show()
    def inncoil_vol(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["IC_voltages"])), 'o-', label=legends[i])
        plt.ylabel('Inner Out Coil Voltage [V]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
    def norm_sig(self):
        for i in range(0,n):
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            #norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_currents"]))
            plt.plot(np.array(files[i]["IC_positions"]), norm_sig, 'o-', label=legends[i])
        plt.ylabel('Normalised Out Coil signal [V/A]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def norm_fit(self, par:str):
        for i in range(0,n):
            inn_pos = np.array(files[i]["IC_positions"])
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / files[i]["IC_voltages"]
            #norm_sig = out_sig / abs(np.array(files[i]["IC_currents"]))
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig*69, 1)
            sim_fit = abs(m_fem) * np.array(inn_pos) + abs(co_fem)
            relerr_fem = ((abs(sim_fit - norm_sig)) / abs(norm_sig)) * 100
            fiterr_fem = (sim_fit - (norm_sig))
            if par == 'signal':
                plt.plot(inn_pos, sim_fit, 'o-', label=legends[i], color = "blue")
            if par == 'error' :
                plt.plot(inn_pos, relerr_fem, 'o-', label=legends[i])
            if par == 'slope':
                print("femm signal slope, constant :", abs(m_fem), co_fem)
                slopes.append(m_fem)
        if par == 'signal' :
            plt.ylabel('LVDT response  [V/v]')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'error':
            plt.ylim(0, 1.5)
            plt.ylabel('Relative error [$\dfrac{abs(fit error)}{actual}$] [%]')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'slope':
            plt.plot(legends, slopes, "o--")
            plt.ylabel('Slope[V/mmv]')
            plt.xlabel('types')
        #plt.ylim(0,0.1)
        plt.legend()
        if self.sav == 1:
            plt.savefig("normfiterr.png")
            shutil.move("normfiterr.png", self.path1)
        plt.show()
    def resitance(self, par:str):
        for i in range(0,n):
            indu = np.array(files[i]["IC_flux"])/np.array(files[i]["IC_currents"])
            induct = sum(indu*1000)/len(indu)
            resi = np.array(files[i]["IC_voltages"])/np.array(files[i]["IC_currents"])
            r = sum(resi) / len(resi)
            ind.append(induct)
            res.append(r)
        print(ind, res)
        if par == "inductance" :
            plt.plot(legends, np.array(ind), "o-")
            plt.ylabel("Flux/current [mH]")
        else :
            plt.plot(legends, np.array(res), "o-")
            plt.ylabel('Inner coil resistance [ohms]')
        plt.xlabel("Inn coil position")
        plt.show()
        if self.sav == 1:
            plt.savefig("inn_ind.png")
            shutil.move("inn_ind.png", self.path1)
    def lin_imp(self):
        for i in range(0,n):
            inn_pos = np.array(files[i]["IC_positions"])
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig, 1)
            print("femm signal slope :", m_fem, co_fem)
            slopes.append(m_fem)
            sim_fit = m_fem * np.array(inn_pos) + co_fem
            relerr_fem = ((abs(sim_fit - norm_sig)) / abs(norm_sig)) * 100
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylim(-33, 33)
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

class VC():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def uppout_for(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["UOC_forces"])), 'o-', label=legends[i])
        plt.ylabel('Upper Out Coil Force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("upp_out.png")
            shutil.move("upp_out.png", self.path1)
        plt.show()
    def lowout_for(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["LOC_forces"])), 'o-', label=legends[i])
        plt.ylabel('Lower Out Coil Force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("low_out.png")
            shutil.move("low_out.png", self.path1)
        plt.show()
    def mag_for(self):
        for i in range(0,n):
            plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["Mag_forces"])), 'o-', label=legends[i])
        plt.ylabel('Magnet Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
    def force_fit(self, para:None):
        for i in range(0, n):
            inn_pos = np.array(files[i]["IC_positions"])
            a1, a2, a3 = np.polyfit(inn_pos, abs(np.array(files[i]["Mag_forces"])),2)
            fit_for = (a1*(inn_pos**2))+(a2*(inn_pos))+a3
            if para:
                plt.plot(np.array(files[i]["IC_positions"]), fit_for/np.array(files[i]["UOC_currents"]), 'o-', label=legends[i])
                plt.ylabel('Normalised Fitted Magnet Force [N/A]')
            else:
                plt.plot(np.array(files[i]["IC_positions"]), fit_for, 'o-', label=legends[i])
                plt.ylabel('Fitted Magnet Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.grid()
        plt.show()
    def stability(self):
        for i in range(0,n):
            inn_pos = np.array(files[i]["IC_positions"])
            renormalised_forces = (abs(np.array(files[i]["Mag_forces"]))/max(abs(np.array(files[i]["Mag_forces"]))))*100
            a1, a2, a3 = np.polyfit(np.array(files[i]["IC_positions"]), renormalised_forces, 2)
            fit_renormalised_forces = (a1*(inn_pos**2))+(a2*(inn_pos))+a3
            plt.plot(np.array(files[i]["IC_positions"]), fit_renormalised_forces, "o--", label = legends[i])
        plt.ylabel('Fitted Normalised Forces [$\dfrac{Magnet force}{Maximum force}$*100] [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
    def power(self):
        for i in range(0,n):
            power = files[i]['UOC_currents']*files[i]['UOC_voltages']
            plt.plot(np.array(files[i]["IC_positions"]), power, "o--", label = legends[i])
        plt.ylabel('Power [W]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()



