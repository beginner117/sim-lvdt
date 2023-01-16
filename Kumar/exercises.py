#import modules.basic as basic
import sys
sys.path.append('./modules/')
import femm_simulation


b = [['def_f', 'F']]  #[[file name:str, default design type:str]], [[file name:str, parameter:float]]
c = [[20, 0.25, -2.5]] #[[no.of steps, step size, initial offset]]
sim_code = femm_simulation.lvdt(save=False, sim_range=c, default = 'yes', data = b)


