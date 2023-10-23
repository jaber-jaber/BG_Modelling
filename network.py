from neuron import h, gui
from neuron.units import ms, mV, sec
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from LFPsimpy import LfpElectrode
from output import mem_potentials, plotmap, raster_plot
from DBS import generate_DBS_signal
from point_source import calculate_distances, compute_transfer_resistance
import pickle

h.load_file("stdrun.hoc")
h.load_file("LFPsimpy-master/LFPsimpy-master/LFPsimpy/LFPsimpy.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 3000 * ms
h.dt = 0.01

N = 100 # Num of STN cells in the network.
SSC_network = Network(N)
stncells = SSC_network.stn_cells1
gpecells = SSC_network.gpe_cells

# Uncomment to open GUI and show cell network.
# ps = h.PlotShape(True)
# ps.show(0)
# ps.color(2, sec=stncells[int(N/2)].soma)

midcell = stncells[int(N/2)]
midpoint = (midcell.soma.x3d(0) + stncells[49].soma.x3d(0))/2

# To save all recorded cell activity in array to create heatmap.
# pot_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in stncells]
# gpe_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in gpecells]

# Compute 'r' in DBS signal.
list_electrodes, list_cells = calculate_distances(45, 55)
ptsrc = compute_transfer_resistance(list_electrodes, list_cells)

stim_vecs = []
signals = []

# DBS Parameters
start = 1000
stop = h.tstop
dt = h.dt
amp = 2.5
freq = 330
pw = 0.06
offset = 0

""" Generating different DBS signals with amplitude depending on r."""
for pt in ptsrc:
    DBS, DBS_times = generate_DBS_signal(start, stop, dt, amp, freq, pw, offset, pt)
    signals.append([DBS, DBS_times])

for n, cell in enumerate(stncells):
    sig_vec = h.Vector().from_python(signals[n][0])
    stim_vec = sig_vec.play(cell.stim, cell.stim._ref_amp, h.dt)
    stim_vecs.append(stim_vec)


# Define two electrodes for differential LFP recording.
c1_electrode = LfpElectrode(x=0, y=0, z=100, sampling_period=0.1, method="Point")
c2_electrode = LfpElectrode(x=0, y=0, z=100, sampling_period=0.1, method="Point")

# Initialize all cells with the same membrane potential.
h.finitialize(h.v_init)
h.run(h.tstop)

# Calculate differential LFP recording.
diff_recording = [a - b for a, b in zip(c2_electrode.values, c1_electrode.values)]

# Uncomment to generate np array of membrane potentials for heatmap.
# pots = mem_potentials(pot_vecs)
# gpe_pots = mem_potentials(gpe_vecs)

# Uncomment to view heatmap.
# plotmap(pots, t)
