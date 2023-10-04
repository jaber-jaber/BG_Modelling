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

h.load_file("stdrun.hoc")
h.load_file("LFPsimpy-master/LFPsimpy-master/LFPsimpy/LFPsimpy.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 1000 * ms

N = 50
SSC_network = Network(N)
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

spike_vecs = [h.Vector() for _ in range(N)]
pot_vecs = [h.Vector().record(cell.soma(0.5)._ref_v) for cell in stncells]
netcons = [h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma) for cell in stncells]

for con in netcons:
    con.threshold = 36

for vec, nc in zip(spike_vecs, netcons):
    nc.record(vec)

# ps = h.PlotShape(True)
# ps.show(0)
# ps.color(2, sec=stncells[int(N/2)].soma)

electrode = LfpElectrode(x=4530, y=10, z=500, sampling_period=0.01, method="Point")

h.finitialize(h.v_init)
h.run(h.tstop)

# pots = mem_potentials(t, spike_vecs, pot_vecs)

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

# plt.figure(2)
# plt.plot(t, volstn)
# plt.show()

# plt.figure(1)
# plt.plot(electrode.times, electrode.values)
# plt.show()