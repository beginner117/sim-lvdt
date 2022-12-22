import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.optimize as opt
from scipy import signal
import warnings
import shutil

class Compare():
    def __init__(self, exp_data, sim_data):
        self.exp_data = exp_data
        self.sim_data = sim_data
        self.a1 = np.load(self.exp_data)
        self.a2 = np.load(self.sim_data)
        print("measures data :", self.a1.files)
        print("simulated data :", self.a2.files)
        print("PI stage movement : ", self.a1["PI"][0], "to ", self.a1["PI"][len(self.a1["PI"])-1], "vertical step size : ", self.a1["PI"][1][1]-self.a1["PI"][0][1] )
        print("DAQ sampling frequency :", len(self.a1["DAQ"][0]))
    def results(self):
        x = np.arange(1, len(self.a1["DAQ"][0])+1, 1)
        amp = []
        fre = []
        pha = []
        con = []
        pos = []
        for i in range(len(self.a1["DAQ"])):
            ff = np.fft.fftfreq(len(x), x[1]-x[0])
            Fyy = np.fft.fft(self.a1["DAQ"][i])
            guess_amp = np.std(self.a1['DAQ'][i]) * 2.**0.5
            guess_offset = np.mean(self.a1['DAQ'][i])
            guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
            guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])
            def sinfunc(t, a, w, p, c):
                return a*(np.sin((w*t)+p))+c
            popt, pcov = curve_fit(sinfunc, x, self.a1['DAQ'][i], p0=guess)
            f = popt[1] / (2. * np.pi)
            #print(popt)
            amp.append(popt[0])
            fre.append(popt[1])
            pha.append(popt[2])
            con.append(popt[3])
            pos.append(self.a1['PI'][i][1])
        inn_pos = np.array(self.a2["IC_positions"])
        inn_vol = abs(np.array(self.a2["IC_voltages"]))
        uppout_vol = np.array(self.a2["UOC_voltages"])
        lowout_vol = np.array(self.a2["LOC_voltages"])
        out_sig = abs(uppout_vol)-abs(lowout_vol)
        norm_sig = out_sig/inn_vol
        upd_amp = np.zeros(len(amp))
        print(np.argmin(abs(np.array(amp))))
        for i in range(0, len(amp)):
            if i<np.argmin(abs(np.array(amp))):
                upd_amp[i] = -abs(np.array(amp)[i])
            else:
                upd_amp[i] = abs(np.array(amp)[i])

        class Response():
            def __init__(self):
                pass
            m_exp, co_exp = np.polyfit(pos, upd_amp/0.5, 1)
            print("exp signal slope :", m_exp,co_exp)
            exp_fit = m_exp*np.array(pos)+co_exp
            gain_factor = 69
            m_fem, co_fem = np.polyfit(inn_pos, norm_sig*gain_factor, 1)
            print("femm signal slope :", m_fem,co_fem)
            sim_fit = m_fem*np.array(inn_pos)+co_fem
        response = Response()

        class Linearity():
            def __init__(self) -> None:
                pass
            fiterr_exp = (response.exp_fit-(upd_amp)/0.5)
            #relerr_exp = ((abs(fiterr_exp))/abs(upd_amp/0.5))*100
            relerr_exp = ((abs(response.exp_fit-(upd_amp)/0.5))/abs(upd_amp/0.5))*100
            fiterr_fem = (response.sim_fit-(norm_sig))
            #relerr_fem = ((abs(fiterr_fem*(response.gain_factor)))/abs(norm_sig*response.gain_factor))*100
            relerr_fem = ((abs(response.sim_fit-(norm_sig)*69))/abs(norm_sig*69))*100

            plt.plot(pos, relerr_exp, "o--", label = "measured")
            plt.plot(pos, relerr_fem, "o--", label = "simulated")
            plt.xlabel("Inn coil(PI stage) position [mm]")
            plt.ylabel("Linearity [V]")
            plt.legend()
            plt.show()
        linearity = Linearity()
