from neuron import h, gui
from neuron.units import ms, mV, sec
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt
import pandas as pd
from LFPsimpy import LfpElectrode

h.load_file("stdrun.hoc")
h.load_file("LFPsimpy-master/LFPsimpy-master/LFPsimpy/LFPsimpy.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 140 * ms

SSC_network = Network(100)

test = SSC_network.gpe_cells[1]
test1 = SSC_network.stn_cells1[1]

volstn = h.Vector().record(test1.soma(0.5)._ref_v)

vol = h.Vector().record(test.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

# ps = h.PlotShape(True)
# ps.show(0)

electrode = LfpElectrode(x=0, y=0, z=100, sampling_period=0.01, method="Point")

h.finitialize(h.v_init)
h.run(h.tstop)

# lfp_data = {'Voltages': electrode.values, 'Times': electrode.times}

# df = pd.DataFrame(lfp_data)

# df.to_excel('lfp_measurement.xlsx', index=False)

# plt.figure(2)
# plt.plot(t, vol)
# plt.show()

plt.figure(1)
plt.plot(electrode.times, electrode.values)
plt.show()