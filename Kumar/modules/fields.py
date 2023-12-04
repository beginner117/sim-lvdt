import femm
import design
import femm_model
import coil
import feed
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import threading

class Coil_magfield:

    def __init__(self, radius, coil_height, current, turns_pr_layer, layers, insulated_wire_thickness, position,r_offset, upper_uppend=None,lower_uppend = None, angle=0, freq = 0):
        self.upper_uppend = upper_uppend
        self.lower_uppend = lower_uppend
        self.r_offset = r_offset
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
        #def_force = [];imp_force = [];rot_x = [];rot_y = []
        emf_tot_upp = []; emf_tot_low = []
        for item in range(0, self.layers):
            emf_layer_u = []; emf_layer_l = []; int_vec_u = []; int_vec_l = []
            threads1 = []; threads2 = []
            for j in range(0, self.turns_pr_layer):
                grid_pt = [self.radius + (self.wire*(item+1)), (self.position + (self.coil / 2)) - (j * self.wire)]
                grid_upp = [np.real(self.radius + (self.wire * (item + 1))), np.real((self.upper_uppend) - (j * self.wire))]
                grid_low = [np.real(self.radius + (self.wire * (item + 1))), np.real((self.lower_uppend) - (j * self.wire))]
                # print(grid_pt[0])
                # print(type(grid_pt[0]))
                b_field = femm.mo_getb(grid_pt[0], grid_pt[1])
                b_field_upp = femm.mo_getb(grid_upp[0], grid_upp[1])
                b_field_low = femm.mo_getb(grid_low[0], grid_low[1])

                #dtheta = 0.1
                inter = 180/0.1
                res = coil.Coil_prop(int(inter))
                uppout_prop = res.uppout()
                lowout_prop = res.lowout()
                #thet = []; b_vec_u = []; b_vec_l=[]; r_v = []

                f_upp = lambda r,theta : r*np.real(femm.mo_getb(r, (self.upper_uppend) - (j * self.wire)))[1]
                f_low = lambda r,theta : r*np.real(femm.mo_getb(r, (self.lower_uppend) - (j * self.wire)))[1]
                print(type(f_upp))
                # t1 = threading.Thread(target=integrate.dblquad, args = [f_upp, 0, np.pi, lambda theta: 0,
                #                   lambda theta: self.r_offset*np.cos(theta) + np.sqrt(self.radius**2 + (self.r_offset*np.sin(theta))**2)])
                # t1.start()
                # threads1.append(t1)
                # t2 = threading.Thread(target=integrate.dblquad, args = [f_low, 0, np.pi, lambda theta: 0,
                #                   lambda theta: self.r_offset * np.cos(theta) + np.sqrt(self.radius ** 2 + (self.r_offset * np.sin(theta)) ** 2)])
                # t2.start()
                # threads2.append(t2)
                flux_induced_upp = 2*integrate.dblquad((f_upp), 0, np.pi, lambda theta: 0,
                                  lambda theta: self.r_offset*np.cos(theta) + np.sqrt(self.radius**2 + (self.r_offset*np.sin(theta))**2))
                flux_induced_low = 2 * integrate.dblquad((f_low), 0, np.pi, lambda theta: 0,
                                  lambda theta: self.r_offset * np.cos(theta) + np.sqrt(self.radius ** 2 + (self.r_offset * np.sin(theta)) ** 2))
                emf_layer_u.append(flux_induced_upp[0])
                emf_layer_l.append(flux_induced_low[0])

                gri_x.append(grid_pt[0])
                gri_y.append(grid_pt[1])
                mag_fie_x.append(b_field[0])
                mag_fie_y.append(b_field[1])

            print('up:', emf_layer_u, '\nlow :', emf_layer_l)
            emf_tot_upp.append(sum(emf_layer_u))
            emf_tot_low.append(sum(emf_layer_l))

            # print('up:', threads1, '\nlow :', threads2)
            # emf_tot_upp.append(sum(threads1))
            # emf_tot_low.append(sum(threads2))
        print([sum(emf_tot_upp), sum(emf_tot_low)])
        return [sum(emf_tot_upp), sum(emf_tot_low)]

    def forces(self, mag_len, mag_dia, current):
        gri_x = [];mag_fie_x = [];mag_fie_y = [];gri_y = []
        def_force = [];imp_force = [];rot_x = [];rot_y = [];math_model_force = []
        for item in range(0, self.layers):
            for j in range(0, self.turns_pr_layer):
                grid_pt = [self.radius+(self.wire*(item+1)), (self.position+(self.coil/2))-(j*self.wire)]
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

                # def func(rad, theta1):
                #     p1 = mag_len / 2 - grid_pt[1]
                #     p2 = mag_len / 2 + grid_pt[1]
                #     fis = (2 * rad * (grid_pt[0] - rad * np.cos(theta1))) / 2 * (
                #             (rad ** 2) + (p1 ** 2) + (grid_pt[0] ** 2) - (
                #             2 * rad * grid_pt[0] * np.cos(theta1))) ** 1.5
                #     sec = (2 * rad * (grid_pt[0] - rad * np.cos(theta1))) / 2 * (
                #             (rad ** 2) + (p2 ** 2) + (grid_pt[0] ** 2) - (
                #             2 * rad * grid_pt[0] * np.cos(theta1))) ** 1.5
                #     return sec - fis
                #
                # res = integrate.dblquad(func, 0, mag_dia / 2, 0, 2 * np.pi)
                # v1 = (res[0] * mu_o * m * 0.25 / np.pi) / 10 ** 8
                # v11 = 2 * np.pi * grid_pt[0] * v1 * current / 1000
                # math_model_force.append(v11)
        #print('default force :', sum(def_force), 'updated force:', sum(imp_force))
        return [sum(def_force), sum(imp_force)]


