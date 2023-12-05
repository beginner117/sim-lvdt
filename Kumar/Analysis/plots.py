import sys
import numpy as np
#import Analysis.plot_design as plot_design
import plot_design
import warnings
warnings.filterwarnings('ignore')

#plots = [uppout_vol, lowout_vol, inncoil_vol, norm_sig, norm_fit, fit, norm_fit_sig]


graph = plot_design.Lvdt(0)

#graph.lin_imp()
graph.norm_fit('slope')




