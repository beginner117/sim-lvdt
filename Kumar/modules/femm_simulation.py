import sys
sys.path.append('./modules/')

import LVDT as LVDT
import VC as VC
import VC_only as VC_only
import YOKE as YOKE
import VC_fields as VC_fields
import LVDT_correction as LVDT_correction
import LVDT_mutual_inductance as LVDT_mutual_inductance
import importlib

class Position_sensor:
    """"
    defining the parameters of the simulation (and the sensor) within specified range
    _____INPUT____
    sensor_type - type of the position sensor to be simulated (string)
    save        - whether to save the simulated data or not(boolean)
    sim_range   - required simulation range. A list of length 3 containing (i)total simulations points (ii)step size (iii)offset/lower limit of the moving coil
    data        - name of the file, whether the simulating design is default NIKHEF design or not, type/parameter of the design
    mat_prop*    - list of materials used (inner coil material, outer coil material, magnet material) in simulation
    simulation*  -  type of the simulation, femm or semi analytic (string)
    (The last two arguments are optional. The default assumptions are '32 AWG' wire and 'N40' magnet with femm simulation type)
    """
    def __init__(self, sensor_type, save, sim_range, data, mat_prop=None, simulation=None):
        self.sensor_type = sensor_type
        self.save = save
        self.sim_range = sim_range
        self.data = data
        self.material_prop = mat_prop if mat_prop is not None else ['32 AWG', '32 AWG', 'N40']
        self.simulation_type = [simulation]*len(sensor_type)
        # if self.mat_prop:
        #     self.material_prop = mat_prop
        # if not self.mat_prop:
        #     self.material_prop = ['32 AWG', '32 AWG', 'N40']
    def execute(self, input_current = None):
        """"
        executes the simulation with above defined parameters"""
        for i in range(len(self.sensor_type)):
            if self.sensor_type[i] == 'LVDT':
                excitation = input_current if input_current is not None else [0.02, 10000, 0]
                if self.data['is default'][i] == 'yes':
                    a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i], input_excitation=excitation,
                                      design_type=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], simulation_type=self.simulation_type[i])
                    a.simulate()
                else:
                    a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                      design_type=None, materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], parameter1=self.data['design or parameter'][i], simulation_type=self.simulation_type[i])
                    a.simulate()
            if self.sensor_type[i] == 'VC':
                excitation = input_current if input_current is not None else [0, 0, 1]
                if self.data['is default'][i] == 'yes':

                    a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                    default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                    design_type=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], simulation_type=self.simulation_type[i])
                    a.simulate()
                else:
                    a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                    default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                    design_type=None,materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], parameter1=self.data['design or parameter'][i], simulation_type=self.simulation_type[i])
                    a.simulate()
            if self.sensor_type[i] == 'VC_only':
                excitation = input_current if input_current is not None else [0, 0, 1]
                if self.data['is default'][i] == 'yes':
                    a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                         default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                         design_type=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]])
                    a.simulate()
                else:
                    a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                         default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                         design_type=None, parameter1=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]])
                    a.simulate()
            if self.sensor_type[i] == 'LVDT with yoke':
                if self.data['is default'][i] == 'yes':
                    a = YOKE.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                      design_type=self.data['design or parameter'][i])
                    a.simulate()
                else:
                    a = YOKE.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                      design_type=None, parameter1=self.data['design or parameter'][i])
                    a.simulate()

            if self.sensor_type[i] == 'VC_fields':
                excitation = input_current if input_current is not None else [0, 0, 1]
                print('vc_analytical')
                if self.data['is default'][i] == 'yes':
                    a = VC_fields.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],input_excitation=excitation,
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                      design_type=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]])
                    a.simulate()
                else:
                    a = VC_fields.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                      default=self.data['is default'][i], filename=self.data['filename(s)'][i],input_excitation=excitation,
                                      design_type=None,materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], parameter1=self.data['design or parameter'][i])
                    a.simulate()

            if self.sensor_type[i] == 'LVDT_corrected':
                excitation = input_current if input_current is not None else [0.02, 10000, 0]
                if self.data['is default'][i] == 'yes':
                    a1 = LVDT_correction.Analysis(save = self.save, default=self.data['is default'][i], offset=self.sim_range['steps_size_offset'][i],
                                       design=self.data['design or parameter'][i], materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], filename=self.data['filename(s)'][i])
                    a1.simulate()
                else:
                    a1 = LVDT_correction.Analysis(save = self.save, default=self.data['is default'][i], offset=self.sim_range['steps_size_offset'][i],
                                       design=None, materials =[self.material_prop[0], self.material_prop[1], self.material_prop[2]],  filename=self.data['filename(s)'][i], parameter=self.data['design or parameter'][i])
                    a1.simulate()
            if self.sensor_type[i] == 'LVDT_mutual_inductance':
                excitation = input_current if input_current is not None else [0.02, 10000, 0]
                if self.data['is default'][i] == 'yes':
                    a1 = LVDT_mutual_inductance.Analysis1(save = self.save, default=self.data['is default'][i], offset=self.sim_range['steps_size_offset'][i],
                                       design_type=self.data['design or parameter'][i],materials1 =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], filename1=self.data['filename(s)'][i])
                    a1.simulate()
                else:
                    a1 = LVDT_mutual_inductance.Analysis1(save = self.save, default=self.data['is default'][i], offset=self.sim_range['steps_size_offset'][i],
                                        design_type=None,materials1 =[self.material_prop[0], self.material_prop[1], self.material_prop[2]], filename1=self.data['filename(s)'][i], parameter1=self.data['design or parameter'][i])
                    a1.simulate()



            




