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

print(midpoint)

c1_pos = 2775 # Between c30 and c31
c2_pos = 7275 # Between c80 and c81

print(c1_pos, c2_pos)

# pot_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in stncells]
# gpe_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in gpecells]

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

for pt in ptsrc:
    DBS, DBS_times = generate_DBS_signal(start, stop, dt, amp, freq, pw, offset, pt)
    signals.append([DBS, DBS_times])

for n, cell in enumerate(stncells):
    sig_vec = h.Vector().from_python(signals[n][0])
    stim_vec = sig_vec.play(cell.stim, cell.stim._ref_amp, h.dt)
    stim_vecs.append(stim_vec)

# test_DBS = signals[50][0]
# test_DBS_times = signals[50][1]

# test_DBS2 = signals[0][0]
# test_DBS_times2 = signals[0][1]
c1_electrode = LfpElectrode(x=c1_pos, y=0, z=100, sampling_period=0.1, method="Point")
c2_electrode = LfpElectrode(x=c2_pos, y=0, z=100, sampling_period=0.1, method="Point")

h.finitialize(h.v_init)
h.run(h.tstop)

diff_recording = [a - b for a, b in zip(c2_electrode.values, c1_electrode.values)]

# pots = mem_potentials(pot_vecs)
# gpe_pots = mem_potentials(gpe_vecs)

time_arr = [round(time, 1) for time in t]

# df1 = pd.DataFrame(pots, columns=time_arr)
# df2 = pd.DataFrame(gpe_pots, columns=time_arr)
with open('pickles/130Hz_2.5_10khz_10sec.pkl', 'wb') as f:
        pickle.dump(diff_recording, f)  

# plotmap(pots, t)

# fig, axs = plt.subplots(1, 2, figsize= (12, 4))
# fig.suptitle('Heatmap of Cell Network')

# axs[0].set_title('STN Network Normal')
# axs[1].set_title('GPe Network Normal')

# sns.heatmap(df1, cmap='plasma', vmin=-63, vmax=40, ax=axs[0])
# sns.heatmap(df2, cmap='plasma', vmin=-63, vmax=40, ax=axs[1])

# cbar = axs[0].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# cbar = axs[1].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# for ax in axs.flat:
#     ax.set(xlabel='Time (ms)', ylabel='Cell #')

# for ax in axs.flat:
#     ax.label_outer()

# plt.show()

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

# fig, axs = plt.subplots(1, 2)
# axs[0].plot(test_DBS_times, test_DBS, color='k')
# axs[0].set_title('DBS Square Wave at Cell #50')

# axs[1].plot(test_DBS_times2, test_DBS2, color='k')
# axs[1].set_title('DBS Square Wave at Cell #1')

# for ax in axs.flat:
#     ax.set(xlabel='Time (ms)', ylabel='mA')

# plt.show()

plt.figure()
plt.plot(c1_electrode.times, diff_recording)
plt.show()

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
