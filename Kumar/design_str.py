import pandas as pd
from pandas import Series, DataFrame
import modules.basic.feed


ip1 = modules.basic.feed.Input()
class Values():
    def __init__(self, design_type):
        self.design_type = design_type
        self.height = {"inner": [self.design_type['inn_ht']], 'upper_out': [self.design_type['out_ht']], 'lower_out': [self.design_type['out_ht']]}
        self.radius = {"inner": [self.design_type['inn_rad']], 'upper_out': [self.design_type['out_rad']], 'lower_out': [self.design_type['out_rad']]}
        self.layers = {"inner": [self.design_type['inn_layers']], 'upper_out': [self.design_type['out_layers']], 'lower_out': [self.design_type['out_layers']]}
        self.mag = {"length":[self.design_type['mag_len']], 'diameter':[self.design_type['mag_dia']], 'ver_shift':[self.design_type['ver_shi']]}
        self.distance = {"inner": [self.design_type['inn_dist']], 'outer': [self.design_type['out_dist']]}
    def coil_height(self):
        """
        returns the height of inner, upper_outer, lower_outer coils
        """
        frame_h = pd.DataFrame(self.height)
        return frame_h
    def coil_radius(self):
        """
        returns the radius of inner, upper_outer, lower_outer coils
        """
        frame_r = pd.DataFrame(self.radius)
        return frame_r
    def coil_layers(self):
        """
        returns the number of layers for of inner, upper_outer, lower_outer coils
        """
        frame_l = pd.DataFrame(self.layers)
        return frame_l
    def magnet(self):
        """
        returns the diameter and length of magnet
        """
        frame_m = pd.DataFrame(self.mag)
        return frame_m
    def coil_distance(self):
        """
        returns the distance between the midpoint of coils
        """
        frame_d = pd.DataFrame(self.distance)
        return frame_d