# turns_per_layer = int(position.upp_outcoil()[3])
# analytical = fields.Coil_magfield(radius=geo.outcoil()[1], position=uppout_prop['UppOut_position'][i],
#                                   coil_height=geo.outcoil()[0], current=sensor.para()[2],
#                                   turns_pr_layer=int(position.upp_outcoil()[3]), layers=geo.outcoil()[2],
#                                   insulated_wire_thickness=(wire.prop_out()[0] + 2 * wire.prop_out()[1]), angle=0)
# if self.sim_type == 'FEMM+ana':
#     force_an = analytical.forces(geo.mag()[0], geo.mag()[1], sensor.para()[2])
#     for_def.append(force_an[0])
#     for_imp.append(force_an[1])
#     print('default force:', force_an[0], 'updated force:', force_an[1])
# if self.sim_type == 'math+ana':
#     force_an = analytical.forces(geo.mag()[0], geo.mag()[1], sensor.para()[2])
#     for_ana.append(force_an[2])
#     print('analytical force:', sum(force_an[2]))



# for k in range(0, int(inter)+1):
                #     thet.append(k*dtheta)
                #     r_vec = np.real(self.r_offset*np.cos(thet[k]) + np.sqrt(self.radius**2 + (self.r_offset*np.sin(thet[k]))**2) + self.wire*(item+1))
                #     uppout_prop['UppOut_flux'][k] = femm.mo_getb(grid_upp[0], grid_upp[1])[1]
                #     lowout_prop['LowOut_flux'][k] = femm.mo_getb(grid_low[0], grid_low[1])[1]
                #     r_v.append(r_vec)
                #     #print('test',r_vec, np.real(uppout_prop['UppOut_flux'][k]))
                # int_vec_u.append(np.trapz(r_v*np.real(uppout_prop['UppOut_flux']), dx = 0.1))
                # int_vec_l.append(np.trapz(r_v*np.real(lowout_prop['LowOut_flux']), dx = 0.1))
                # a1 =  2*np.trapz(int_vec_u, dx = dtheta)
                # a2 = 2 * np.trapz(int_vec_l, dx=dtheta)
                # emf_layer_u.append(a1); emf_layer_l.append(a2)


                #r_max = self.r_offset*np.cos(theta) + np.sqrt(self.radius**2 + (self.r_offset*np.sin(theta))**2)

                # f1 = lambda y, x: y
                # print(type(f1))
                # f2 = integrate.dblquad(f1, 0, 1, lambda x: x, lambda x: 2 - x)
                # print('f2 :', f2)