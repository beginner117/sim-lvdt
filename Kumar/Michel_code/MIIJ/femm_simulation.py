import sys
sys.path.append('./modules/basic/')
import LVDT
import VC
import VC_only
import YOKE

class Position_sensor:
    def __init__(self, save, sim_range, data):
        self.save = save
        self.sim_range = sim_range
        self.data = data
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



            




