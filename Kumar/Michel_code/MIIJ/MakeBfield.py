import LVDT_mag
# import LVDT
# import VC
# import VConly
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import integrate
from scipy.optimize import curve_fit
import femm
import feed
import femm_simulation
import design
import os
from multiprocessing import Process


# pass lvdt object as argument to functions such that the function
# can get the geometry of the lvdt out of the lvdt object
# e.g. compute_voltage_diff(self, z_max, filename, lvdt_design):


def make_b_field(z_max, dz, r_max, dr, filename):
    """Makes the B field for a new configuration and saves it to the file
    """
    # Simulate 1 lvdt configuration in femm
    field_sim = LVDT_mag.Analysis(n_steps=0, inncoil_offset=0)
    field_sim.simulate()
    # Use the get_b_field function to acquire and store the B field data
    compute_b_field(r_max, dr, z_max, dz, '../dataMap/bFields/' + filename)


def make_b_field2(z_max, dz, r_max, dr, lvdt_type, filename):
    """Makes the B field for a new configuration and saves it to the specified filename. Lvdt_type is the name of the
    design from the feed.py script (e.g. 'A'). Data is saved as B[T]; x,y,z[mm]."""
    # Simulate 1 LVDT configuration in FEMM
    sim_code = femm_simulation.Position_sensor(False, sim_range={'steps_size_offset': [[0, 0, 0]]},
                                               data={'filename(s)': [filename], 'is default': ['yes'],
                                                     'design or parameter': [lvdt_type]})
    sim_code.lvdt()
    # Use the get_b_field function to acquire and store the B field data
    compute_b_field(r_max, dr, z_max, dz, '../dataMap/bFields/' + filename)
    print('magnetic vector field saved: B[T], position[mm]')


def remove_inncoil_b_field(lvdt_type, load_filename, save_filename, wire_type: str = "32 AWG"):
    """Adjusts the specified magnetic field (load_filename) by removing the B field inside the coils of the
    innercoil itself. Lvdt_type is the name of the design from the feed.py script (e.g. 'A').
    Data is saved as B[T]; x,y,z[mm]."""
    r_vec, z_vec, b_mat_z, b_mat_r = get_b_field('../dataMap/bFields/' + load_filename, True)
    rv, zv = np.meshgrid(r_vec, z_vec)
    # Load dimensions of LVDT
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    # create boolean masks for radial direction
    mask_r = np.logical_and(rv >= dims['inn_rad'], rv <= dims['inn_rad'] + wire_tot * dims['inn_layers'])
    # create a boolean mask for the radial mask and take height of innercoil into account
    mask = np.logical_and(mask_r, zv <= dims['inn_ht'] * 0.5)
    # set the corresponding values in the B field to zero
    b_mat_z[mask] = 0
    b_mat_r[mask] = 0
    np.savez('../dataMap/bFields/' + save_filename, r_vec=r_vec, z_vec=z_vec, b_mat_z=b_mat_z, b_mat_r=b_mat_r)


def compute_asymm_flux(x_offset, d_theta, lvdt_type, load_filename, save_filename, radius=-5):
    """"Compute the flux phi(z) by integrating the circle inside the outer coils at every z gridpoint
    (0, z_max), the outer coil has an offset x_offset from the center of the inner coil in x the direction.
    The filename only requires the name of the file itself, the appropriate folder will be selected by the function,
    the load file determines the name from which B field file the data should be taken,
    save file determines name of flux data file. phi[T.m^2]; z[mm]
    """
    r_vec, z_vec, b_mat_z = get_b_field('../dataMap/bFields/' + load_filename)
    phi_vec = np.zeros(len(z_vec))
    # Load dimensions of LVDT
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    rad = dims["out_rad"]
    if radius > 0:
        rad = radius
    # Loop over all heights in z grid
    for i in range(0, len(z_vec)):
        phi_vec[i] = asymm_circle_flux_polar(x_offset, rad, d_theta, b_mat_z[i, :], r_vec)
    # Create the full phi_tot and z_tot vectors for the [-z_max, z_max] domain, by mirroring
    # the vectors in the [0, z_max] domain
    z_tot = np.concatenate((-np.flipud(z_vec[1:]), z_vec))
    # Introduce prefactor 1e-6 for conversion mm^2 -> m^2
    phi_tot = 1e-6 * np.concatenate((np.flipud(phi_vec[1:]), phi_vec))
    # save the phi_vec to the desired file
    np.savez('../dataMap/flux/' + save_filename, z_vec=z_tot, phi_vec=phi_tot)
    print('flux saved: phi[T.m^2]')


