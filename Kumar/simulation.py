import design
import fem_cond
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import threading
import smallIP_LVDT
import LVDT_F1F2_mirrortower
import smallIp_VC



trail1 = LVDT_F1F2_mirrortower.Analysis(18, "fred14")
#trail2 = LVDT_F1F2_mirrortower.Analysis(16, "innht16")
#trail3 = LVDT_F1F2_mirrortower.Analysis(20, "innht20")
#trail4 = LVDT_F1F2_mirrortower.Analysis(19, "innht19")



lis = [trail1]
for item in lis:
    item.simulate()

