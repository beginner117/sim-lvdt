import warnings
from matplotlib import pyplot as plt
import numpy as np
warnings.filterwarnings('ignore')
#import rough

output_files = [ "linearity/50p_25f_1mic_A_sl_M", "linearity/50p_25f_1mic_A_sl_M0.1", "linearity/50p_25f_1mic_A_sl_fullM0.1"]
legends = [ r'step: 1μm, fit:25pts'"\n"'mesh : 1,0.5,1', r'step: 1μm, fit:25pts'"\n"'mesh : 0.1,0.5,1', r'step: 1μm, fit:25pts'"\n"'mesh : 0.1,0.5,0.5']
inputdata = []
for i in range(0,len(output_files)):
    X = np.loadtxt(output_files[i], dtype=complex)
    inputarray = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    inputdata.append(inputarray)
n = len(output_files)
p1_1 = np.arange(-0.025, 0, 0.001)
p2_1 = np.arange(0.001, 0.026, 0.001)
p1_2 = np.arange(-0.025, 0, 0.001)
p2_2 = np.arange(0.001, 0.026, 0.001)
p1 = np.concatenate([p1_1, p2_1])
p2 = np.concatenate([p1_2, p2_2])
p11 = np.concatenate([p1_1, p2_1])
p22 = np.concatenate([p1_2, p2_2])
p = [p1, p2]
c = ['r', 'b']
#f = (abs(np.array(slope)-3.281)/np.array(slope))*100
#d = (abs(angle-73.042)/angle)*100

for i in range(0, n):
    a = inputdata[i][1]
    angle = (np.array(a).real)
    slope = (np.tan(angle * np.pi / 180))
    f = (abs(np.array(slope) - 3.281) / np.array(slope))
    plt.plot(p11[:23], f[:23],"o--", label = legends[i])
plt.ylabel("relative slope error")
plt.xlabel("Inn coil position")
#plt.ylim(0, 0.02)
plt.legend()
plt.show()
for i in range(0, n):
    a = inputdata[i][0]
    plt.plot(p11[:23], a[:23],"o--", label = legends[i])
plt.ylabel("linearity [%]")
plt.xlabel("Inn coil position")
#plt.ylim(0, 2)
plt.legend()
plt.show()
for i in range(0, n):
    a = inputdata[i][0]
    arc = np.arctan(a)
    plt.plot(p22, arc,"o--", label = legends[i])
plt.ylabel("AAP")
plt.xlabel("Inn coil position")
plt.legend()
plt.show()


'''
#def gauss(x, a, b):
def loga(x,a,b):
    #y = a * np.exp(-1 * b * x ** 2)
    y = a*np.exp(b*x)
    return y
p1 = np.arange(-0.1, 0, 0.001)
p2 = np.arange(0.001, 0.101, 0.001)
p = np.concatenate([p1, p2])
print(len(inputdata[0]))

x2 = p2[1:]
y2 = inputdata[0][0][101:]
parameters, covariance = curve_fit(loga, x2, y2)
a_fit = parameters[0]
b_fit = parameters[1]

#para = [a_fit, np.sqrt(1 / (2 * b_fit))]
para = [a_fit, b_fit]
print("parameters :", para)
fit_y = loga(x2, a_fit, b_fit)
#angles = np.array(inputdata[0][1]).real.tolist()
#print(angles)
plt.plot(x2,y2, "o--", label = "data")
plt.plot(x2, fit_y, label = "exp fit")
plt.ylabel("relative error")
plt.xlabel("Inn coil position [mm]")
plt.legend()
plt.show()

obs_data = fit_y
exp_data = y2
chi_square_test_statistic, p_value = stats.chisquare(obs_data, exp_data)
print('chi_square_test_statistic is : ' + str(chi_square_test_statistic))
print('p_value : ' + str(p_value))
# find Chi-Square critical value
print(stats.chi2.ppf(1 - 0.05, df=6))
'''
