import LVDT_mag
import LVDT
import VC
import VConly

trail1 = LVDT_mag.Analysis(11, "20mA_fullfit_step1_5")

#trail1 = VC.Analysis(11, "tr6")
#trail2 = VC.Analysis(13, "irad_vc_13")
#trail3 = VC.Analysis(15, "irad_vc_15")


lis = [trail1]
for item in lis:
    item.simulate()



