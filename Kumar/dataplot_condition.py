import matplotlib.pyplot as plt
import os
import shutil
import numpy as np

class Req_plots():
    def __init__(self, out_vol, inn_vol, norm_signal, fit_error, Norm_fiterror, phase = None, impedance=None, extras=None):
        self.out_vol = out_vol
        self.inn_vol = inn_vol
        self.phase = phase
        self.norm_signal = norm_signal
        self.fit_error = fit_error
        self.Norm_fiterror = Norm_fiterror
        self.impedance = impedance
        self.extras = extras

class Print_data():
    def __init__(self, phase,slope):
        self.phase = phase
        self.slope = slope

class Save_data():
    def __init__(self, filename, inn_position, upp_vol=None, low_vol=None, inn_vol=None, out_sig=None, fiterr=None, norm_fit=None, Inn_ind=None, Inn_res=None, rough1=None, rough2=None):
        self.filename = filename
        self.inn_position = inn_position
        self.upp_vol = upp_vol
        self.low_vol = low_vol
        self.inn_vol = inn_vol
        self.out_sig = out_sig
        self.fiterr = fiterr
        self.norm_fit = norm_fit
        self.inn_ind = Inn_ind
        self.inn_res = Inn_res
        self.rough1 = rough1
        self.rough2 = rough2
        #if self.rough1.any():
            #data = np.column_stack((self.rough1, self.rough2))
        #else:
        data = np.column_stack((self.inn_position, self.upp_vol, self.low_vol, self.inn_vol, self.out_sig, self.fiterr, self.norm_fit, self.inn_ind, self.inn_res))
        np.savetxt(self.filename, data)



class Plot_parameters():
    def __init__(self, x, y, x_lab, y_lab, save, save_dir=None, filename=None, title=None):
        self.x = x
        self.y = y
        self.xlab = x_lab
        self.y_lab = y_lab
        self.title = title
        self.save = save
        self.filename = filename
        self.save_dir = save_dir
        plt.plot(x,y,"o-")
        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        if self.save == 1:
            plt.savefig(filename)
            shutil.move(filename, save_dir)
        if title:
            plt.title(title)
class Plot_base():
    def __init__(self, x_lab, y_lab):
        self.x_lab = x_lab
        self.y_lab = y_lab
        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        plt.legend()
        plt.show()
class save_figure():
    def __init__(self, save, title, location):
        self.save = save
        self.title = title
        self.location = location
        if self.save == 1:
            plt.savefig(self.title)
            shutil.move(self.title, self.location)



