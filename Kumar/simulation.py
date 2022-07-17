import design
import femm_model
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
import VConly



trail1 = smallIP_LVDT.Analysis(10, "def_try29")
#trail2 = LVDT_F1F2_mirrortower.Analysis(18, "tria1")




lis = [trail1]
for item in lis:
    item.simulate()

