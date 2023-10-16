
This repository contains the modules with FEMM code to simulate the LVDTs & VCs in general and some customized modules to simulate the preliminary NIKHEF designs.
Here we are using the pyFEMM package to interface the FEMM functions with python to easily simulate, analyse the results without the need for software like Labview. FEMM is only available on Windows operating systems the repository python code will only work on Windows systems with FEMM installed.

Below, you will find some short instructions on how to install the software. 

    Install the FEMM software on your Windows machine: https://www.femm.info/wiki/HomePage Go to download page and follow instructions.
    Assuming you have a working python 3 environment, install pyFEMM: https://www.femm.info/wiki/pyFEMM. You can do this with pip via: pip install pyfemm. On the linked page you can also find the pyFEMM manual.

Here is the list of modules 
    feed.py - contains the dimensions of preliminary NIKHEF designs
    design.py - contains all the classes that returns the coil geometry
    coil.py - contains all the classes that returns coil properties  
    femm_model.py - contains the script that models the coil in FEMM
    fields.py - contains the script that calculates the magnetic fields of the coils
    LVDT.py - contains the script that simulates a typical LVDT used in pathfinder
    VC.py - contains the script that simulates a typical VC used in pathfinder
    VC_only.py - contains the script that simulates a typical VC-only used in pathfinder
    YOKE.py - contains the script that simulates a complicated YOKE structure used in pathfinder
    LVDT_mutual_inductance.py - contains the script that calculates the mutual inductance between the coils of the LVDT
    LVDT_correction.py - contains the script that calculates the correction factor (needed due to open circuit simulation in FEMM) of LVDT response  
    

Here is a working example for simulating a typical LVDT/VC with just two lines. One can simulate one or more sensors simultaneously
(Import the script 'FEMM_simulation' and make sure pyFEMM in installed)

    sim_code = femm_simulation.Position_sensor(sensor_type=, save=, sim_range={'steps_size_offset':},
                                    data = {'filename(s)':, 'is default':, 'design or parameter':})

    sim_code.execute()

    """
        ______INPUT_______
        sensor_type = list with names of sensors that should be simulated
        save = 'True' to save all the simulated files or 'False' to not save the files
        sim_range = list containg a list (nested list) of total steps, grid size and offset
        filename(s) = name(s) of the simulated file(s) 
        is default = 'yes' if the simulation is for a preliminary NIKHEF designs and 'no' if not
        design or parameter = list with design type (if 'is default' is 'yes') or parameter (if 'is default is 'no')
    """

Example (for two simultaneous simulations of LVDT and VC)

    import femm_simulation
    import sys
    sys.path.append('path to the directory containing all the modules above')

    sim_code = femm_simulation.Position_sensor(sensor_type=[LVDT, VC], save=False, sim_range={'steps_size_offset':[[20, 1, -10], [10, 1, -5]]},
                                    data = {'filename(s)':['trail1', 'trial2'], 'is default':['yes', 'no'], 'design or parameter':['A', 3]})
    sim_code.execute() 
    
