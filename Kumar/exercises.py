#import modules.basic as basic
import femm_simulation

b = [['def11', 'G']]
c = [[10, 0.5, -2.5]]
sim_code = femm_simulation.lvdt(save=False, sim_range=c, default = 'yes', data = b)


