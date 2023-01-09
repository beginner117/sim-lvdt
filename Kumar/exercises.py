#import modules.basic as basic
import sys
sys.path.append('./modules/')
import femm_simulation


b = [['def11', 'G']]  #[[file name, default design type]], [[file name, parameter]]
c = [[10, 0.5, -2.5]] #[[no.of steps, step size, initial offset]]
sim_code = femm_simulation.lvdt(save=False, sim_range=c, default = 'yes', data = b)


