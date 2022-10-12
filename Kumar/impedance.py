import numpy as np
import matplotlib.pyplot as plt
import TINA_simulation
'''
turns_I = [100.50, 41.88, 62.81, 33.50, 33.50, 75.38, 100.50, 75.38]
turns_o = [56.53, 41.88, 50.25, 33.50, 33.50, 56.53, 56.53, 56.53]

ro = 11
n = 2*(0.2032+0.0178)
layers = 6
s = 0
turns_pr_lay = 100
l = 13.5
mu = 1.256*(10**-6)
mutual = 0
if mutual == 0:
    for i in range(0,layers):
        r = ro+(i*n)
        a = r*r
        b = (2*(layers-i)-1)*a
        s = b+s
        print(s)
if mutual == 1:
    for i in range(0,layers):
        r = ro+(i*n)
        a = r*r
        b = (2*(layers-i-1))*a
        s = b+s
        print(s)

imp = ((mu*turns_pr_lay*turns_pr_lay*(np.pi))/l)*s
print("ind in mH :", imp)

types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'J']

impedance_femm = [5.35, 0.399, 3.80, 0.566, 0.687, 9.68, 3.86, 9.68]
res_femm = [(24.025, 336.493), (4.44, 25.131),(18.170, 238.936), (5.269, 35.584), (5.951, 43.227), (33.358, 608.283), (19.933, 242.552), (33.358,608.283) ]
impedance_online = [5.34, 0.407, 3.852, 0.582, 0.707, 9.65, 3.85, 9.729]
'''


#v_in = [a1+a2+a3+a4+a5+a6  for (a1, a2, a3, a4, a5, a6, a7) in zip(datasets.v_in_1, datasets.v_in_2, datasets.v_in_3, datasets.v_in_4, datasets.v_in_5, datasets.v_in_6, datasets.v_in_7)]
#v_out = [b1+b2+b3+b4+b5+b6  for (b1, b2, b3, b4, b5, b6, b7) in zip(datasets.v_out_1, datasets.v_out_2, datasets.v_out_3, datasets.v_out_4, datasets.v_out_5, datasets.v_out_6, datasets.v_out_7)]
trials = 6
fre = TINA_simulation.fre
v_in = TINA_simulation.vo_in_5
v_out = TINA_simulation.vo_out_5
date = "25_08out"
save = 1
#v_rat_tina = np.array([0.131, 0.163, 0.250, 0.341, 0.427, 0.504, 0.654, 0.754, 0.820, 0.864, 0.895])
v_rat = np.array(v_out)/(np.array(v_in)*0.965)

imp = np.zeros(len(fre))
ind = np.zeros(len(fre))
rea = np.zeros(len(fre))
ref_res = []
ind_res = []
correction = []

r_ref = 990
#r_ind = 135.4
c = 0.965
r_ind = 36.1

for i in range(0, len(fre)):
    rea[i] = np.sqrt(((r_ind ** 2) - ((r_ref + r_ind) ** 2) * (v_rat[i] ** 2)) / ((v_rat[i] ** 2) - 1))
    ind[i] = rea[i]/(2*np.pi*fre[i])
    imp[i] = np.sqrt((rea[i]**2) + (r_ind)**2)
    ref_res.append(r_ref)
    ind_res.append(r_ind)
    correction.append(c)

if save == 1:
    data = np.column_stack((correction, ref_res, ind_res, fre, v_in, v_out, v_rat, rea, ind, imp,))
    np.savetxt(date, data)
print("impedance : ", imp)
print("inductance : ", ind)
print("reactance :", rea)

#plt.plot(np.array(fre)/1000, np.array(imp1)/1000, "o--", label = "TINA")
plt.plot(np.array(fre)/1000, np.array(imp)/1000, "o--", label = "c = 0.965")
plt.xlabel("frequency [KHz]")
plt.ylabel("impedance [kΩ]")
plt.legend()
plt.title("impedance of Fred's coil")
plt.grid()
plt.show()

#plt.plot(np.array(fre)/1000, np.array(ind1)*1000, "o--", label = "TINA")
plt.plot(np.array(fre)/1000, np.array(ind)*1000, "o--", label = "c = 0.965")
plt.xlabel("frequency [KHz]")
plt.ylabel("inductance [mH]")
plt.legend()
plt.title("inductance of Fred's coil")
plt.grid()
plt.show()

plt.plot(np.array(fre)/1000, np.array(rea)/1000, "o--", label = "c = 0.965")
plt.xlabel("frequency [KHz]")
plt.ylabel("reactance [kΩ]")
plt.legend()
plt.title("reactance of Fred's coil")
plt.grid()
plt.show()











