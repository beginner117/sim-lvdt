import sys
sys.path.append('./modules/')
import femm_simulation



 #[[no.of steps, step size, initial offset]]

saveall = []
input = {'sensor_type' : ['VC_only'], 'SaveFile' : False,
            'file_names' : [ "tr4"],
            'default_design' : ['yes'],
            'type_or_parameter' : ['H'],
            'TotalSteps_StepSize_Offset' : [ [6, 1, -1]]}


sim_code = femm_simulation.Position_sensor(sensor_type = input['sensor_type'], save=input['SaveFile'], sim_range={'steps_size_offset':input['TotalSteps_StepSize_Offset']},
                                data = {'filename(s)':input['file_names'], 'is default':input['default_design'], 'design or parameter':input['type_or_parameter']})
sim_code.execute()



#b = [['A_def_extend', 'yes', 'A']]  #[[file name:str, default design check:str, design type:str/design parameter:float]]