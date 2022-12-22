import matplotlib.pyplot as plt
import numpy as np
import csv

with open('TINA/tcurve_r_vf5.txt', 'r') as f:
    fr5 = []
    v_abs5 = []
    phase5 = []
    for line in f:
        line = line.split("\t")
        try:
            a5 = float(line[0].replace(",", "."))
            b5 = float(line[1].replace(",", "."))
            c5 = float(line[2].replace(",", "."))
            fr5.append(a5)
            v_abs5.append(b5)
            phase5.append(c5)
        except:
            pass

with open('TINA/tcurve_c_vf5.txt', 'r') as g:
    fr6 = []
    v_abs6 = []
    phase6 = []
    for line in g:
        line = line.split("\t")
        try:
            a6 = float(line[0].replace(",", "."))
            b6 = float(line[1].replace(",", "."))
            c6 = float(line[2].replace(",", "."))
            fr6.append(a6)
            v_abs6.append(b6)
            phase6.append(c6)
        except:
            pass
with open('TINA/tcurve_ind_vf5.txt', 'r') as h:
    fr4 = []
    v_abs4 = []
    phase4 = []
    for line in h:
        line = line.split("\t")
        try:
            a4 = float(line[0].replace(",", "."))
            b4 = float(line[1].replace(",", "."))
            c4 = float(line[2].replace(",", "."))
            fr4.append(a4)
            v_abs4.append(b4)
            phase4.append(c4)
        except:
            pass
plt.plot(fr4, np.array(v_abs4), label = "inductance:25.77mH")
plt.plot(fr5, np.array(v_abs5), label = "resistance:1.619KΩ")
plt.plot(fr6, np.array(v_abs6), label = "capacitence:9.83nF")
plt.xscale('log')
plt.xlabel("frequency")
plt.ylabel("output noise [$\dfrac{V}{sqrt(Hz)}$]")
plt.title("impedance : 1.619KΩ")
plt.legend()
plt.show()

