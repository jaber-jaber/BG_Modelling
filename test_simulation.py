from neuron import h, gui
from STN import STN
from neuron.units import ms, mV, sec
from simurun import set_recording_vectors, simulate, show_output
import matplotlib.pyplot as plt
import numpy as np

exec(open("./STN.py").read())
h.load_file("stdrun.hoc")

stn = STN()
# To check the mechanisms and point processes present in the STN soma:
# run print(h.psection())

# Insert this if you want to obtain results of depolarization current injection into cell.
""" stim = STN_cell.loc = STN_cell.current_clamp()
stim.delay = 1
stim.dur = 50
stim.amp = 0.2 """

soma_v = h.Vector().record(stn.soma()._ref_v)
time = h.Vector().record(h._ref_t)

h.finitialize(-60 * mV)
h.continuerun(1 * sec)

plt.figure(1)
plt.plot(time/1000, soma_v, color='k')
plt.ylim(-60)
plt.xlabel("Time (s)")
plt.ylabel("Membrane Potential (mV)")
plt.show()
