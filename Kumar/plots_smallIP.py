import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import warnings
warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol, [2]-low_out_vol, [3]-inn_vol, [4]-Norm_Out_Sig, [5]-fit_err(1) , [6]-norm-fit(1)
#output_files = ["dis:9,5.txt", "dis:10,5.txt", "dis:11,5.txt"]
output_files = ["lv_11", "lv_13", "lv_15", "lv_17"]
legends = ["11,35(def)", "rad:(13,35)", "rad:(15,35)", "rad:(17,35)"]
inputdata = []

save = 1
if save == 1:
    directory = "lv_radgap_comp"
    parent_dir = r"C:\Users\kumar\OneDrive\Desktop\pi\bench"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    data = path


#for i in range(0,len(output_files)):
#    inputarray = np.loadtxt(output_files[i], dtype=complex)
#    inputdata.append(inputarray)
for i in range(0,len(output_files)):
    X = np.loadtxt(output_files[i], dtype=complex)
    inputarray = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    inputdata.append(inputarray)

#print(inputdata)
#arr = np.array(inputdata[0][1]).real
#lis = arr.tolist()
print(np.array(inputdata[1][1]).real.tolist())
print(np.array(inputdata[1][0]).real.tolist())
print(len(output_files))

'''
plt.style.use(['science','grid','notebook'])

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][1]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Upper Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("upp_out.png")
    shutil.move("upp_out.png", data)
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][2]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Lower Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("low_out.png")
    shutil.move("low_out.png", data)
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][3]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Inner Out Coil Voltage [V]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("Inn_vol.png")
    shutil.move("Inn_vol.png", data)
plt.show()
'''
plt.style.use(['science','grid','notebook'])
for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Out Coil signal [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("norm_sig.png")
    shutil.move("norm_sig.png", data)
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][6]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Fit Error [%]')
plt.xlabel('Inner Coil Position [mm]')
plt.ylim(0,4)
plt.legend()
if save == 1:
    plt.savefig("normfiterr.png")
    shutil.move("normfiterr.png", data)
plt.show()


for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][5]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Fit Error [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("fiterr.png")
    shutil.move("fiterr.png", data)
plt.show()
'''
for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][7]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Fit Norm. Out Coil signal [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
if save == 1:
    plt.savefig("fit_norm_sig.png")
    shutil.move("fit_norm_sig.png", data)
plt.show()
'''