import design
import fem_cond
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import pickle


class Req_plots():
    def __init__(self, out_vol, inn_vol, phase, norm_signal, fit_error, Norm_fiterror):
        self.out_vol = out_vol
        self.inn_vol = inn_vol
        self.phase = phase
        self.norm_signal = norm_signal
        self.fit_error = fit_error
        self.Norm_fiterror = Norm_fiterror

class Print_data():
    def __init__(self, phase,slope):
        self.phase = phase
        self.slope = slope

class Data_save():
    def __init__(self, directory, parent_dir):
        self.dir = directory
        self.par_dir = parent_dir
        self.path = os.path.join(parent_dir, directory)
        os.makedirs(self.path)

class Plot_parameters():
    def __init__(self, x, y, x_lab, y_lab,save, save_dir=None, filename=None, title=None):
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
        plt.show()
        if title:
            plt.title(title)


