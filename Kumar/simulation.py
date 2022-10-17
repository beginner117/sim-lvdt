import LVDT_mag
import LVDT
import VC
import VConly

trail1 = LVDT.Analysis(24, "20mA_fullfit_step1_11")

lis = [trail1]
for item in lis:
    item.simulate()


