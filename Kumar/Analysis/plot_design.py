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

output_files = ["C:/Users/kumar/PycharmProjects/lvdtsimulations/Kumar/modules/tr1.npz", "C:/Users/kumar/PycharmProjects/lvdtsimulations/Kumar/modules/tr2.npz"]
legends = ['1', '2']
# output_files = ["C:/Users/kumar/PycharmProjects/lvdtsimulations/Kumar/Analysis/typeA_vc/typeA_{}mA_10offset.npz".format(i) for i in ['2p5', 5, '7p5', 10]]
# legends = ['{}mA'.format(i) for i in ['2.5', 5, '7.5', 10]]
for i in range(0,len(output_files)):
    b = np.load(output_files[i], allow_pickle=True)

    print(b['Input_config'])
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
            plt.plot(np.array(files[i]["IC_positions"]), abs(norm_sig)*65, 'o-', label=legends[i])
        plt.legend()
        plt.grid()
        plt.ylabel('Normalised Out Coil signal [V/v]')
        plt.xlabel('Inner Coil Position [mm]')
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def norm_fit(self, par:str):
        for i in range(0,n):
            inn_pos = np.array(files[i]["IC_positions"])
            out_sig = abs(np.array(files[i]["UOC_voltages"])) - abs(np.array(files[i]["LOC_voltages"]))
            norm_sig = out_sig / abs(np.array(files[i]["IC_voltages"]))
            norm_sig_c = out_sig / abs(np.array(files[i]["IC_currents"]))
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig*65, 1)
            m_fem_c, co_fem_c = np.polyfit(inn_pos, norm_sig_c, 1)
            sim_fit = (abs(m_fem) * np.array(inn_pos))+ abs(co_fem)
            relerr_fem = ((abs(sim_fit - (norm_sig*69))) / abs(norm_sig)) * (100/69)
            fiterr_fem = (sim_fit - (norm_sig))
            if par == 'signal':
                plt.plot(inn_pos, sim_fit, 'o-', label=legends[i], color = "blue")
            if par == 'error' :
                plt.plot(inn_pos, relerr_fem, 'o-', label=legends[i])
            if par == 'slope':
                print("femm signal slope, constant :", abs(m_fem), co_fem)
                print("femm signal with current slope, constant :", abs(m_fem_c), co_fem_c)
                slopes.append(m_fem)
        if par == 'signal' :
            plt.ylabel('LVDT response  [V/v]')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'error':
            #plt.ylim(0, 1)
            plt.ylabel('Relative error [$\dfrac{abs(fit error)}{actual}$] [%]')
            plt.xlabel('Inner Coil Position [mm]')
        if par == 'slope':
            plt.plot(legends, slopes, "o--")
            plt.ylabel('Slope[V/mmv]')
            plt.xlabel('types')
        #plt.ylim(0,0.1)
        #plt.legend()
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

class VC:
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def coil_force(self, par):
        for i in range(0,n):
            if par == 'upp_out':
                plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["UOC_forces"])), 'o-', label=legends[i])
            if par == 'low_out':
                plt.plot(np.array(files[i]["IC_positions"]), abs(np.array(files[i]["LOC_forces"])), 'o-', label=legends[i])
        plt.ylabel('{} Coil Force [N] '.format(par))
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("upp_out.png")
            shutil.move("upp_out.png", self.path1)
        plt.show()
    def mag_for(self, para=None):
        for i in range(0,n):
            inn_pos = np.array(files[i]["UOC_positions"])
            mag_force = abs(np.array(files[i]["Mag_forces"]))
            #mag_force = abs(np.array(files[i]["UOC_forces"]))
            currents = np.array(files[i]["UOC_currents"])
            if para == 'norm':
                plt.plot(inn_pos, mag_force/currents, 'o-', label = legends[i])
                plt.ylabel('Normalised Magnet Force [N/A]')
                #plt.ylim(-0.75, 0.75)
            else:
                plt.plot(np.array(inn_pos), abs(np.array(files[i]["Mag_forces"])), 'o-', label=legends[i])
                plt.ylabel('Magnet Force [N]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.title('VC Forces [Type : A]')
        plt.grid()
        plt.show()
    def force_fit(self, para=None):
        forc = []
        for i in range(0, n):
            #inn_pos = np.array(files[i]["IC_positions"])
            inn_pos = np.array(files[i]["UOC_positions"])
            mag_force = abs(np.array(files[i]["Mag_forces"]))
            #mag_force = abs(np.array(files[i]["UOC_forces"]))
            currents = np.array(files[i]["UOC_currents"])
            p1 = 1; p2 = 101
            a1, a2, a3 = np.polyfit(inn_pos[p1:p2], abs(mag_force[p1:p2])/1,2)
            fit_for = (a1*(inn_pos**2))+(a2*inn_pos)+a3
            if para == 'norm':
                plt.plot(inn_pos, fit_for/currents, 'o-', label = legends[i])
                plt.ylabel(' Fitted normalised Magnet Force [N/A]')
            if para == 'error':
                plt.plot(inn_pos[p1:p2], abs(fit_for[p1:p2]-mag_force[p1:p2])/currents[p1:p2], 'o-', label = legends[i])
                plt.ylabel('Fit Force error [N/A]')
            if para == 'rel_error':
                plt.plot(inn_pos[p1:p2], (abs(fit_for[p1:p2]-mag_force[p1:p2])/mag_force[p1:p2])*100, 'o-', label = legends[i])
                plt.ylim(0, 200)
                plt.ylabel('relative fit Force error [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        plt.title('VC Forces [Type : A]')
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
            inn_pos = np.array(files[i]["IC_positions"])
            renormalised_forces = (abs(np.array(files[i]["Mag_forces"]))/max(abs(np.array(files[i]["Mag_forces"]))))*100
            a1, a2, a3 = np.polyfit(inn_pos, renormalised_forces, 2)
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




