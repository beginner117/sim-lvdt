import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil
import warnings
warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol, [2]-low_out_vol, [3]-inn_vol, [4]-Norm_Out_Sig, [5]-fit_err (or) fit, [6]-norm-fit
output_files = ["dist9.txt", "mir_def.txt", "dist11.txt",  "dist12.txt"]

legends = ["dist = 9", "dist = 10(def)", "dist = 11", "dist = 12"]
inputdata = []

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

plt.style.use(['science','grid','notebook'])

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][1]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Upper Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("upp_out.png")
shutil.move("upp_out.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][2]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Lower Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("low_out.png")
shutil.move("low_out.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][3]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Inner Out Coil Voltage [V]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("Inn_vol.png")
shutil.move("Inn_vol.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Out Coil signal [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("norm_sig.png")
shutil.move("norm_sig.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][6]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Fit Error [%]')
plt.xlabel('Inner Coil Position [mm]')
plt.ylim(0,4)
plt.legend()
plt.savefig("normfiterr.png")
shutil.move("normfiterr.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()


for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][5]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Fit Error [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("fiterr.png")
shutil.move("fiterr.png", r"C:\Users\kumar\OneDrive\Desktop\pi\mirror\res\dist")
plt.show()


'''
fit_d = [-7.12219038e+01, -6.40996332e+01, -5.69773626e+01, -4.98550920e+01,
 -4.27328214e+01, -3.56105508e+01, -2.84882801e+01, -2.13660095e+01,
 -1.42437389e+01, -7.12146834e+00,  8.02260464e-04,  7.12307286e+00,
  1.42453435e+01,  2.13676141e+01,  2.84898847e+01,  3.56121553e+01,
  4.27344259e+01,  4.98566965e+01,  5.69789671e+01,  6.41012377e+01,
  7.12235083e+01]
a1 = np.array(fit_d)
print(plt.style.available)

plt.style.use(['science','grid','notebook'])
for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), abs(np.array(inputdata[i][4]).real.tolist()-a1), 'o-', label=legends[i])
plt.ylabel('Norm_signals - Default Fit(-1,1) [V/mmA] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("outrad_tail.png")
shutil.move("outrad_tail.png", r"C:Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res")
plt.show()

#norm_fit_err1 = (abs(np.array(inputdata[i][4]) - a1) / abs(np.array(inputdata[i][4])))*100
for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), (abs(np.array(inputdata[i][4]) - a1) / abs(np.array(inputdata[i][4])))*100, 'o-', label=legends[i])
plt.ylabel('$\dfrac{(Norm.signals - Default Fit(-1,1))}{Norm.signals}$  [V/mmA] ')
plt.xlabel('Inner Coil Position [mm]')
#plt.ylim(0, 15)
plt.legend()
plt.savefig("outrad_tail_nor.png")
shutil.move("outrad_tail_nor.png", r"C:Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res")
plt.show()
'''