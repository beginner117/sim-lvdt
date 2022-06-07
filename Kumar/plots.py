import plot_design_text
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import warnings
warnings.filterwarnings('ignore')
#plots = [uppout_vol, lowout_vol, inncoil_vol, norm_sig, norm_fit, fit, norm_fit_sig]

graph = plot_design_text.Yoke_graphs(1, "b7+b8")
graph.b1()
graph.b2()
graph.b3()
graph.b4()
graph.b5()
graph.b6()
graph.b7()
graph.b_total()
graph.mag()
graph.low_inn()
#graph.tot_diff()





