from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")

h.celsius = 30
h.v_init = -62.25 * mV
h.tstop = 3000 * ms

stn = STN(1, 0, 0, 0, 'stn')
stn2 = STN(2, 0, 0, 0, 'stn')

gabaa_ = stn.Syn_list[0]

nc = h.NetCon(stn2.soma(0.5)._ref_v, gabaa_, sec=stn2.soma)
nc.weight[0] = 1
nc.delay = 1000

stn_v = h.Vector().record(stn.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(h.v_init)
h.continuerun(h.tstop)

plt.figure(1)
plt.plot(t, stn_v)
plt.show()