import design
import femm
import numpy as np
import cmath
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import shutil
import threading

import LVDT_F1F2_benchtower
#import smallIP_VC_31AWG


trail1 = LVDT_F1F2_benchtower.Analysis(11, "lv_11")
trail2 = LVDT_F1F2_benchtower.Analysis(13, "lv_13")
trail3 = LVDT_F1F2_benchtower.Analysis(15, "lv_15")
trail4 = LVDT_F1F2_benchtower.Analysis(17, "lv_17")
#trail3 = thread1.Trail(9, "check3")

lis = [trail1, trail2, trail3, trail4]
for item in lis:
    item.simulate()

