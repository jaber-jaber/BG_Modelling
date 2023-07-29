from neuron import h, gui
from STN import STN
from neuron.units import ms, mV, sec
from simurun import set_recording_vectors, simulate, show_output
import matplotlib.pyplot as plt
import numpy as np

exec(open("./STN.py").read())
h.load_file("stdrun.hoc")
h.celsius = 30

stn = STN()
stn_area = stn.soma().area()
recording_vec = h.Vector()

rec_netcon = h.NetCon(stn.soma()._ref_v, None)
rec_netcon.record(recording_vec)

# To check the mechanisms and point processes present in the STN soma:
# print(stn.soma.psection()) # Tells you all the density mech values

# Insert this if you want to obtain results of depolarization current injection into cell.
""" stim = STN_cell.loc = STN_cell.current_clamp()
stim.delay = 1
stim.dur = 50
stim.amp = 0.2 """

k_current = h.Vector().record(stn.soma()._ref_ik)
caL_current = h.Vector().record(stn.soma().stn._ref_icaL)
na_current = h.Vector().record(stn.soma()._ref_ina)
atype_current = h.Vector().record(stn.soma().stn._ref_ikA)
caT_current = h.Vector().record(stn.soma().stn._ref_icaT)
ahp_current = h.Vector().record(stn.soma().stn._ref_ikAHP)

soma_v = h.Vector().record(stn.soma()._ref_v)
time = h.Vector().record(h._ref_t)

h.finitialize(-60 * mV)
h.continuerun(1 * sec)

plt.figure(1)
plt.plot(time/1000, soma_v, color='k')
plt.ylim(-60)
plt.xlabel("Time (s)")
plt.ylabel("Membrane Potential (mV)")


# plt.figure(2)
# plt.plot(time/1000, k_current)
# plt.plot(time/1000, caL_current)
# plt.plot(time/1000, na_current)
# plt.plot(time/1000, atype_current)
# plt.plot(time/1000, caT_current)
# plt.plot(time/1000, ahp_current)
# plt.legend(["Potassium current", "L-type calcium current", "Sodium current", "A-type Potassium current", "T-type calcium current", "Calcium-dependent Potassium current"])

plt.show()