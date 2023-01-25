#import modules.basic as basic
import sys
sys.path.append('./modules/')
import femm_simulation


b = [['defA', 'A']]  #[[file name:str, default design type:str]], [[file name:str, parameter:float]]
c = [[20, 0.5, -5]] #[[no.of steps, step size, initial offset]]
sim_code = femm_simulation.lvdt(save=True, sim_range=c, default = 'yes', data = b)


