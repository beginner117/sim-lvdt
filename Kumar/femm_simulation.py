import modules.basic as basic
import modules.LVDT as LVDT
import modules.VC as VC
#import modules.basic
class lvdt():
    def __init__(self, save, sim_range, default, data):
        self.save = save
        self.sim_range = sim_range
        self.default = default
        self.data = data

        for i in range(len(self.data)):
            if self.default=='yes':
                a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default = self.default, filename = self.data[i][0], design_type = self.data[i][1])
                a.simulate()
            else:
                a = LVDT.Analysis(self.save, sim_range=self.sim_range[i], default = self.default, filename = self.data[i][0], design_type=None,  parameter1 = self.data[i][1])
                a.simulate()

class vc():
    def __init__(self,save, sim_range, default, data):
        self.save = save
        self.sim_range = sim_range
        self.default = default
        self.data = data

        for i in range(len(self.data)):
            if self.default=='yes':
                a = VC.Analysis(self.save, sim_range=self.sim_range[i], default = self.default, filename = self.data[i][0], design_type = self.data[i][1])
                a.simulate()
            else:
                a = VC.Analysis(self.save, sim_range=self.sim_range[i], default = self.default, filename = self.data[i][0], design_type=None,  parameter1 = self.data[i][1])
                a.simulate()

            




