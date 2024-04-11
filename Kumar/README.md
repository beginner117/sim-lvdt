
This repository contains the modules with FEMM code to simulate the LVDTs & VCs in general and some customized modules to simulate the preliminary NIKHEF designs.
Here we are using the pyFEMM package to interface the FEMM functions with python to easily simulate, analyse the results without the need for software like Labview. FEMM is only available on Windows operating systems the repository python code will only work on Windows systems with FEMM installed.

Below, you will find some short instructions on how to install the software. 

    Install the FEMM software on your Windows machine: https://www.femm.info/wiki/HomePage Go to download page and follow instructions.
    Assuming you have a working python 3 environment, install pyFEMM: https://www.femm.info/wiki/pyFEMM. You can do this with pip via: pip install pyfemm. On the linked page you can also find the pyFEMM manual.

Here is the list of modules:

    feed.py - contains the dimensions of preliminary NIKHEF designs and wire types used
    design.py - contains all the classes that returns the coil geometry
    coil.py - contains all the classes that returns coil properties  
    femm_model.py - contains the classes that models the coils, magnets in FEMM
    fields.py - contains the classes that calculates the magnetic fields, voltages, forces by numerical methods (using the field information from FEMM)
    LVDT.py - contains the script that simulates a typical LVDT used in pathfinder
    VC.py - contains the script that simulates a typical VC used in pathfinder
    VC_only.py - contains the script that simulates a typical VC-only used in pathfinder
    YOKE.py - contains the script that simulates a complicated YOKE structure used in pathfinder
    LVDT_mutual_inductance.py - contains the script that calculates the mutual inductance between the coils of the LVDT
    LVDT_correction.py - contains the script that calculates the correction factor (needed due to open circuit simulation in FEMM) of LVDT response  
    femm_simulation.py - contains all the methods that call and execute LVDT and VC simulations using FEMM
    analytical_simulation - contains all the methods that call and execute LVDT and VC simulations analytically
    single_coil.py - models a single coil

Here is a explanation for simulating a typical LVDT/VC with just two lines. One can simulate one or more sensors simultaneously

(Import the script 'FEMM_simulation' and make sure pyFEMM in installed)

    sim_code = femm_simulation.Position_sensor(sensor_type=, save=, sim_range={'steps_size_offset':},
                                    data = {'filename(s)':, 'is default':, 'design or parameter':})

    sim_code.execute()

    ______INPUT_______
    sensor_type = list with names of sensors that should be simulated
    save = 'True' to save all the simulated files or 'False' to not save the files
    sim_range = list containg a list (nested list) of total steps, grid size and offset
    filename(s) = name(s) of the simulated file(s) 
    is default = 'yes' if the simulation is for a preliminary NIKHEF designs and 'no' if not
    (NOTE - if analysis is not for a default design, go to the '.py' file of the specific sensor (for instance, LVDT.py or VC.py), 
     a line after, "if self.default == 'no':", modify the parameter that you want to change as 'self.parameter1')
    design or parameter = list with design type (if 'is default' is 'yes') or parameter (if 'is default is 'no')
    _______OUTPUT______
    saves all the data along with the simulation parameters in a .npz file (if the save argument above is True)
OPTIONAL


    mat_prop = list containing (i) inner coil material (ii) outer coil material (iii) magnet material
    simulation_type = list with strings 'semi_analytical' for analytical calculation.

Here are the default assumptions

    wire material - 32 AWG
    magnet type - N40
    Inner coil excitation (for LVDT) - 10Khz, 20mA sinusoidal wave
    Outer coil excitation (for VC, VC_only) - 1A DC sinusoidal wave
    Units - millimeters
    precision - 1.0e-10
            Boundary conditions 
    material - Air
    Region 1, mesh - sphere with radius 100mm, 
    Region 2, mesh - sphere with radius 300mm, auto mesh
    #For analytical calculations:

NOTE - To modify any of the above parameters, alter the code in the respective modules. 
For chainging the coil excitations and the boundary conditions of LVDT/VC/VC_only, modify the instance 'sensor' and 'bc', and to change the units and precisions, modify the command 'mi_probdef' in the corresponding LVDT/VC.py script 
For changing the wire, magnet material modify the instance 'wire' in the corresponding LVDT/VC.py script and add this material to the 'prop_inn', 'prop_out' & 'mag_mat' methods of 'Wiretype' class in the design.py module. 
(Make sure the modified material is available in the FEMM material library. If not, the new material must be defined with all the properties in the classes 'FEMM_coil' and 'FEMM_magnet' of the 'femm_model.py' module.)
    

For a better understanding, a model code to simulate LVDTs is given in 'example.md' file. Please go through that.   