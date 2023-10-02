from neuron import h, gui
from neuron.units import ms, mV, sec
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from LFPsimpy import LfpElectrode

h.load_file("stdrun.hoc")
h.load_file("LFPsimpy-master/LFPsimpy-master/LFPsimpy/LFPsimpy.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 5000 * ms

time_bins = 5000
bin_width = 1.0

SSC_network = Network(100)
stncells = SSC_network.stn_cells1

test = SSC_network.gpe_cells[1]
test1 = stncells[1]

# stim = h.IClamp(test1.soma(0.5))
# stim.delay = 250 * ms
# stim.dur = h.tstop - stim.delay
# stim.amp = -10

volstn = h.Vector().record(test1.soma(0.5)._ref_v)

vol = h.Vector().record(test.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

vecs = [h.Vector() for _ in range(len(stncells))]
netcons = [h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma) for cell in stncells]

for vec, nc in zip(vecs, netcons):
    nc.record(vec)

# ps = h.PlotShape(True)
# ps.show(0)
# ps.color(2, sec=stncells[50].soma)

# electrode = LfpElectrode(x=4530, y=10, z=500, sampling_period=0.01, method="Point")

h.finitialize(h.v_init)
h.run(h.tstop)

firing_rates = np.zeros((len(stncells), time_bins))
membrane_potentials = np.zeros((len(stncells), time_bins))

for i in range(len(stncells)):
    spike_times = vecs[i].to_python()
    np_spiketimes = np.array(spike_times)
    np_mp = np.array(spike_times)
    bins = np.arange(0, time_bins*bin_width, bin_width)
    bin_indices = np.digitize(np_mp, bins)

    for j in range(time_bins):
        num_spikes = np.sum((np_spiketimes >= j * bin_width) & (np_spiketimes < (j+1) * bin_width))
        firing_rates[i, j] = num_spikes / bin_width

        if len(np_mp[bin_indices == j]) > 0:
            membrane_potentials[i, j] = np_mp[bin_indices == j][0]
        else:
            membrane_potentials[i, j] = np.nan

# plt.figure(figsize=(10, 10))
# sns.heatmap(firing_rates, cmap='hot', yticklabels=10, xticklabels=30)
# plt.xlabel('Time (ms)')
# plt.ylabel('STN Cells')
# plt.show()

plt.figure(figsize=(10, 10))
sns.heatmap(membrane_potentials, cmap='viridis', yticklabels=10, xticklabels=10)
plt.xlabel('Time (ms)')
plt.ylabel('STN Cells')
plt.show()
# lfp_data = {'Voltages': electrode.values, 'Times': electrode.times}

# df = pd.DataFrame(lfp_data)

# df.to_excel('lfp_measurement.xlsx', index=False)

# plt.figure(2)
# plt.plot(t, vol)
# plt.show()

# plt.figure(1)
# plt.plot(electrode.times, electrode.values)
# plt.show()