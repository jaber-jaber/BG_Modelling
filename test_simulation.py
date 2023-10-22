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
h.tstop = 3000 * ms
h.dt = 0.01

# Defining the cell(s)
recording_vec = h.Vector()

gpe = GPe(1, 0, 0, 0, "gpe")
gpe2 = GPe(2, 0, 0, 0, "gpe")
gpe_area = gpe.soma().area()

# Record spikes (for Freq. calculation)
rec_netcon = h.NetCon(gpe.soma()._ref_v, None)
rec_netcon.record(recording_vec)

# Current train


# To check the mechanisms and point processes present in the STN soma:
# print(stn.soma.psection()) # Tells you all the density mech values
# To find out all h attributes, run: print(textwrap.fill(", ".join(dir(h))))

# Insert this if you want to obtain results of depolarization current injection into cell.
stim1 = h.IClamp(gpe.soma(0.5))
stim1.delay = 1 * sec
stim1.dur = 1 * sec
stim1.amp = 25e-3

stim2 = h.IClamp(gpe2.soma(0.5))
stim2.delay = 1 * sec
stim2.dur = 1 * sec
stim2.amp = -25e-3

# stim3 = h.IClamp(stn3.soma(0.5))
# stim3.delay = 1 * sec
# stim3.dur = 1 * sec
# stim3.amp = 0.0954
# I3onic currents
# k_current = h.Vector().record(stn.soma().stn._ref_ik)
# caL_current = h.Vector().record(stn.soma().stn._ref_icaL)
# na_current = h.Vector().record(stn.soma().stn._ref_ina)
# atype_current = h.Vector().record(stn.soma().stn._ref_ikA)
# caT_current = h.Vector().record(stn.soma().stn._ref_icaT)
# ahp_current = h.Vector().record(stn.soma().stn._ref_ikAHP)

# Membrane potential
soma_v = h.Vector().record(gpe.soma()._ref_v)
soma_v2 = h.Vector().record(gpe2.soma()._ref_v)
# soma_v3 = h.Vector().record(stn3.soma()._ref_v)
time = h.Vector().record(h._ref_t)
# apc = h.APCount(stn.soma(0.5))

h.finitialize(h.v_init)
h.continuerun(h.tstop)

# Calculate Frequency
rec_data = np.array(recording_vec)
f = (len(rec_data) / (h.tstop))*1000

print("{} Hz".format(f))
# print(apc.thresh) # Threshold is -20 at this temp
# time_list = time.to_python()
# voltage_list = soma_v.to_python()


fig, axs = plt.subplots(2, 1)
fig.suptitle('GPe Cell Model')

axs[0].plot(time, soma_v, color='k')
axs[1].plot(time, soma_v2, color='k')

for ax in axs.flat:
    ax.set(xlabel='Time (ms)', ylabel='mV')

for ax in axs.flat:
    ax.label_outer()

plt.show()

# vtime = plt.figure(1)
# plt.plot(time, soma_v, color='k')
# plt.title("GPe Cell Membrane Potential vs Time")
# plt.xlabel("Time (s)")
# plt.ylabel("mV")
# vtime.show()

# ctime = plt.figure(2)
# plt.plot(time, k_current)
# plt.plot(time, caL_current)
# plt.plot(time, na_current)
# plt.plot(time, atype_current)
# plt.plot(time, caT_current)
# plt.plot(time, ahp_current)
# plt.xlabel('Time (ms)')
# plt.ylabel('Current Density (uA/cm2)')
# plt.legend(["Potassium current", "L-type calcium current", "Sodium current", "A-type Potassium current", "T-type calcium current", "Calcium-dependent Potassium current"])
# ctime.show()

plt.show()