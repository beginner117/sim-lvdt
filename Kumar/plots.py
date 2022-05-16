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

graph = plot_design.Graphs(0, "compa")
graph.norm_sig()
graph.slope()
graph.fit()
graph.norm_fit()
graph.lin_imp()
#graph.linear_range()