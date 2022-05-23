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


trail1 = LVDT_F1F2_mirrortower.Analysis(9, "di9")
trail2 = LVDT_F1F2_mirrortower.Analysis(10, "defvs1")
trail3 = LVDT_F1F2_mirrortower.Analysis(11, "di11")
trail4 = LVDT_F1F2_mirrortower.Analysis(12, "di12")

lis = [trail1]
for item in lis:
    item.simulate()

