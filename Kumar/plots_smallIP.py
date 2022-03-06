import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import shutil
import warnings
warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol, [2]-low_out_vol, [3]-inn_vol, [4]-Norm_Out_Sig, [5]-fit_err, [6]-norm-fit
output_files = [ "sip_def_sml.txt", "sip_inn wid_25_sml.txt", "sip_inn wid_26_sml.txt"]

legends = ["inn wid = 24(def)", "inn wid = 25", "inn wid = 26"]
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

#'''
#print(plt.style.available)
plt.style.use(['science','grid','notebook'])

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][1]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Upper Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("upp_out.png")
shutil.move("upp_out.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][2]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Lower Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("low_out.png")
shutil.move("low_out.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][3]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Inner Out Coil Voltage [V]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("Inn_vol.png")
shutil.move("Inn_vol.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][4]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Out Coil signal [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.savefig("norm_sig.png")
shutil.move("norm_sig.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()

for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][6]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Normalised Fit Error [%]')
plt.xlabel('Inner Coil Position [mm]')
plt.ylim(0,0.4)
plt.legend()
plt.savefig("normfiterr.png")
shutil.move("normfiterr.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()


for i in range(0,len(output_files)):
    plt.plot(np.array(inputdata[i][0]).real.tolist(), np.array(inputdata[i][5]).real.tolist(), 'o-', label=legends[i])
plt.ylabel('Fit Error [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
#plt.savefig("fiterr.png")
#shutil.move("fiterr.png", r"C:\Users\kumar\OneDrive\Desktop\pi\lvdt\small, large ip\small_IP\res\innwidth_2")
plt.show()
#'''
'''
x2 = [8.5/22, 8.5/20, 10.5/24, 8.5/18, 10.5/22, 12.5/24, 10.5/20, 13.5/24, 12.5/22, 10.5/18, 13.5/22, 12.5/20, 13.5/20, 13.5/18]
y2 = [22.499, 21.8, 28.73, 19.4, 27.3, 33.441, 26.7, 35.8, 31.8, 23.8, 33.8, 29.9007, 31.8, 35.8]
plt.plot(x2, y2, 'o-')
plt.xlabel("out coil width/inn coil width (ratio)")
plt.ylabel("Slope (sensitivity)")
plt.savefig("ratio.png")

plt.show()
'''