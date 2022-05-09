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



trail1 = smallIP_LVDT.Analysis(23, "inn23")
trail2 = smallIP_LVDT.Analysis(25, "inn25")
trail3 = smallIP_LVDT.Analysis(26, "inn26")
#trail2 = smallIP_LVDT.Analysis(26,12,31.5, "imp")
#trail2 = smallIP_LVDT.Analysis(26,12,31.5, "imp")


lis = [trail1, trail2, trail3]
for item in lis:
    item.simulate()