def compute_asymm_flux_layers(x_offset, d_theta, lvdt_type, load_filename, save_filename, wire_type: str = "32 AWG"):
    """Similar to the compute_asymm_flux() function, but looping over all outer coil layers and adding the flux
    of each layer to sum to the total flux.
    """
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    path = '../dataMap/flux/' + save_filename
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Created new directory")
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    phi_vec_list = []  # create list to store the phi_vec of each layer
    for i in range(0, dims['out_layers']):
        rad_i = dims['out_rad'] + i * wire_tot
        file_i = save_filename + '/layer' + str(i + 1)
        compute_asymm_flux(x_offset, d_theta, lvdt_type, load_filename, file_i, radius=rad_i)
        z_vec, phi_vec = get_phi_vec('../dataMap/flux/' + file_i)
        phi_vec_list.append(phi_vec)
        print('layer ' + str(i + 1) + ' finished')
    z_vec_save, phi_vec_dummy = get_phi_vec('../dataMap/flux/' + save_filename + '/layer1')
    np.savez('../dataMap/flux/' + save_filename + '_Tot', z_vec=z_vec_save, phi_vec=sum(phi_vec_list))
    print('flux saved: phi[T.m^2]')


def par_task(m, x_offset, d_theta, lvdt_type, load_filename, save_filename, out_rad, wire_tot):
        rad_i = out_rad + m * wire_tot
        file_i = save_filename + '/layer' + str(m + 1)
        compute_asymm_flux(x_offset, d_theta, lvdt_type, load_filename, file_i, radius=rad_i)
        print('layer ' + str(m + 1) + ' finished')


def compute_asymm_flux_layers_par(x_offset, d_theta, lvdt_type, load_filename, save_filename,
                                  wire_type: str = "32 AWG"):
    """Similar to the compute_asymm_flux_layers() function, but the looping over all outer coil layers is
    parallelized.
    """
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    path = '../dataMap/flux/' + save_filename # Path to folder in which the fluxdata of every layer will be stored
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Created new directory")
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    phi_vec_list = []  # create list to store the phi_vec of each layer
    # Start parallel processing the asymmetric flux computation
    processes = [Process(target=par_task, args=(m, x_offset, d_theta, lvdt_type, load_filename, save_filename,
                                                dims['out_rad'], wire_tot)) for m in range(dims['out_layers'])]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    for i in range(0, dims['out_layers']):
        file_i = save_filename + '/layer' + str(i + 1)
        z_vec, phi_vec = get_phi_vec('../dataMap/flux/' + file_i)
        phi_vec_list.append(phi_vec)
    z_vec_save, phi_vec_dummy = get_phi_vec('../dataMap/flux/' + save_filename + '/layer1')
    np.savez('../dataMap/flux/' + save_filename + '_Tot', z_vec=z_vec_save, phi_vec=sum(phi_vec_list))
    print('Total flux layers saved: phi[T.m^2]')


def compute_symm_flux(lvdt_type, load_filename, save_filename):
    """"Computes the flux inside a sphere with radius R, by integrating the B_z(r) field using the trapezoidal rule in
    2pi*int(r*B(z,r)). The filename only requires the name of the file itself, the appropriate folder will be
    selected by the function, the load file determines the name from which B field file the data should be taken,
    save file determines name of flux data file. phi[T.m^2]; z[mm]
    """
    r_vec, z_vec, b_mat_z = get_b_field('../dataMap/bFields/' + load_filename)
    phi_vec = np.zeros(len(z_vec))
    # Load dimensions of LVDT
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    # Loop over all heights in z grid
    for i in range(0, len(z_vec)):
        phi_vec[i] = symm_circle_flux(dims["out_rad"], b_mat_z[i, :], r_vec)
    # Create the full phi_tot and z_tot vectors for the [-z_max, z_max] domain, by mirroring
    # the vectors in the [0, z_max] domain
    z_tot = np.concatenate((-np.flipud(z_vec[1:]), z_vec))
    # Introduce prefactor 1e-6 for conversion mm^2 -> m^2
    phi_tot = 1e-6 * np.concatenate((np.flipud(phi_vec[1:]), phi_vec))
    # save the phi_vec to the desired file
    np.savez('../dataMap/flux/' + save_filename, z_vec=z_tot, phi_vec=phi_tot)
    print('flux saved in [T.m^2]')


