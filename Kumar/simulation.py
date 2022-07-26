import LVDT_mag
import LVDT
import VC
import VConly

#trail1 = VC.Analysis(10, "def_try29")
trail2 = LVDT_mag.Analysis(24, "tria11")

lis = [trail2]
for item in lis:
    item.simulate()

