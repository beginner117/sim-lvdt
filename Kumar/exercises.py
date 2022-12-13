import LVDT_mag
import LVDT
import VC
import VConly
import simulation


b = [[24,'def3']]
sim_code = simulation.Femm_simulation(sensor_type=LVDT_mag, input=b)
sim_code.execute()