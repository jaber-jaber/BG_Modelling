from neuron import h, gui
from neuron.units import ms, mV, sec
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from output import plotmap, raster_plot
from DBS import generate_DBS_signal
from point_source import calculate_distances, compute_transfer_resistance
import pickle

""" Run to produce rasters of N STN and GPe cells. """

h.load_file("stdrun.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 1000 * ms
h.dt = 0.01

N = 100
Ngpe = N * 3

SSC_network = Network(N)
stncells = SSC_network.stn_cells1
gpecells = SSC_network.gpe_cells

stn_Firing = raster_plot(stncells)
gpe_Firing = raster_plot(gpecells)

t = h.Vector().record(h._ref_t)

list_electrodes, list_cells = calculate_distances(45, 55)
ptsrc = compute_transfer_resistance(list_electrodes, list_cells)

stim_vecs = []
signals = []

# DBS Parameters
start = 0
stop = h.tstop
dt = h.dt
amp = 2.5
freq = 130
pw = 0.06
offset = 0

for pt in ptsrc:
    DBS, DBS_times = generate_DBS_signal(start, stop, dt, amp, freq, pw, offset, pt)
    signals.append([DBS, DBS_times])

for n, cell in enumerate(stncells):
    sig_vec = h.Vector().from_python(signals[n][0])
    stim_vec = sig_vec.play(cell.stim, cell.stim._ref_amp, h.dt)
    stim_vecs.append(stim_vec)

cmap_colors = ['white', 'black']
my_cmap = LinearSegmentedColormap.from_list('my_cmap', cmap_colors)

h.finitialize(h.v_init)
h.continuerun(h.tstop)

num_time_bins = 1000
stn_spike_times_binary = np.zeros((N, num_time_bins))
gpe_spike_times_binary = np.zeros((Ngpe, num_time_bins))

for i, neuron_spike_times in enumerate(stn_Firing):
    for spike_time in neuron_spike_times:
        time_bin = int(spike_time)
        if time_bin < num_time_bins:
            stn_spike_times_binary[i, time_bin] = 1

for i, j in enumerate(gpe_Firing):
    for spike_time in j:
        gpe_time_bin = int(spike_time)
        if gpe_time_bin < num_time_bins:
            gpe_spike_times_binary[i, gpe_time_bin] = 1

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(stn_spike_times_binary, cmap=my_cmap, aspect='auto')
ax2.imshow(gpe_spike_times_binary, cmap=my_cmap, aspect='auto')

ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Neuron')
ax1.set_title('STN Rasters')

ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Neuron')
ax2.set_title('GPe Rasters')

plt.show()