def compute_voltages2(z_max, lvdt_type: str, load_filename: str, save_filename: str, wire_type: str = "32 AWG"):
    """Compute the induced voltages for different z positions of the inner coil compared to the outer coils
    in the domain: [lower boundary of lower coil = -z_max, upper boundary of upper coil = z_max]. The filename only
    requires the name of the file itself, the appropriate folder will be selected by the function"""
    z_vec, phi_vec = get_phi_vec('../dataMap/flux/' + load_filename)
    # Check if z_max has a usable value
    if z_max > z_vec[-1]:
        print("z_max should be smaller than the z domain of the flux vector")
        quit()
    # Find the lower boundary of the flux vector
    z_lower = z_vec[0]
    # Find the stepsize of the z vector
    dz = z_vec[1] - z_vec[0]
    # Load dimensions from LVDT type
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    out_dist = dims["out_dist"]
    out_ht = dims["out_ht"]
    # Load wire dimensions
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    # Find the indices for the domain of the coils
    z_n_min = round((-z_max - z_lower) / dz)
    z_n_max = round((z_max - z_lower - (out_dist + out_ht)) / dz)
    # Initialize induced voltage for lower and upper coil
    v_induced_low = np.zeros(round(z_n_max - z_n_min))
    v_induced_upp = v_induced_low
    # Loop over all positions of the outer coil compared to inner coil and compute the induced voltage in each coil
    # by integrating phi(z) over the respective coil height. Introduce prefactor 10e-6 for conversion mm^2 -> m^2
    for i in range(0, round(z_n_max - z_n_min)):
        v_induced_low[i] = np.sum(phi_vec[(z_n_min + i):(z_n_min + round(out_ht / dz) + i)]) * 10e-6
        v_induced_upp[i] = np.sum(phi_vec[(z_n_min + round(out_dist / dz) + i):(z_n_min + round((
                                                                                                        out_dist + out_ht) / dz) + i)]) * 10e-6
    # Create new appropriate z positions vector
    z_probed_low = -z_max + round((out_dist + out_ht) / 2)
    z_vec_new = np.linspace(z_probed_low, z_probed_low + round((z_n_max - z_n_min) * dz), z_n_max - z_n_min)
    print('saved voltages')
    np.savez('../dataMap/voltages/' + save_filename, z_vec=z_vec_new, v_low=v_induced_low, v_upp=v_induced_upp)


def compute_voltages_disc(z_max, lvdt_type: str, load_filename: str, save_filename: str, wire_type: str = "32 AWG"):
    """Compute the induced voltages for different z positions of the inner coil compared to the outer coils
    in the domain: [lower boundary of lower coil = -z_max, upper boundary of upper coil = z_max]. The filename only
    requires the name of the file itself, the appropriate folder will be selected by the function"""
    z_vec, phi_vec = get_phi_vec('../dataMap/flux/' + load_filename)
    print('length z vec', len(z_vec))
    # Check if z_max has a usable value
    if z_max > z_vec[-1]:
        print("z_max should be smaller than the z domain of the flux vector")
        quit()
    # Find the lower boundary of the flux vector
    z_lower = z_vec[0]
    # Find the stepsize of the z vector
    dz = z_vec[1] - z_vec[0]
    # Load dimensions from LVDT type
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    out_dist = dims["out_dist"]
    out_ht = dims["out_ht"]
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    # Find the indices for the domain of the coils
    z_n_min = round((-z_max - z_lower) / dz)  # min n for the bottom of the lower outer coil
    # print('z_n_min:', z_vec[z_n_min])
    # print('z top', z_vec[round((z_max-z_lower)/dz)])
    z_n_max = round((z_max - z_lower - (out_dist + out_ht)) / dz)  # max n for the bottom of the lower outer coil
    # print('z_n_max:', z_vec[z_n_max])
    # Initialize induced voltage for lower and upper coil
    v_induced_low = np.zeros(round(z_n_max - z_n_min) + 1)
    v_induced_upp = v_induced_low
    # Loop over all positions of the outer coil compared to inner coil and compute the induced voltage in each coil
    # by integrating phi(z) over the respective coil height. Introduce prefactor omega = 2*pi*f = 2*pi*1e4
    print("number of windings computed: ")
    print(len(phi_vec[(z_n_min + round(wire_tot / (2 * dz))):
                      (z_n_min + round((out_ht - wire_tot / 2) / dz) + 1):round(wire_tot / dz)]))
    for i in range(0, round(z_n_max - z_n_min) + 1):
        v_induced_low[i] = np.sum(phi_vec[(z_n_min + round(wire_tot / (2 * dz)) + i):
                                          (z_n_min + round((out_ht - wire_tot / 2) / dz) + i + 1):round(
            wire_tot / dz)]) * 2 * np.pi * 1e4
        v_induced_upp[i] = np.sum(phi_vec[(z_n_min + round((out_dist + wire_tot / 2) / dz) + i):(z_n_min
                                                                                                 + round(
                    (out_dist + out_ht - wire_tot / 2) / dz) + i + 1):round(wire_tot / dz)]) * 2 * np.pi * 1e4
    # Create new appropriate z positions vector for the position of the center of the inner coil
    # z_probed_low = -z_max + round((out_dist/2 + out_ht))
    # z_probed_low = -z_max + out_dist - out_ht/2
    # print('min:', z_n_min)
    # print('max:', z_n_max)
    # change this into dz step of 0.1
    z_vec_new = z_vec[z_n_min:z_n_max + 1] + (out_dist + out_ht) / 2
    # z_vec_new = np.linspace(-round(0.5*(z_n_max - z_n_min) * dz), round(0.5*(z_n_max - z_n_min) * dz), z_n_max - z_n_min)
    # z_vec_new = np.linspace(z_probed_low, 27, z_n_max - z_n_min)
    # z_vec_new = np.arange(z_probed_low, -z_probed_low, dz)
    print('saved voltages')
    np.savez('../dataMap/voltages/' + save_filename, z_vec=z_vec_new, v_low=v_induced_low, v_upp=v_induced_upp)


