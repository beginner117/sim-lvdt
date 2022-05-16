import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import warnings


warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol/for, [2]-low_out_vol/for, [3]-inn_vol/mag_for, [4]-Norm_Out_Sig/for, [5]-fit_err(1) , [6]-norm-fit(1), [7]-Linear Range
inputdata = []
slopes = []

#output_files = [ "dis26", "defs", "dis30", "dis32"]
output_files = [ "defs"]
#legends = ["dist:26.5", "dist:28.5(def)", "dist:30.5", "dist:32.5" ]
legends = ["(default)" ]
voice_coil = 0
for i in range(0,len(output_files)):
    X = np.loadtxt(output_files[i], dtype=complex)
    inputarray = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    inputdata.append(inputarray)
n = len(output_files)

plt.style.use(['science', 'grid', 'notebook'])

class Graphs():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = r"C:\Users\kumar\OneDrive\Desktop\pi\bench"
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def uppout_vol(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][1]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Upper Out Coil Voltage [V] ')
        if voice_coil == 1:
            plt.ylabel('Upper Out Force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("upp_out.png")
            shutil.move("upp_out.png", self.path1)
        plt.show()
    def lowout_vol(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][2]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Lower Out Coil Voltage [V] ')
        if voice_coil == 1:
            plt.ylabel('Lower Out Coil Force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("low_out.png")
            shutil.move("low_out.png", self.path1)
        plt.show()
    def inncoil_vol(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][3]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Inner Out Coil Voltage [V]')
        if voice_coil == 1:
            plt.ylabel('Magnet Force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("Inn_vol.png")
            shutil.move("Inn_vol.png", self.path1)
        plt.show()
    def norm_sig(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Normalised Out Coil signal [V/A]')
        if voice_coil == 1:
            plt.ylabel('Normalised Magnet Force [N/A]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def norm_fit(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][6]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('Normalised Fit Error [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylim(0,0.1)
        plt.legend()
        if self.sav == 1:
            plt.savefig("normfiterr.png")
            shutil.move("normfiterr.png", self.path1)
        plt.show()

    def fit(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][5]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Fit Error [V/A]')
        if voice_coil == 1:
            plt.ylabel('Fit Error [N/A]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("fiterr.png")
            shutil.move("fiterr.png", self.path1)
        plt.show()
    def norm_fit_sig(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][7]).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Fit Norm. Out Coil signal [V/A]')
        if voice_coil == 1:
            plt.ylabel('Fit Norm. Out Coil Forces [N/A]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("fit_norm_sig.png")
            shutil.move("fit_norm_sig.png", self.path1)
        plt.show()
    def lin_imp(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), 100 - (np.array(inputdata[i][6])/np.array(inputdata[output_files.index("defs")][6]))*100, 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Linear Improvement [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylim(-100, 100)
        plt.legend()
        if self.sav == 1:
            plt.savefig("linfit.png")
            shutil.move("linfit.png", self.path1)
        plt.show()
    def slope(self):
        for i in range(0,n):
            m = np.polyfit(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 1)[0]
            slopes.append(m)
        #plt.plot(legends, slopes, 'o--')
        plt.plot(legends, ((np.array(slopes)/slopes[output_files.index("defs")])*100) - 100, "o--")
        if voice_coil == 0:
            plt.ylabel('slope increment [%]')
        if voice_coil == 1:
            plt.ylabel('slope')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def linear_range(self):
        if voice_coil == 1:
            for i in range(0, n):
                plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][7]).real.tolist(), 'o-',
                         label=legends[i])
            plt.ylabel('Fit Norm. Out Coil Forces [N/A]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            if self.sav == 1:
                plt.savefig("fit_norm_sig.png")
                shutil.move("fit_norm_sig.png", self.path1)
            plt.show()
