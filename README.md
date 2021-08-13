This repository contains FEMM code to simulate LVDT and VC systems. It is based on the code developed by F. Schimmel at Nikhef. In this case we are using the pyFEMM package to interface the FEMM functions with python. This way we can use python files and notebooks to easily simulate, analyse and plot the results without the need for software like Labview. Unfortunately, as FEMM is only available on Windows operating systems the repository python code will only work on Windows systems with FEMM installed.

Update: latest pyFEMM version seems to imply it now also works on Linux and Mac systems by using FEMM with Wine.

Below you will find some short instruction on how to install and setup the software. This content is under construction.

1. Install the FEMM software on your Windows machine: https://www.femm.info/wiki/HomePage
Go to download page and follow instructions.

2. Assuming you have a working python 3 environment, install pyFEMM: https://www.femm.info/wiki/pyFEMM
You can do this with pip via: pip install pyfemm.
On the linked page you can also find the pyFEMM manual.

3. Clone this repository on your local computer to get access to all jupyter notebooks.

More info on the notebooks:

- LVDT_Position_ETpf_LIP.ipynb: This will simulate the classic (inner coil excited) LVDT position measurement with a geometry implemented as intended for the ETpathfinder large IP.
- LVDT_Position_ETpf_LIP_Plot.ipynb: Allows to read in results from previous notebook and make more plots comparing different simulations.

- RevLVDT_Position_ETpf_LIP.ipynb: This will simulate the reversed (outer coils excited) LVDT position measurement with a geometry implemented as intended for the ETpathfinder large IP.
- RevLVDT_Position_ETpf_LIP_Plot.ipynb: Allows to read in results from previous notebook and make more plots comparing different simulations.

- RevLVDT_VC_ETpf_LIP.ipynb: This will simulate the VC action of the same (Rev)LVDT geometry as implemented for ETpathfinder large IP. It uses DC current FEMM simulations instead of AC current for the LVDT position simulation.
- RevLVDT_VC_ETpf_LIP_Plot.ipynb: Allows to read in results from previous notebook and make more plots comparing different simulations.

Every notebook has some general parameters, geometry specific parameters etc. 
One can change the simulation parameters but keep the geometry the same.
Or one can change the geometry and keep simulation parameters.
Still a lot of work and improvements can be done.

Currently basic results can reproduce those from F. Schimmel's original code.
But one should still explore different implementations in pyFEMM to see what is going on, and what can be more efficient.

At some point one should see if this can also be moved to simulations in Matlab or another software program with better capabilities. 
It is said that the CoreCoil LVDT concept can not (is it?) be simulated with FEMM.




