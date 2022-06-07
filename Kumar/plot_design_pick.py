import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import warnings
import pickle


warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol/for, [2]-low_out_vol/for, [3]-inn_vol/mag_for, [4]-Norm_Out_Sig/for, [5]-fit_err(1) , [6]-norm-fit(1), [7]-Linear Range
#yoke data : [0]-position, [1]-inncoil_force, [2]-mag_force, [3]-b1, [4]-b2, [5]-b3, [6]-b4, [7]-b5, [8]-b6, [9]-b7
inputdata = []
slopes = []

output_files = ["inht16", "def_bench", "inht20", "inht22" ]
legends = ["inn_ht=16", "inn_ht=18(def)", "inn_ht=20", "inn_ht=22"]
b123_legends = ["b1", "b2", "b3"]
b4567_legends = ["b4", "b5", "b6", "b7"]
voice_coil = 0
for i in range(0,len(output_files)):
    pickle_in = open("pick" + output_files[i], "rb")
    output_files[i] = pickle.load(pickle_in)
n = len(output_files)

inn1 = [2.62935675, 2.66902954, 2.67169041, 2.6682842,  2.65856084, 2.6280785,
 2.58718421, 2.52591351, 2.41799797, 2.27640943, 2.13471348]
mag1 = [-12.52180112, -12.41901964, -12.30531739, -12.18863861, -12.07444921,
 -11.97619313, -11.86011547, -11.74769664, -11.62095208, -11.55793709,
 -11.47895378]
pos1 = [-2, -1,  0,  1,  2,  3,  4,  5,  6,  7,  8]

print(len(output_files[0]))

plt.style.use(['science', 'grid', 'notebook'])