def compute_voltages_cont(z_max, lvdt_type: str, load_filename: str, save_filename: str, wire_type: str = "32 AWG"):
    """Compute the induced voltages for different z positions of the inner coil compared to the outer coils
    in the domain: [lower boundary of lower coil = -z_max, upper boundary of upper coil = z_max]. The filename only
    requires the name of the file itself, the appropriate folder will be selected by the function"""
    z_vec, phi_vec = get_phi_vec('../dataMap/flux/' + load_filename)
    # Check if z_max has a usable value
    if z_max > z_vec[-1]:
        print("z_max should be smaller than the z domain of the flux vector")
        quit()
    # Find the lower boundary of the flux vector
    z_lower = z_vec[0]
    # Find the stepsize of the z vector
    dz = z_vec[1] - z_vec[0]
    # Load dimensions from LVDT type
    dim_obj = feed.Input()
    dims = dim_obj.return_data(lvdt_type)  # Example type "F"
    out_dist = dims["out_dist"]
    out_ht = dims["out_ht"]
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    N_wind_perLayer = out_ht / wire_tot
    print(*['Windings per layer outer coil: ', N_wind_perLayer])
    # Find the indices for the domain of the coils
    z_n_min = round((-z_max - z_lower) / dz)
    z_n_max = round((z_max - z_lower - (out_dist + out_ht)) / dz)
    # Initialize induced voltage for lower and upper coil
    v_induced_low = np.zeros(round(z_n_max - z_n_min))
    v_induced_upp = v_induced_low
    # Loop over all positions of the outer coil compared to inner coil and compute the induced voltage in each coil
    # by integrating phi(z) over the respective coil height. Introduce prefactor omega = 2*pi*f = 2*pi*1e4
    for i in range(0, round(z_n_max - z_n_min)):
        phi_vec_low_i = phi_vec[(z_n_min + i):(z_n_min + round(out_ht / dz) + i)]
        phi_vec_upp_i = phi_vec[(z_n_min + round(out_dist / dz) + i):(z_n_min + round((out_dist + out_ht) / dz) + i)]
        v_induced_low[i] = np.sum(phi_vec_low_i) * (N_wind_perLayer / len(phi_vec_low_i)) * 2 * np.pi * 1e4
        v_induced_upp[i] = np.sum(phi_vec_upp_i) * (N_wind_perLayer / len(phi_vec_upp_i)) * 2 * np.pi * 1e4
    # Create new appropriate z positions vector
    z_probed_low = -z_max + round((out_dist + out_ht) / 2)
    z_vec_new = np.linspace(z_probed_low, z_probed_low + round((z_n_max - z_n_min) * dz), z_n_max - z_n_min)
    print('saved voltages')
    np.savez('../dataMap/voltages/' + save_filename, z_vec=z_vec_new, v_low=v_induced_low, v_upp=v_induced_upp)


