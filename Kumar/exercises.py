import sys
sys.path.append('./modules/')
import femm_simulation

c = {'steps_size_offset':[[10, 1, -5]]}  #[[no.of steps, step size, initial offset]]
c1 = [2, 1, -1]
sim_code = femm_simulation.Position_sesnor(save=False, sim_range={'steps_size_offset':[c1]},
                                data = {'filename(s)':["tr_6m"], 'is default':['no'], 'design or parameter':[5]})
sim_code.vc()




#b = [['A_def_extend', 'yes', 'A']]  #[[file name:str, default design check:str, design type:str/design parameter:float]]