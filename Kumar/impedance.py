import numpy as np
import matplotlib.pyplot as plt
import datasets
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
'''

types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'J']

impedance_femm = [5.35, 0.399, 3.80, 0.566, 0.687, 9.68, 3.86, 9.68]
res_femm = [(24.025, 336.493), (4.44, 25.131),(18.170, 238.936), (5.269, 35.584), (5.951, 43.227), (33.358, 608.283), (19.933, 242.552), (33.358,608.283) ]
impedance_online = [5.34, 0.407, 3.852, 0.582, 0.707, 9.65, 3.85, 9.729]

v_in_high = [4.18, 4.18, 4.18, 4.6, 4.58, 4.58, 4.62, 4.65, 4.65, 4.66, 4.70, 4.65, 4.68, 4.67]
v_out_high = [0.58, 0.71, 1.07, 1.58, 1.89, 2.10, 2.80, 3.25, 3.52, 3.76, 3.90, 4.05, 4.10, 4.15]
fre_high = [1000, 2000, 4000, 6000, 8000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 50000, 60000]

fre = datasets.fre
#v_in = np.array(np.array(datasets.v_in_1)+np.array(datasets.v_in_2)+np.array(datasets.v_in_3)+np.array(datasets.v_in_4)+np.array(datasets.v_in_5))/5
#v_out = np.array(np.array(datasets.v_out_1)+np.array(datasets.v_out_2)+np.array(datasets.v_out_3)+np.array(datasets.v_out_4)+np.array(datasets.v_out_5))/5
v_in = [a1+a2+a3+a4+a5  for (a1, a2, a3, a4, a5) in zip(datasets.v_in_1, datasets.v_in_2, datasets.v_in_3, datasets.v_in_4, datasets.v_in_5)]
v_out = [b1+b2+b3+b4+b5  for (b1, b2, b3, b4, b5) in zip(datasets.v_out_1, datasets.v_out_2, datasets.v_out_3, datasets.v_out_4, datasets.v_out_5)]
v_rat1 = np.array(v_out)/(np.array(v_in)/1.04)
v_rat2 = np.array(v_out)/(np.array(v_in)*0.965)
v_rat3 = np.array(v_out)/(np.array(v_in)*1)
#fre.extend(fre_high)
#v_in.extend(v_in_high)
#v_out.extend(v_out_high)
imp1 = np.zeros(len(fre))
imp2 = np.zeros(len(fre))
imp3 = np.zeros(len(fre))
ind1 = np.zeros(len(fre))
ind2 = np.zeros(len(fre))
ind3 = np.zeros(len(fre))
rea1 = np.zeros(len(fre))
rea2 = np.zeros(len(fre))
rea3 = np.zeros(len(fre))
r_ref = 990
#r_ind = 135.4
r_ind = 36.1

for i in range(0, len(fre)):
    rea1[i] = np.sqrt(((r_ind**2)-((r_ref+r_ind)**2)*(v_rat1[i]**2))/((v_rat1[i]**2)-1))
    rea2[i] = np.sqrt(((r_ind ** 2) - ((r_ref + r_ind) ** 2) * (v_rat2[i] ** 2)) / ((v_rat2[i] ** 2) - 1))
    rea3[i] = np.sqrt(((r_ind ** 2) - ((r_ref + r_ind) ** 2) * (v_rat3[i] ** 2)) / ((v_rat3[i] ** 2) - 1))
    ind2[i] = rea2[i]/(2*np.pi*fre[i])
    ind1[i] = rea1[i] / (2 * np.pi * fre[i])
    ind3[i] = rea3[i] / (2 * np.pi * fre[i])
    imp2[i] = np.sqrt((rea2[i]**2) + (r_ind)**2)
    imp1[i] = np.sqrt((rea1[i]**2) + (r_ind)**2)
    imp3[i] = np.sqrt((rea3[i]**2) + (r_ind)**2)

print("impedance1 : ", imp1)
print("impedance2 : ", imp2)
print("impedance3 : ", imp3)
print("inductance1 : ", ind1)
print("inductance2 : ", ind2)
print("inductance3 : ", ind3)
print("reactance1 :", rea1)
print("reactance2 :", rea2)
print("reactance3 :", rea3)
#plt.style.use([ 'grid', 'notebook'])

#plt.plot(np.array(fre)/1000, np.array(imp1)/1000, "o--", label = "c = 1.04")
plt.plot(np.array(fre)/1000, np.array(imp2)/1000, "o--", label = "c = 0.965")
plt.plot(np.array(fre)/1000, np.array(imp3)/1000, "o--", label = "c = 1")
plt.xlabel("frequency [KHz]")
plt.ylabel("impedance [kΩ]")
plt.legend()
plt.title("impedance of Fred's coil")
plt.show()

#plt.plot(np.array(fre)/1000, np.array(ind1)*1000, "o--", label = "c = 1.04")
plt.plot(np.array(fre)/1000, np.array(ind2)*1000, "o--", label = "c = 0.965")
plt.plot(np.array(fre)/1000, np.array(ind3)*1000, "o--", label = "c = 1")
plt.xlabel("frequency [KHz]")
plt.ylabel("inductance [mH]")
plt.legend()
plt.title("inductance of Fred's coil")
plt.show()

plt.plot(np.array(fre)/1000, np.array(rea2)*1000, "o--", label = "c = 0.965")
plt.plot(np.array(fre)/1000, np.array(rea3)*1000, "o--", label = "c = 1")
#plt.plot(np.array(fre)/1000, np.array(rea1)*1000, "o--", label = "c = 1.04")
plt.xlabel("frequency [KHz]")
plt.ylabel("reactance [kΩ]")
plt.legend()
plt.title("reactance of Fred's coil")
plt.show()











