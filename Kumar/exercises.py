import LVDT_mag
import LVDT
import VC
import VConly
import simulation

c = '10mm_0.1step_volnormalisation_51fit_typeA1'
b = [[24,'1']]
sim_code = simulation.Femm_simulation(sensor_type=LVDT_mag, input=b)
sim_code.execute()