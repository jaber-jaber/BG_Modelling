from neuron import h, gui
from neuron.units import ms, mV, sec
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from LFPsimpy import LfpElectrode
from output import mem_potentials, plotmap
from DBS import generate_DBS_signal
from point_source import calculate_distances, compute_transfer_resistance
import pickle

h.load_file("stdrun.hoc")
h.load_file("LFPsimpy-master/LFPsimpy-master/LFPsimpy/LFPsimpy.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 5000 * ms
h.dt = 0.01

N = 100
SSC_network = Network(N)
stncells = SSC_network.stn_cells1
gpecells = SSC_network.gpe_cells

testval = 50

gpe1 = SSC_network.gpe_cells[testval]
stn1 = stncells[testval]
# stim = h.IClamp(test1.soma(0.5))
# stim.delay = 3000 * ms
# stim.dur = 2000 * ms
# stim.amp = -10e-3
t = h.Vector().record(h._ref_t)
volstn1 = h.Vector().record(stn1.soma(0.5)._ref_v)
volgpe1 = h.Vector().record(gpe1.soma(0.5)._ref_v)
# ps = h.PlotShape(True)
# ps.show(0)
# ps.color(2, sec=stncells[int(N/2)].soma)

midcell = stncells[int(N/2)]
midpoint = (midcell.soma.x3d(0) + stncells[49].soma.x3d(0))/2
c1_pos = midpoint - 3000
c2_pos = midpoint + 3000

list_electrodes, list_cells = calculate_distances(45, 55)
ptsrc = compute_transfer_resistance(list_electrodes, list_cells)

stim_vecs = []
signals = []

# DBS Parameters
start = 1000
stop = h.tstop
dt = h.dt
amp = 2.5
freq = 250
pw = 0.06
offset = 0

for pt in ptsrc:
    DBS, DBS_times = generate_DBS_signal(start, stop, dt, amp, freq, pw, offset, pt)
    signals.append([DBS, DBS_times])

for n, cell in enumerate(stncells):
    sig_vec = h.Vector().from_python(signals[n][0])
    stim_vec = sig_vec.play(cell.stim, cell.stim._ref_amp, h.dt)
    stim_vecs.append(stim_vec)

test_DBS = signals[50][0]
test_DBS_times = signals[50][1]
# pot_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in stncells]
# gpe_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in gpecells]
c1_electrode = LfpElectrode(x=c1_pos, y=0, z=0, sampling_period=0.01, method="Point")
c2_electrode = LfpElectrode(x=c2_pos, y=0, z=0, sampling_period=0.01, method="Point")

h.finitialize(h.v_init)
h.continuerun(h.tstop)

diff_recording = [a - b for a, b in zip(c2_electrode.values, c1_electrode.values)]

# pots = mem_potentials(pot_vecs)

with open('pickles/250Hz_2.5_5sec.pkl', 'wb') as f:
        pickle.dump(diff_recording, f)

# plotmap(pots, t)

# plt.figure(figsize=(10, 10))
# sns.heatmap(firing_rates, cmap='hot')
# plt.xlabel('Time (ms)')
# plt.ylabel('STN Cells')
# plt.show()

# plt.figure(figsize=(10, 10))
# sns.heatmap(membrane_potentials, cmap='viridis', yticklabels=10, xticklabels=10)
# plt.xlabel('Time (ms)')
# plt.ylabel('STN Cells')
# plt.show()
# lfp_data = {'Voltages': electrode.values, 'Times': electrode.times}

# df = pd.DataFrame(lfp_data)

# df.to_excel('lfp_measurement.xlsx', index=False)

# plt.figure(1)
# plt.plot(test_DBS_times, test_DBS, color='k')
# plt.title('DBS Square Wave at Cell #50')
# plt.xlabel('Time (ms)')
# plt.ylabel('Current (nA)')
# plt.show()

# plt.figure()
# plt.plot(t, volstn1)
# plt.show()

# fig, axs = plt.subplots(2)
# axs[0].plot(t, volstn1, color='k')
# axs[0].set_title('STN Cells #1 Membrane Potential vs Time')

# axs[1].plot(t, volgpe1, color='k')
# axs[1].set_title('GPe Cells #1 Membrane Potential vs Time')

# for ax in axs.flat:
#     ax.set(xlabel='Time (ms)', ylabel='mV')

# for ax in axs.flat:
#     ax.label_outer()

# plt.show()

plt.figure(1)
plt.plot(c1_electrode.times, diff_recording, color='k')

plt.title('STN Local Field Potentials')
plt.xlabel('Time (ms)')
plt.ylabel('mV')

plt.show()
