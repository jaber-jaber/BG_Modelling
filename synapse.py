from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 3000 * ms

stn = STN(1, 0, 0, 0)
stn2 = STN(2, 0, 0, 0)


stn_syn = h.AMPA_S(stn2.soma(0.5))

nc = h.NetCon(stn.soma(0.5)._ref_v, stn_syn, sec=stn.soma)
# nc.dur = 2000 * ms
nc.delay = 1000 * ms
nc.weight[0] = 1

stn2_v = h.Vector().record(stn2.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(h.v_init)
h.continuerun(h.tstop)

plt.figure(1)
plt.plot(t, stn2_v)
plt.show()