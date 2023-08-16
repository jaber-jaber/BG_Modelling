from neuron import h
from STN import STN
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")

h.celsius = 30

stn1 = STN(1)
stn2 = STN(2)
hh_cell = h.Section(name="soma")
hh2_cell = h.Section(name="soma")

# Set morphology, biophysics
hh_cell.L = 20
hh_cell.diam = 20
hh2_cell.L = hh_cell.L

hh_cell.insert("hh")
hh2_cell.insert("hh")
# STN will be pre-synaptic cell
# HH Cell will be post-synaptic cell

# stim = h.IClamp(stn1.soma(0.5))
# stim.delay = 500 * ms
# stim.dur = 500 * ms
# stim.amp = 5

# Stimulating the pre-synaptic STN cell with a depolarizing current induces a burst of spikes in both
# pre-synaptic cell and post-synaptic cell.

syn = h.AMPA_S(hh_cell(0.5))

nc = h.NetCon(stn1.soma(0.5)._ref_v, syn, sec=stn1.soma)
nc.weight[0] = 0.05

v_hh = h.Vector().record(hh_cell(1)._ref_v)
v_stn = h.Vector().record(stn1.soma(0.5)._ref_v)
v_hh2 = h.Vector().record(hh2_cell(0.5)._ref_v)

t = h.Vector().record(h._ref_t)

h.finitialize(-62.65 * mV)
h.continuerun(3000 * ms)

plt.figure(1)
plt.plot(t, v_hh)

plt.figure(2)
plt.plot(t, v_stn)

plt.figure(3)
plt.plot(t, v_hh2)

plt.show()