class Graphs():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small_IP\res"
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def uppout_vol(self):
        for i in range(0,n):
            uppout = []
            posi = []
            for j in range(0,len(output_files[0])):
                 uppout.append(output_files[i][j][1])
                 posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(uppout).real.tolist(), 'o-', label=legends[i])
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
            lowout = []
            posi = []
            for j in range(0, len(output_files[0])):
                lowout.append(output_files[i][j][2])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(lowout).real.tolist(), 'o-', label=legends[i])
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
            inncoil = []
            posi = []
            for j in range(0, len(output_files[0])):
                inncoil.append(output_files[i][j][3])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi)[0::2], np.array(inncoil)[0::2], 'o-', label=legends[i])
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
            normsig = []
            posi = []
            for j in range(0, len(output_files[0])):
                normsig.append(output_files[i][j][4])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi), np.array(normsig), 'o-', label=legends[i])

        if voice_coil == 0:
            plt.ylabel('Normalised Out Coil signal [V/A]')
        if voice_coil == 1:
            plt.ylabel('Normalised Magnet Force [N/A]')
        plt.xlabel('Inner Coil Position [mm]')

        plt.legend()
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def norm_fit(self):
        for i in range(0,n):
            normfit = []
            posi = []
            for j in range(0, len(output_files[0])):
                normfit.append(output_files[i][j][6])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(normfit).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('Normalised Fit Error [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylim(0,0.8)
        plt.legend()
        if self.sav == 1:
            plt.savefig("normfiterr.png")
            shutil.move("normfiterr.png", self.path1)
        plt.show()

    def fit(self):
        for i in range(0,n):
            fit = []
            posi = []
            for j in range(0, len(output_files[0])):
                fit.append(output_files[i][j][5])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(fit).real.tolist(), 'o-', label=legends[i])
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
            normfitsig = []
            posi = []
            for j in range(0, len(output_files[0])):
                normfitsig.append(output_files[i][j][7])
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(normfitsig).real.tolist(), 'o-', label=legends[i])
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
            linimp = []
            posi = []
            for j in range(0, len(output_files[0])):
                p = 100 - ((np.array(output_files[i][j][6]/np.array(output_files[output_files.index("def_bench")][j][6])))*100)
                linimp.append(p)
                posi.append(output_files[i][j][0])
            plt.plot(np.array(posi).real.tolist(), np.array(linimp).real.tolist(), 'o-', label=legends[i])
        if voice_coil == 0:
            plt.ylabel('Linear Improvement [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.ylim(-33, 33)
        plt.legend()
        if self.sav == 1:
            plt.savefig("linfit.png")
            shutil.move("linfit.png", self.path1)
        plt.show()
    def slope(self):
        for i in range(0,n):
            normsig = []
            posi = []
            for j in range(0, len(output_files[0])):
                normsig.append(output_files[i][j][4])
                posi.append(output_files[i][j][0])
            m = np.polyfit(np.array(posi), np.array(normsig), 1)[0]
            slopes.append(m)
        #plt.plot(legends, slopes, 'o--')
        plt.plot(legends, ((np.array(slopes)/slopes[output_files.index("def_bench")])*100) - 100, "o--")
        if voice_coil == 0:
            plt.ylabel('slope increment [%]')
        if voice_coil == 1:
            plt.ylabel('slope increment [%]')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("norm_sig.png")
            shutil.move("norm_sig.png", self.path1)
        plt.show()
    def linear_range(self):
        if voice_coil == 1:
            for i in range(0, n):
                linran = []
                posi = []
                for j in range(0, len(output_files[0])):
                    linran.append(output_files[i][j][7])
                    posi.append(output_files[i][j][0])
                plt.plot(np.array(posi), np.array(linran), 'o-', label=legends[i])
            plt.ylabel('Fit Norm. Out Coil Forces [%]')
            plt.xlabel('Inner Coil Position [mm]')
            plt.legend()
            #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            if self.sav == 1:
                plt.savefig("fit_norm_sig.png")
                shutil.move("fit_norm_sig.png", self.path1)
            plt.show()

class Yoke_graphs():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = r"C:\Users\kumar\OneDrive\Desktop\pi\bench"
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def low_inn(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][1]).real.tolist(), 'o-', label=legends[i])
        plt.plot(np.array(pos1), np.array(inn1), 'o-', label = "gap=1.35(2,7)")
        plt.ylabel('Lower Inn coil force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Lower Inner Coil Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("low_inn.png")
            shutil.move("low_inn.png", self.path1)
        plt.show()
    def mag(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][2]).real.tolist(), 'o-', label=legends[i])
        plt.plot(np.array(pos1), np.array(mag1), 'o-', label="gap=1.35(2,7)")
        plt.ylabel('Magnet force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Magnet Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("mag.png")
            shutil.move("mag.png", self.path1)
        plt.show()
    def b1(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][3]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block1 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b1.png")
            shutil.move("b1.png", self.path1)
        plt.show()
    def b2(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block2 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b2.png")
            shutil.move("b2.png", self.path1)
        plt.show()
    def b3(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][5]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block3 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b3.png")
            shutil.move("b3.png", self.path1)
        plt.show()
    def b4(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][6]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block4 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b4.png")
            shutil.move("b4.png", self.path1)
        plt.show()
    def b5(self):
        for i in range(0, n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][7]).real.tolist(), 'o-',
                     label=legends[i])
        plt.ylabel('block5 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b5.png")
            shutil.move("b5.png", self.path1)
        plt.show()
    def b6(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][8]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block6 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b6.png")
            shutil.move("b6.png", self.path1)
        plt.show()
    def b7(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][9]).real.tolist(), 'o-', label=legends[i])
        plt.ylabel('block7 force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b7.png")
            shutil.move("b7.png", self.path1)
        plt.show()
    def b_total(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]), (np.array(inputdata[i][3])+np.array(inputdata[i][4])+np.array(inputdata[i][5])+np.array(inputdata[i][6])+np.array(inputdata[i][7])+np.array(inputdata[i][8])+np.array(inputdata[i][9])), 'o-', label=legends[i])
        plt.plot(np.array(pos1), -np.array(mag1)-np.array(inn1), 'o-', label="gap=1.35(2,7)")
        plt.ylabel('total block force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Total Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b_tot.png")
            shutil.move("b_tot.png", self.path1)
        plt.show()

'''
class Single_sim():
    def __init__(self, num, save, directory=None):
        self.sav = save
        self.directory = directory
        self.file = num
        if self.directory and self.sav == 1:
                parent_dir = ""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def b123(self):
        for i in (0, len(b123_legends)):
            plt.plot(np.array(inputdata[self.file][0]).real.tolist(), np.array(inputdata[self.file][i+3]).real.tolist(), 'o-',
                     label=b123_legends[i])
        plt.ylabel('block forces [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b123.png")
            shutil.move("b123.png", self.path1)
        plt.show()
    def b4567(self):
        for i in (0, len(b4567_legends)):
            plt.plot(np.array(inputdata[self.file][0]).real.tolist(), np.array(inputdata[self.file][i+6]).real.tolist(), 'o-',
                     label=b4567_legends[i])
        plt.ylabel('block forces [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b4567.png")
            shutil.move("b4567.png", self.path1)
        plt.show()
'''


