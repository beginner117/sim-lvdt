import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# output_file data : [0]-position, [1]-upp_out_vol, [2]-low_out_vol, [3]-inn_vol, [4]-Norm_Out_Sig, [5]-fit_err, [6]-norm-fit
output_files = []

legends = []
inputdata = []

for i in range(0,len(output_files)):
    inputarray = np.loadtxt(output_files[i], dtype=complex)
    inputdata.append(inputarray)

print(inputdata)

#print(plt.style.available)
plt.style.use(['science','grid','notebook'])

for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][1].real, 'o-', label=legends[i])
plt.ylabel('Upper Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()

for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][2].real, 'o-', label=legends[i])
plt.ylabel('Lower Out Coil Voltage [V] ')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()

for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][3].real, 'o-', label=legends[i])
plt.ylabel('Inner Out Coil Voltage [V]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()

for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][4].real, 'o-', label=legends[i])
plt.ylabel('Normalised Out Coil signal [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()

for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][6].real, 'o-', label=legends[i])
plt.ylabel('Normalised Fit Error []')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()


for i in range(0,len(output_files)):
    plt.plot(inputdata[i][0], inputdata[i][5].real, 'o-', label=legends[i])
plt.ylabel('Fit Error [V/mmA]')
plt.xlabel('Inner Coil Position [mm]')
plt.legend()
plt.show()

