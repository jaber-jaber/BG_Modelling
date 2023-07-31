from neuron import h, gui
from STN import STN
from neuron.units import ms, mV, sec
from simurun import set_recording_vectors, simulate, show_output
import matplotlib.pyplot as plt
import numpy as np

exec(open("./STN.py").read())
h.load_file("stdrun.hoc")

# Defining initial conditions
h.celsius = 39.65 # T = 273 + 39.65 - 9.5 = 303.15 K or 30 deg Cel

# Defining the cell
stn = STN()
stn_area = stn.soma().area()
recording_vec = h.Vector()

# Record spikes (for Freq. calculation)
rec_netcon = h.NetCon(stn.soma()._ref_v, None)
rec_netcon.record(recording_vec)

# To check the mechanisms and point processes present in the STN soma:
print(stn.soma.psection()) # Tells you all the density mech values

# Insert this if you want to obtain results of depolarization current injection into cell.
# stim = STN_cell.loc = STN_cell.current_clamp()
# stim.delay = 1
# stim.dur = 50
# stim.amp = 0.2

# Ionic currents
k_current = h.Vector().record(stn.soma().stn._ref_ik)
caL_current = h.Vector().record(stn.soma().stn._ref_icaL)
na_current = h.Vector().record(stn.soma().stn._ref_ina)
atype_current = h.Vector().record(stn.soma().stn._ref_ikA)
caT_current = h.Vector().record(stn.soma().stn._ref_icaT)
ahp_current = h.Vector().record(stn.soma().stn._ref_ikAHP)

# Membrane potential
soma_v = h.Vector().record(stn.soma()._ref_v)
time = h.Vector().record(h._ref_t)

# Normalising the simulation duration
total_dur = 1
c_duration = 104.1

h.finitialize(-60 * mV)
h.continuerun(total_dur * sec)

# Calculate Frequency
# rec_data = np.array(recording_vec)
# f = len(rec_data) / (total_dur)

# print(f)

plt.figure(1)
plt.plot(time/1000, soma_v, color='k')
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