def plot_b_gradient(filename: str, logplot: bool = False, quiverplot: bool = True, n_quiver_r: int = 15,
                    n_quiver_z: int = 15, coil_type: str = None, wire_type: str = "32 AWG", eps_x=0.5, eps_y=0.5):
    """Plots the gradient of the B field grid, specify which kind of plots to be shown by setting 'logplot' and 'quiverplot' to
    True/False. The number of gridpoints between each vector with n_quiver_r (or _z) can also be adjusted. By specifying
    an LVDT design (i.e. 'F') in the coil_type argument, the positions of the inner and outer coil will be shown."""
    r_vec, z_vec, b_mat_z, b_mat_r = return_b_field(filename, True)
    z_tot = np.concatenate((-np.flipud(z_vec[1:]), z_vec))
    # matrices are rotated or something, gradient doesnt seem correct
    b_mat_z_tot = np.concatenate((np.flipud(b_mat_z[1:, :]), b_mat_z), axis=0)
    b_mat_r_tot = np.concatenate((-np.flipud(b_mat_r[1:, :]), b_mat_r), axis=0)
    rv, zv = np.meshgrid(r_vec, z_tot)
    dz = z_tot[1] - z_tot[0]
    dr = r_vec[1] - r_vec[0]
    # compute the gradient of the B field
    grad_r, grad_z = np.gradient(np.sqrt(np.real(b_mat_r_tot) ** 2 + np.real(b_mat_z_tot) ** 2), dr, dz)
    grad_tot = np.sqrt(grad_r ** 2 + grad_z ** 2)
    # Load dimensions from LVDT type
    dim_obj = feed.Input()
    dims = dim_obj.return_data(coil_type)  # Example type "F"
    out_dist = dims['out_dist']
    out_ht = dims['out_ht']
    # Load wire dimensions and compute total wire width (taking into account insulation)
    wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
    wire_width, wire_ins = wire.prop_out()[0:2]
    wire_tot = wire_width + 2 * wire_ins
    InnCoil_LowEnd = (dims['inn_dist'] - dims['inn_ht']) / 2
    InnCoil_OutRadius = dims['inn_rad'] + wire_tot * dims['inn_layers']
    InnCoil_UppEnd = InnCoil_LowEnd + dims['inn_ht']
    # eliminate the diverging gradient inside the inner coil
    grad_tot_masked = ma.masked_where(
        (rv > dims['inn_rad'] - eps_x) & (rv < InnCoil_OutRadius + eps_x) & (zv > InnCoil_LowEnd - eps_y) & (
                zv < InnCoil_UppEnd + eps_y), grad_tot)
    grad_r_masked = ma.masked_where(
        (rv > dims['inn_rad'] - eps_x) & (rv < InnCoil_OutRadius + eps_x) & (zv > InnCoil_LowEnd - eps_y) & (
                zv < InnCoil_UppEnd + eps_y), grad_r)
    grad_z_masked = ma.masked_where(
        (rv > dims['inn_rad'] - eps_x) & (rv < InnCoil_OutRadius + eps_x) & (zv > InnCoil_LowEnd - eps_y) & (
                zv < InnCoil_UppEnd + eps_y), grad_z)

    if logplot:
        'Scaling of colorbar is not correct yet'
        fig1, ax2 = plt.subplots(layout='constrained')
        CS = ax2.contourf(rv, zv, np.log(grad_tot_masked / np.amax(grad_tot_masked)), cmap='jet')
        cbar = fig1.colorbar(CS)
        cbar.ax.set_ylabel(r'$log(|\nabla B/\nabla B_{max}|)$')
    else:
        fig1, ax2 = plt.subplots(layout='constrained')
        CS = ax2.contourf(rv, zv, grad_tot_masked / np.amax(grad_tot_masked), cmap='jet')
        cbar = fig1.colorbar(CS)
        cbar.ax.set_ylabel(r'$|\nabla B/\nabla B_{max}|$')
    if quiverplot:
        rows = np.arange(0, len(z_tot), n_quiver_z)
        cols = np.arange(0, len(r_vec), n_quiver_r)
        # normalize all vectors for a clearer plot
        grad_r_norm = grad_r / grad_tot
        grad_z_norm = grad_z / grad_tot
        plt.quiver(rv[rows, :][:, cols], zv[rows, :][:, cols], grad_r_norm[rows, :][:, cols],
                   grad_z_norm[rows, :][:, cols], cmap='plasma')
    if coil_type:
        # plot the emitting coil as a rectangle
        plt.gca().add_patch(
            (Rectangle((dims['inn_rad'], (dims['inn_dist'] - dims['inn_ht']) / 2), wire_tot * dims['inn_layers']
                       , dims['inn_ht'], edgecolor='blue', facecolor='none', lw=2)))
        # plot the receiving coils as rectangles
        plt.gca().add_patch((Rectangle((dims['out_rad'], (dims['out_dist'] - dims["out_ht"]) / 2),
                                       wire_tot * dims['out_layers'], dims["out_ht"], edgecolor='red',
                                       facecolor='none', lw=2)))
        plt.gca().add_patch((Rectangle((dims['out_rad'], -(dims['out_dist'] + dims['out_ht']) / 2),
                                       wire_tot * dims['out_layers'], dims['out_ht'], edgecolor='red',
                                       facecolor='none', lw=2)))


