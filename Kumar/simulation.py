import design
import femm
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


trail1 = smallIP_LVDT.Analysis(26.5, "dis26")
#trail2 = smallIP_LVDT.Analysis(24, "defs")
trail3 = smallIP_LVDT.Analysis(30.5, "dis30")
trail4 = smallIP_LVDT.Analysis(32.5, "dis32")
#trail2 = smallIP_LVDT.Analysis(26,12,31.5, "imp")


lis = [trail1, trail3, trail4]
for item in lis:
    item.simulate()

