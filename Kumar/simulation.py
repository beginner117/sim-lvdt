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



trail1 = smallIP_LVDT.Analysis(5, "5lay")
trail2 = smallIP_LVDT.Analysis(4, "4lay")
trail3 = smallIP_LVDT.Analysis(3, "3lay")
trail4 = smallIP_LVDT.Analysis(2, "2lay")
trail5 = smallIP_LVDT.Analysis(1, "1lay")


lis = [trail5]
for item in lis:
    item.simulate()

