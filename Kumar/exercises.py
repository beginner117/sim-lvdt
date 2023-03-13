import sys
sys.path.append('./modules/')
import femm_simulation



c = {'steps_size_offset':[[10, 1, -5]]}  #[[no.of steps, step size, initial offset]]
c1 = [10, 1, -5]
sim_code = femm_simulation.Position_sensor(save=False, sim_range={'steps_size_offset':[c1]},
                                data = {'filename(s)':["type_F_40mm"], 'is default':['yes'], 'design or parameter':['A']})
sim_code.vc()




#b = [['A_def_extend', 'yes', 'A']]  #[[file name:str, default design check:str, design type:str/design parameter:float]]