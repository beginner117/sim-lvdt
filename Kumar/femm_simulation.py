import sys
#sys.path.append('./modules/basic/')
sys.path.append('./modules/')
import modules.LVDT as LVDT
import modules.VC as VC
import modules.VC_only as VC_only
import modules.YOKE as YOKE

class Position_sensor:
    def __init__(self, sensor_type, save, sim_range, data):
        self.sensor_type = sensor_type
        self.save = save
        self.sim_range = sim_range
        self.data = data
    def execute(self):
        for i in range(len(self.sensor_type)):
            if self.sensor_type[i] == 'LVDT':
                    if self.data['is default'][i] == 'yes':
                        # a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default=self.data[i][1], filename=self.data[i][0], design_type=self.data[i][2])
                        a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                          default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                          design_type=self.data['design or parameter'][i])
                        a.simulate()
                    else:
                        # a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default=self.data[i][1], filename=self.data[i][0], design_type=None, parameter1=self.data[i][2])
                        a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                          default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                          design_type=None, parameter1=self.data['design or parameter'][i])
                        a.simulate()
            if self.sensor_type[i] == 'VC':
                    if self.data['is default'][i] == 'yes':
                        a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                        default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                        design_type=self.data['design or parameter'][i])
                        a.simulate()
                    else:
                        a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                        default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                        design_type=None, parameter1=self.data['design or parameter'][i])
                        a.simulate()
            if self.sensor_type[i] == 'VC_only':
                    if self.data['is default'][i] == 'yes':
                        a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                             default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                             design_type=self.data['design or parameter'][i])
                        a.simulate()
                    else:
                        a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i],
                                             default=self.data['is default'][i], filename=self.data['filename(s)'][i],
                                             design_type=None, parameter1=self.data['design or parameter'][i])
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


    def lvdt(self):
        for i in range(len(self.data['filename(s)'])):
            #if self.data[i][1] == 'yes':
            if self.data['is default'][i] == 'yes':
                #a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default=self.data[i][1], filename=self.data[i][0], design_type=self.data[i][2])
                a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=self.data['design or parameter'][i])
                a.simulate()
            else:
                #a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default=self.data[i][1], filename=self.data[i][0], design_type=None, parameter1=self.data[i][2])
                a = LVDT.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=None, parameter1=self.data['design or parameter'][i])
                a.simulate()
    def vc(self):
        for i in range(len(self.data['filename(s)'])):
            if self.data['is default'][i] == 'yes':
                a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=self.data['design or parameter'][i])
                a.simulate()
            else:
                a = VC.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=None, parameter1=self.data['design or parameter'][i])
                a.simulate()

    def vc_only(self):
        for i in range(len(self.data['filename(s)'])):
            if self.data['is default'][i] == 'yes':
                a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=self.data['design or parameter'][i])
                a.simulate()
            else:
                a = VC_only.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=None, parameter1=self.data['design or parameter'][i])
                a.simulate()

    def yoke(self):
        for i in range(len(self.data['filename(s)'])):
            if self.data['is default'][i] == 'yes':
                a = YOKE.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=self.data['design or parameter'][i])
                a.simulate()
            else:
                a = YOKE.Analysis(self.save, sim_range=self.sim_range['steps_size_offset'][i], default=self.data['is default'][i], filename=self.data['filename(s)'][i], design_type=None, parameter1=self.data['design or parameter'][i])
                a.simulate()



            




