from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 3000 * ms

SSC_network = Network(3)

test = SSC_network.gpe_cells[1]

vol = h.Vector().record(test.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(h.v_init)
h.continuerun(h.tstop)

plt.figure(1)
plt.plot(t, vol)
plt.show()
h.finitialize(h.v_init)