# BG_Modelling

To run the model:

Compile the MOD files by running:
`nrnivmodl` in the terminal.

Run test_simulation.py to see behaviour of model STN cells and GPe cells.

STN cell as defined by: T. Otsuka, T. Abe, T. Tsukagawa, and W.-J. Song, “Conductance-Based Model of the
Voltage-Dependent Generation of a Plateau Potential in Subthalamic Neurons,” J
Neurophysiol, vol. 92, no. 1, pp. 255–264, Jul. 2004, doi: 10.1152/jn.00508.2003

GPe cell as defined by: A. Nambu and R. Llinas, “Electrophysiology of globus pallidus neurons in vitro,” J
Neurophysiol, vol. 72, no. 3, pp. 1127–1139, Sep. 1994, doi:
10.1152/jn.1994.72.3.1127.

Run network.py to generate DBS signal, record STN LFP and plot Seaborn heatmaps/differential LFP recording.
Run rasters.py to plot STN or GPe rasters.