def plot_b_field(filename: str, contourplot: bool = True, quiverplot: bool = True, n_quiver_r: int = 15,
                 n_quiver_z: int = 15, coil_type: str = None, wire_type: str = "32 AWG", contour_norm=False, shift_z=0):
    """Plots the B field grid, specify which kind of plots to be shown by setting 'contourplot' and 'quiverplot' to
    True/False. The number of gridpoints between each vector with n_quiver_r (or _z) can also be adjusted. By specifying
    an LVDT design (i.e. 'F') in the coil_type argument, the positions of the inner and outer coil will be shown."""
    r_vec, z_vec, b_mat_z, b_mat_r = return_b_field(filename, True)
    z_tot = np.concatenate((-np.flipud(z_vec[1:]), z_vec))
    b_mat_z_tot = np.concatenate((np.flipud(b_mat_z[1:, :]), b_mat_z), axis=0)
    b_mat_r_tot = np.concatenate((-np.flipud(b_mat_r[1:, :]), b_mat_r), axis=0)
    rv, zv = np.meshgrid(r_vec, z_tot)
    b_tot = np.sqrt(b_mat_z_tot ** 2 + b_mat_r_tot ** 2)
    if contour_norm:
        'Scaling of colorbar is not correct yet'
        fig1, ax2 = plt.subplots(layout='constrained')
        CS = ax2.contourf(rv, zv, b_tot / np.amax(b_tot), cmap='jet')
        cbar = fig1.colorbar(CS)
        cbar.ax.set_ylabel(r'$|B/B_{max}|$')
        contourplot = False
    if contourplot:
        'Scaling of colorbar is not correct yet'
        fig1, ax2 = plt.subplots(layout='constrained')
        CS = ax2.contourf(rv, zv, b_tot, cmap='jet')
        cbar = fig1.colorbar(CS)
        cbar.ax.set_ylabel('|B| [T]')
    if quiverplot:
        rows = np.arange(0, len(z_tot), n_quiver_z)
        cols = np.arange(0, len(r_vec), n_quiver_r)
        # normalize all vectors for a clearer plot
        b_mat_r_norm = b_mat_r_tot / b_tot
        b_mat_z_norm = b_mat_z_tot / b_tot
        plt.quiver(rv[rows, :][:, cols], zv[rows, :][:, cols], b_mat_r_norm[rows, :][:, cols],
                   b_mat_z_norm[rows, :][:, cols], cmap='plasma')
    if coil_type:
        # Load dimensions from LVDT type
        dim_obj = feed.Input()
        dims = dim_obj.return_data(coil_type)  # Example type "F"
        out_dist = dims['out_dist']
        out_ht = dims['out_ht']
        # Load wire dimensions and compute total wire width (taking into account insulation)
        wire = design.Wiretype(outcoil_material=wire_type, inncoil_material=wire_type)  # Example wire type "32 AWG"
        wire_width, wire_ins = wire.prop_out()[0:2]
        wire_tot = wire_width + 2 * wire_ins
        # plot the emitting coil as a rectangle
        plt.gca().add_patch(
            (Rectangle((dims['inn_rad'], (dims['inn_dist'] - dims['inn_ht']) / 2), wire_tot * dims['inn_layers']
                       , dims['inn_ht'], edgecolor='blue', facecolor='none', lw=2)))
        # plot the receiving coils as rectangles
        plt.gca().add_patch((Rectangle((dims['out_rad'], 0.5 * (dims['out_dist'] - dims["out_ht"]) + shift_z),
                                       wire_tot * dims['out_layers'], dims["out_ht"], edgecolor='red',
                                       facecolor='none', lw=2)))
        plt.gca().add_patch((Rectangle((dims['out_rad'], -0.5 * (dims['out_dist'] + dims['out_ht']) + shift_z),
                                       wire_tot * dims['out_layers'], dims['out_ht'], edgecolor='red',
                                       facecolor='none', lw=2)))


def return_b_field(filename: str, b_z_component: bool = False):
    """"Returns r_vec, z_vec, b_mat(z,r)_z and b_mat(z,r)_r if specified"""
    return get_b_field('../dataMap/bFields/' + filename, b_z_component)


