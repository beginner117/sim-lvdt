
lis = []
class Femm_simulation():
    def __init__(self, sensor_type, input=None):
        self.sensor_type = sensor_type
        self.input = input
    def execute(self):
        for item in self.input:
            print(item)
            try:
                a = self.sensor_type.Analysis(item[0], item[1], item[2])
            except:
                a = self.sensor_type.Analysis(item[0], item[1])
            a.simulate()
            




