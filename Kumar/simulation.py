import LVDT_mag
import LVDT
import VC
import VConly

trail1 = LVDT_mag.Analysis(54.5, "tr7")
#trail2 = LVDT_mag.Analysis(17, "dis52")
#trail1 = VC.Analysis(11, "tr6")
#trail2 = VC.Analysis(13, "irad_vc_13")
#trail3 = VC.Analysis(15, "irad_vc_15")




#trail2 = VConly.Analysis(10, "trail45")
#trail1 = LVDT_mag.Analysis(24, "def_try2")


lis = [trail1]
for item in lis:
    item.simulate()