def return_flux_vec(filename: str):
    """"Returns z_vec, and phi_vec(z)"""
    return get_phi_vec('../dataMap/flux/' + filename)


def return_voltage_vec(filename: str):
    """"Returns z_vec, v_low vector and v_upp vector"""
    return get_voltage_vec('../dataMap/voltages/' + filename)


# --------------------------------------------------------------------------------------------------------------------#
# General functions


# Function which can be put after femm simulation and puts the magnetic field B_z(r,z) as a matrix in file
def compute_b_field(r_max, dr, z_max, dz, filename):
    """"Writes matrix of z components of the magnetic field and r and z position vectors
    to the filename
    """
    # Construct the position vectors and flux
    r_vec = np.arange(0, r_max + dr, dr, dtype=np.double)
    z_vec = np.arange(0, z_max + dz, dz, dtype=np.double)  # z_vec will be mirrored about z=0 later on

    # Construct the matrix of B field vectors (B_r,B_z)
    b_mat_vec = np.zeros((len(z_vec), len(r_vec), 2), dtype=np.double).astype(complex)
    # Compute the B field in the r,z-plane
    for i in range(0, len(z_vec)):
        for j in range(0, len(r_vec)):
            b_mat_vec[i, j, :] = femm.mo_getb(r_vec[j], z_vec[i])
    # Matrix of B(r,z) field with only z components (index: 1): only relevant data for flux computation
    b_mat_z = np.real(b_mat_vec[:, :, 1])
    # Matrix of B(r,z) field with only r components (index: 0)
    b_mat_r = np.real(b_mat_vec[:, :, 0])
    # Save data to the specified file
    np.savez(filename, r_vec=r_vec, z_vec=z_vec, b_mat_z=b_mat_z, b_mat_r=b_mat_r)


def indx_closest(arr, value):
    return np.absolute(arr - value).argmin()


def moving_average(arr, window_size):
    """Computes a moving average for the arr array, averaging over window_size number of elements (uneven number).
    The length of the returned arr is (window_size-1)/2 elements shorter than the argument arr by cutting of the ends
     of the array."""
    # Initialize an empty list to store moving averages
    moving_averages = np.zeros(len(arr) - window_size + 1)
    # Perform the averages
    for i in range(0, len(arr) - window_size + 1):
        moving_averages[i] = np.average(arr[i:i + window_size])
    return moving_averages


def fit_slope(arr_x, arr_y, x_min, x_max, error: bool = False, eps=0.1, returnF: bool = False):
    """Performs a linear fit over the data (arr_x, arr_y) in the range [x_min, x_max] and returns the slope. Setting returnF to True
    will not only return the slope but also the function p(x). The error option will return the deviation from linearity
    of the data from the performed linear fit.
    """
    indx_min = indx_closest(arr_x, x_min) # Look for the value in arr_x closest to x_min
    indx_max = indx_closest(arr_x, x_max) # Look for the value in arr_x closest to x_max
    x = arr_x[indx_min:indx_max]
    y = arr_y[indx_min:indx_max]
    param = np.polyfit(x, y, 1)
    if error:
        p = np.poly1d(param)
        err = (p(x[np.absolute(x) > eps]) - y[np.absolute(x) > eps]) / abs(y[np.absolute(x) > eps])
        plt.plot(x[np.absolute(x) > eps], err, 'o-')
    if returnF:
        p = np.poly1d(param)
        print("the fitted slope m: " + str(param[0]))
        return p, param[0]
    print("the fitted slope m: " + str(param[0]))
    return param[0]


def fit_slope_dev(arr_x, arr_y, x_min, x_max, dev, returnF: bool = False):
    indx_min = indx_closest(arr_x, x_min)
    indx_max = indx_closest(arr_x, x_max)
    x = arr_x[indx_min:indx_max]
    y = arr_y[indx_min:indx_max]
    x_vec = []
    y_vec = []
    for j in range(len(x)):
        x_vec.append(x[j])
        y_vec.append(y[j])

    def lin_f(x, slope, intercept):
        y = intercept + slope * x
        return y

    param, cov= curve_fit(lin_f, x_vec, y_vec, sigma=dev, absolute_sigma=True)
    if returnF:
        p = np.poly1d(param)
        print("the fitted slope m: " + str(param[0]))
        return p, param[0], cov
    print("the fitted slope m: " + str(param[0]))
    return param[0]


