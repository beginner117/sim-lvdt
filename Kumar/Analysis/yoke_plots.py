import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import warnings
warnings.filterwarnings('ignore')

#yoke data : [0]-position, [1]-inncoil_force, [2]-mag_force, [3]-b1, [4]-b2, [5]-b3, [6]-b4, [7]-b5, [8]-b6, [9]-b7, [10]-total
#errorbar = [0]-correction factor, [1]-reference res, [2]-coil DC res, [3]-freq, [4]-input_vol, [5]-output_vol, [6]-ratio, [7]-reactance, [8]-inductance, [9]-impedance

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
v_in_mean = []
v_in_err = []
v_out_mean = []
v_out_err = []

output_files = ["def_typeA_lv.npz"]
legends = ["trial"]
for i in range(0,len(output_files)):
    b = np.load(output_files[i])
    files.append(b)
n = len(output_files)
f = 11




'''
class Yoke_graphs():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = r""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)
    def low_inn(self):
        for i in range(0,n):
            plt.plot(np.array(inputdata[i][0]).real.tolist()[:6], np.array(inputdata[i][1]).real.tolist()[:6], 'o-', label=legends[i])
        #plt.plot(np.array(pos1), np.array(inn1), 'o-', label = "gap=1.35(2,7)")
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
            plt.plot(np.array(inputdata[i][0]).real.tolist()[:6], np.array(inputdata[i][2]).real.tolist()[:6], 'o-', label=legends[i])
        #plt.plot(np.array(pos1), np.array(mag1), 'o-', label="gap=1.35(2,7)")
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
            force_sum = (inputdata[i][3])+np.array(inputdata[i][4])+np.array(inputdata[i][5])+np.array(inputdata[i][6])+np.array(inputdata[i][7])+np.array(inputdata[i][8])+np.array(inputdata[i][9])
            plt.plot(np.array(inputdata[i][0])[:6], np.array(force_sum)[:6], 'o-', label=legends[i])
        #plt.plot(np.array(pos1), -np.array(mag1)-np.array(inn1), 'o-', label="gap=1.35(2,7)")
        plt.ylabel('total block force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Total Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b_tot.png")
            shutil.move("b_tot.png", self.path1)
        plt.show()
    def tot_diff(self):
        for i in range(0,n):
            force_sum = (inputdata[i][3]) + np.array(inputdata[i][4]) + np.array(inputdata[i][5]) + np.array(inputdata[i][6]) + np.array(inputdata[i][7]) + np.array(inputdata[i][8]) + np.array(inputdata[i][9])
            plt.plot(np.array(inputdata[i][0]), (np.array(force_sum)-np.array(inputdata[i][10])), 'o-', label=legends[i])
        plt.ylabel('total block force - total force [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Force difference')
        plt.legend()
        if self.sav == 1:
            plt.savefig("tot_dif.png")
            shutil.move("tot_dif.png", self.path1)
        plt.show()
    def rough1(self):
        for i in range(0, n):
            #plt.plot(np.array(inputdata[i][0])[:6], (np.array(inputdata[i][3])+np.array(inputdata[i][4])+np.array(inputdata[i][5])+np.array(inputdata[i][6]))[:6] , 'o-',
            #         label="upp part sum")
            #plt.plot(np.array(inputdata[i][0])[:6],
            #         (np.array(inputdata[i][9]) + (np.array(inputdata[i][7]) + np.array(inputdata[i][8])))[:6], 'o-',
            #         label="low part sum")
            plt.plot(np.array(inputdata[i][0]), (np.array(inputdata[i][3])+np.array(inputdata[i][4])+np.array(inputdata[i][5])+np.array(inputdata[i][6])) +
                     (np.array(inputdata[i][9]) + (np.array(inputdata[i][7]) + np.array(inputdata[i][8]))), 'o-',
                     label="difference")
        plt.ylabel('block forces [N] ')
        plt.xlabel('Inner Coil Position [mm]')
        plt.title('Individual Block Force')
        plt.legend()
        if self.sav == 1:
            plt.savefig("b5.png")
            shutil.move("b5.png", self.path1)
        plt.show()

class Impedance_graphs():
    def __init__(self, save, directory=None):
        self.sav = save
        self.directory = directory
        if self.directory and self.sav == 1:
                parent_dir = r""
                path1 = os.path.join(parent_dir, self.directory)
                self.path1 = path1
                os.mkdir(self.path1)

    def reactance(self):
        for i in range(0, n):
            plt.plot(np.array(inputdata[i][3]).real.tolist(), np.array(inputdata[i][7]).real.tolist(), 'o-')
        plt.ylabel('reactance [Ω] ')
        plt.xlabel('frequency [KHz]')
        plt.title("average reactance of Fred's coil")
        if self.sav == 1:
            plt.savefig("low_inn.png")
            shutil.move("low_inn.png", self.path1)
        plt.show()
    def err_rea(self):
        for i in range(0, f):
            rea = []
            for j in range(0, n):
                rea.append(inputdata[j][7][i])
            r = abs(np.array(rea))
            rea_err.append(np.std(r))
            rea_mean.append(np.mean(r))
        print("err :", rea_err)
        plt.errorbar((abs(np.array(inputdata[1][3])) / 1000)[1:8], ((np.array(rea_mean))/1000)[1:8],
                     yerr=((np.array(rea_err))/1000)[1:8], capsize = 4)
        plt.xlabel("frequency [KHz]")
        plt.ylabel("reactance [KΩ]")
        plt.show()
    def err_ind(self):
        for i in range(0, f):
            ind = []
            for j in range(0, n):
                ind.append(inputdata[j][8][i])
            r = abs(np.array(ind))
            ind_err.append(np.std(r))
            ind_mean.append(np.mean(r))
        print("err ind :", ind_err)
        plt.errorbar((abs(np.array(inputdata[1][3])) / 1000), (np.array(ind_mean)),
                     yerr=(np.array(ind_err)), capsize = 4,  label='both limits (default)')
        plt.xlabel("frequency [KHz]")
        plt.ylabel("inductance [H]")
        plt.show()
    def err_imp(self):
        for i in range(0, f):
            ind = []
            for j in range(0, n):
                ind.append(inputdata[j][9][i])
            r = abs(np.array(ind))
            imp_err.append(np.std(r))
            imp_mean.append(np.mean(r))
        print("err imp :", imp_err)
        plt.errorbar((abs(np.array(inputdata[1][3])) / 1000)[1:8], ((np.array(imp_mean)))[1:8],
                     yerr=((np.array(imp_err)))[1:8], capsize = 4)
        plt.xlabel("frequency [KHz]")
        plt.ylabel("impedance [Ω]")
        plt.show()
    def err_rat(self):
        for i in range(0, f):
            v_in = []
            v_out = []
            for j in range(0, n):
                v_in.append(inputdata[j][4][i])
                v_out.append(inputdata[j][5][i])
            r_i = abs(np.array(v_in))
            r_o = abs(np.array(v_out))
            v_in_err.append(np.std(r_i))
            v_out_err.append(np.std(r_o))
            v_in_mean.append(np.mean(r_i))
            v_out_mean.append(np.mean(r_o))
        a = np.array(v_out_mean)/(np.array(v_in_mean)*0.965)
        v_o = (np.array(v_out_err)/np.array(v_out_mean))**2
        v_i = (np.array(v_in_err) / np.array(v_in_mean)) ** 2
        s = np.sqrt(v_o+v_i)
        r = a*s
        rl = 36.1
        r1 = 990
        p = rl+r1
        t = (np.array(a)**2-1)
        rea_un = (np.sqrt(t/(rl**2-(np.array(a)**2)*(p**2)))*(((p*p)-rl**2)/(n*n))*(2*r*a))/2
        rea = np.sqrt(((rl*rl)-(a*p)**2)/t)
        print("err v_in, mean v_in :", v_in_err, v_in_mean)
        print("err v_out, mean v_out :", v_out_err, v_out_mean)
        print("ratio_mean :", a)
        print("ratio**2_un :", 2*r*a)
        print("ratio_un :", r)
        #plt.plot((abs(np.array(inputdata[1][3])) / 1000), 2*r*100, "o--")
        plt.plot((abs(np.array(inputdata[1][3])) / 1000), rea_un/rea, "o--")
        plt.xlabel("frequency [KHz]")
        plt.ylabel("rea rel ")
        plt.show()

'''
