import sys
import numpy as np
#import Analysis.plot_design as plot_design
import plot_design
import warnings
warnings.filterwarnings('ignore')

#plots = [uppout_vol, lowout_vol, inncoil_vol, norm_sig, norm_fit, fit, norm_fit_sig]


graph = plot_design.VC(0)


graph.force('mag_norm')

# b = np.load("C:/Users/kumar/PycharmProjects/lvdtsimulations/Kumar/modules/I_860k_ana.npz")
# print(b.files)