def get_b_field(filename, b_z_component: bool = False):
    """"Returns r_vec, z_vec, b_mat(z,r)_z and b_mat(z,r)_r if specified"""
    b_field_data = np.load(filename + '.npz')
    if b_z_component:
        return b_field_data["r_vec"], b_field_data["z_vec"], b_field_data["b_mat_z"], b_field_data["b_mat_r"]
    else:
        return b_field_data["r_vec"], b_field_data["z_vec"], b_field_data["b_mat_z"]


def get_phi_vec(filename):
    """"Returns the data necessary to plot the phi(z) flux"""
    flux_data = np.load(filename + '.npz')
    return flux_data["z_vec"], flux_data["phi_vec"]


def get_voltage_vec(filename):
    """"Returns the data necessary to plot the phi(z) flux"""
    voltage_data = np.load(filename + '.npz')
    return voltage_data["z_vec"], voltage_data["v_low"], voltage_data["v_upp"]


def asymm_circle_flux(a, R, dy, b_z_r_vec, r_vec):
    """"Computes the magnetic field inside a sphere with radius R, grid stepsize dy and offset a in the x direction from the center of the
    innercoil by integrating the B_z(r) field using the trapezoidal rule"""
    dr = r_vec[1]  # Determines the stepsize of r direction
    n_y = np.floor(R / dy)  # Number of grid points in the y direction
    int_vec = np.zeros(n_y + 1)  # Initialize integral vector
    # Loop over all y heights smaller than R
    for i in range(0, n_y + 1):
        # Create the positive x part of the B field vector
        b_vec_right = b_z_r_vec[(r_vec < a + np.sqrt(R ** 2 - (i * dy) ** 2)) & (r_vec >= i * dy)]
        # Create the negative x part of the B field vector
        b_vec_left = b_vec_right[r_vec < np.abs(a - np.sqrt(R ** 2 - (i * dy) ** 2))]
        # Put vectors behind each other (concatenate) and remove first element (r=0) from negative x part, such that
        # the total B vector has only one B(r=0) entry
        b_vec_total = np.concatenate(np.flip(b_vec_left[1:]), b_vec_right)
        # Integrate the B field in the x direction and add it to the integral vector
        int_vec[i] = np.trapz(b_vec_total, dx=dr)
    # Integrate the B field along the y direction and multiply by 2 since the integral is only computed for positive y
    return 2 * np.trapz(int_vec, dx=dy)


def asymm_circle_flux_polar(a, R, d_theta, b_z_r_vec, r_vec):
    """"Computes the magnetic flux inside a circle with radius R, angular stepsize d_theta and offset a in the x direction from the center of the
    innercoil by integrating the B_z(r) field using the trapezoidal rule"""
    dr = r_vec[1]  # Determines the stepsize of r direction
    if R > r_vec[-1]:
        print("The radius R should be smaller than the r domain of the magnetic field data")
        quit()
    n_theta = round(np.floor(np.pi / d_theta))  # Number of grid points for the theta coordinate
    int_vec = np.zeros(n_theta + 1)  # Initialize integral vector
    # Loop over all angles (theta = i*d_theta) smaller than pi
    for i in range(0, n_theta + 1):
        # Create the B field vector and r vector for the given angle theta
        b_vec_i = b_z_r_vec[r_vec < a * np.cos(i * d_theta) + np.sqrt(R ** 2 - (a * np.sin(i * d_theta)) ** 2)]
        r_vec_i = r_vec[r_vec < a * np.cos(i * d_theta) + np.sqrt(R ** 2 - (a * np.sin(i * d_theta)) ** 2)]
        # Integrate the B field in the r coordinate with differential rdr in polar coordinates
        int_vec[i] = np.trapz(r_vec_i * b_vec_i, dx=dr)
        # int_vec[i] = integrate.simpson(r_vec_i*b_vec_i, dx=dr)
    # Integrate the B field in the theta coordinate and multiply by 2 since the integral is only computed for positive y
    # return 2*integrate.simpson(int_vec, dx=d_theta)
    return 2 * np.trapz(int_vec, dx=d_theta)


def symm_circle_flux(R, b_z_r_vec, r_vec):
    """"Computes the magnetic field inside a sphere with radius R,
     by integrating the B_z(r) field using the trapezoidal rule in 2pi*int(r*B(z,r))"""
    dr = r_vec[1]  # Determines the stepsize of r direction
    # Integrate the B field in the theta coordinate and multiply by 2 since the integral is only computed for positive y
    b_vec_new = b_z_r_vec[r_vec < R]
    r_vec_new = r_vec[r_vec < R]
    # return 2*integrate.simpson(int_vec, dx=d_theta)
    return 2 * np.pi * integrate.simpson(r_vec_new * b_vec_new, dx=dr)
