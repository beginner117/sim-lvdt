import sys
sys.path.append('./modules/')
import femm_simulation

#[[no.of steps, step size, initial offset]]

input_para = {'sensor_type' : ['VC_fields'], 'SaveFile' : False,
            'file_names' : ['tr1'],
            'default_design' : ['no'],
            'type_or_parameter_OR_angle' : [0],
            'TotalSteps_StepSize_Offset_OR_offset' : [[0, 1, 0]]}

sim_code = femm_simulation.Position_sensor(sensor_type = input_para['sensor_type'], save=input_para['SaveFile'], sim_range={'steps_size_offset':input_para['TotalSteps_StepSize_Offset_OR_offset']},
                                data = {'filename(s)':input_para['file_names'], 'is default':input_para['default_design'], 'design or parameter':input_para['type_or_parameter_OR_angle']})

sim_code.execute()
