Example (for three simultaneous simulations of LVDT, VC, VC_only)

    import femm_simulation
    import sys
    sys.path.append('path to the directory containing all the modules above')

    sim_code = femm_simulation.Position_sensor(sensor_type=['LVDT', 'VC', 'VC_only'], save=False, sim_range={'steps_size_offset':[[20, 1, -10], [10, 1, -5], [20, 1, -10]]},
                                    data = {'filename(s)':['trail1', 'trial2', 'trail3'], 'is default':['yes', 'no', 'yes'], 'design or parameter':['A', 3, 'I']})
    sim_code.execute() 

Example to compute the mutual inductances of the coils

    import femm_simulation
    import sys
    sys.path.append('path to the directory containing all the modules above')

    sim_code = femm_simulation.Position_sensor(sensor_type=['LVDT_mutual_inductance', 'LVDT_mutual_inductance'], save=False, sim_range={'steps_size_offset':[[20, 1, -10], [20, 1, -10]]},
                                    data = {'filename(s)':['trail1', 'trial2'], 'is default':['yes', 'no'], 'design or parameter':['A', 3]})
    sim_code.execute()

Example to compute the correction factor of the coils

    import femm_simulation
    import sys
    sys.path.append('path to the directory containing all the modules above')

    sim_code = femm_simulation.Position_sensor(sensor_type=['LVDT_corrected', 'LVDT_corrected'], save=False, sim_range={'steps_size_offset':[0, 0]]},
                                    data = {'filename(s)':['trail1', 'trial2'], 'is default':['yes', 'no'], 'design or parameter':['A', 3]})
    sim_code.execute()

Example to compute the voltages, forces numerically