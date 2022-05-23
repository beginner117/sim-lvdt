import plot_design
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import warnings
warnings.filterwarnings('ignore')
#plots = [uppout_vol, lowout_vol, inncoil_vol, norm_sig, norm_fit, fit, norm_fit_sig]

graph = plot_design.Yoke_graphs(0, "compa")
graph.low_inn()
graph.mag()

