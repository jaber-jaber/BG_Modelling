from neuron import h, gui
from STN import STN
from GPE import GPe
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import textwrap

h.load_file("stdrun.hoc")

# Defining initial conditions
h.celsius = 30
h.v_init = -62.65 * mV
h.tstop =  10 * sec
h.dt = 0.01

# Defining the cell(s)
stn = STN(1, 0, 0, 0, "stn")
stn_area = stn.soma().area()
recording_vec = h.Vector()

gpe = GPe(1, 0, 0, 0, "gpe")
gpe_area = gpe.soma().area()

# Record spikes (for Freq. calculation)
rec_netcon = h.NetCon(stn.soma()._ref_v, None)
rec_netcon.record(recording_vec)

# Current train
stim = h.Ipulse2(stn.soma(0.5))
stim.delay = 1 * sec
stim.dur = 5 * ms
stim.per =  7.35 * ms
stim.num = 1
stim.amp = 0.1

# To check the mechanisms and point processes present in the STN soma:
# print(stn.soma.psection()) # Tells you all the density mech values
# To find out all h attributes, run: print(textwrap.fill(", ".join(dir(h))))

# Insert this if you want to obtain results of depolarization current injection into cell.
# stim = h.IClamp(gpe.soma(0.5))
# stim.delay = 1 * sec
# stim.dur = 0.5 * sec
# stim.amp = -10e-3

# Ionic currents
# k_current = h.Vector().record(stn.soma().stn._ref_ik)
# caL_current = h.Vector().record(stn.soma().stn._ref_icaL)
# na_current = h.Vector().record(stn.soma().stn._ref_ina)
# atype_current = h.Vector().record(stn.soma().stn._ref_ikA)
# caT_current = h.Vector().record(stn.soma().stn._ref_icaT)
# ahp_current = h.Vector().record(stn.soma().stn._ref_ikAHP)

# Membrane potential
soma_v = h.Vector().record(stn.soma()._ref_v)
time = h.Vector().record(h._ref_t)
# apc = h.APCount(stn.soma(0.5))

h.finitialize(h.v_init)
h.continuerun(h.tstop)

# Calculate Frequency
rec_data = np.array(recording_vec)
f = (len(rec_data) / (h.tstop))*1000

print("{} Hz".format(f))
# print(apc.thresh) # Threshold is -20 at this temp


vtime = plt.figure(1)
plt.plot(time, soma_v, color='k')
plt.xlabel("Time (s)")
plt.ylabel("Membrane Potential (mV)")
vtime.show()

# ctime = plt.figure(2)
# plt.plot(time/1000, k_current)
# plt.plot(time/1000, caL_current)
# plt.plot(time/1000, na_current)
# plt.plot(time/1000, atype_current)
# plt.plot(time/1000, caT_current)
# plt.plot(time/1000, ahp_current)
# plt.legend(["Potassium current", "L-type calcium current", "Sodium current", "A-type Potassium current", "T-type calcium current", "Calcium-dependent Potassium current"])
# ctime.show()

plt.show()