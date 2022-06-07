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



trail1 = LVDT_F1F2_mirrortower.Analysis(16, "inht16")
#trail2 = LVDT_F1F2_mirrortower.Analysis(13.5, "def_bench")
trail3 = LVDT_F1F2_mirrortower.Analysis(20, "inht20")
trail4 = LVDT_F1F2_mirrortower.Analysis(22, "inht22")

lis = [trail1, trail3, trail4]
for item in lis:
    item.simulate()

