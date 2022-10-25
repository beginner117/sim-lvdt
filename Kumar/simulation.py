
lis = []
class Femm_simulation():
    def __init__(self, sensor_type, input=None):
        self.sensor_type = sensor_type
        self.input = input
    def execute(self):
        for item in self.input:
            print(item)
            a = self.sensor_type.Analysis(item[0], item[1])
            lis.append(a)
        for item in lis:
            item.simulate()
            




