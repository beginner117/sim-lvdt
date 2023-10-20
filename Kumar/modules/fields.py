import femm
import design
import femm_model
import coil
import feed
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

class Coil_magfield:

    def __init__(self, radius, position, coil_height, current, turns_pr_layer, layers, insulated_wire_thickness,angle=0, freq = 0 ):
        self.radius = radius
        self.position = position
        self.turns_pr_layer = turns_pr_layer
        self.layers = layers
        self.wire = insulated_wire_thickness
        self.coil = coil_height
        self.current = current
        self.angle = angle
        self.freq = freq
        #self.res = res

    def mag_fields(self):
        gri_x = []; mag_fie_x = [];mag_fie_y = [];gri_y = []
        def_force = [];imp_force = [];rot_x = [];rot_y = [];math_model_force = []
        for item in range(0, self.layers):
            for j in range(0, self.turns_pr_layer):
                grid_pt = [self.radius + self.wire, (self.position + (self.coil / 2)) - (j * self.wire)]
                # print(grid_pt[0])
                # print(type(grid_pt[0]))
                b_field = femm.mo_getb(grid_pt[0], grid_pt[1])
                gri_x.append(grid_pt[0])
                gri_y.append(grid_pt[1])
                mag_fie_x.append(b_field[0])
                mag_fie_y.append(b_field[1])

    def forces(self, mag_len, mag_dia, current):
        gri_x = [];mag_fie_x = [];mag_fie_y = [];gri_y = []
        def_force = [];imp_force = [];rot_x = [];rot_y = [];math_model_force = []
        for item in range(0, self.layers):
            for j in range(0, self.turns_pr_layer):
                grid_pt = [self.radius+self.wire, (self.position+(self.coil/2))-(j*self.wire)]
                #print(grid_pt[0])
                #print(type(grid_pt[0]))
                b_field = femm.mo_getb(grid_pt[0], grid_pt[1])
                gri_x.append(grid_pt[0])
                gri_y.append(grid_pt[1])
                mag_fie_x.append(b_field[0])
                mag_fie_y.append(b_field[1])

                g = (2*np.pi*grid_pt[0]*self.current*b_field[0])/1000
                def_force.append(g)
                theta = (self.angle/180)*np.pi
                rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                c = np.dot(rotMatrix, np.array(b_field))
                rot_x.append(c[0])
                rot_y.append(c[1])
                f = (2*np.pi*c[0]*self.current*b_field[0])/1000
                imp_force.append(f)

                mu_o = 1.256 * (10 ** -6)
                m = 969969

                def func(rad, theta1):
                    p1 = mag_len / 2 - grid_pt[1]
                    p2 = mag_len / 2 + grid_pt[1]
                    fis = (2 * rad * (grid_pt[0] - rad * np.cos(theta1))) / 2 * (
                            (rad ** 2) + (p1 ** 2) + (grid_pt[0] ** 2) - (
                            2 * rad * grid_pt[0] * np.cos(theta1))) ** 1.5
                    sec = (2 * rad * (grid_pt[0] - rad * np.cos(theta1))) / 2 * (
                            (rad ** 2) + (p2 ** 2) + (grid_pt[0] ** 2) - (
                            2 * rad * grid_pt[0] * np.cos(theta1))) ** 1.5
                    return sec - fis

                res = integrate.dblquad(func, 0, mag_dia / 2, 0, 2 * np.pi)
                v1 = (res[0] * mu_o * m * 0.25 / np.pi) / 10 ** 8
                v11 = 2 * np.pi * grid_pt[0] * v1 * current / 1000
                math_model_force.append(v11)
        #print('default force :', sum(def_force), 'updated force:', sum(imp_force))
        return [sum(def_force), sum(imp_force), sum(math_model_force)]




