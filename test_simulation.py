from neuron import h, gui
from STN import STN
from neuron.units import ms, mV
from simurun import set_recording_vectors, simulate, show_output
import matplotlib.pyplot as plt
import numpy as np

exec(open("./STN.py").read())
h.load_file("stdrun.hoc")

STN_cell = STN()

# Insert this if you want to obtain results of depolarization current injection into cell.
stim = STN_cell.loc = STN_cell.current_clamp()
stim.delay = 0
stim.dur = 200
stim.amp = 12

tstop = 0.2
spike_times = []
soma_v = h.Vector().record(STN_cell.soma()._ref_v)
time = h.Vector().record(h._ref_t)


def record_spike():
    spike_times.append(h.t)

spike_detector = h.NetCon(STN_cell.soma()._ref_v, None)
spike_detector.threshold = 0 * mV
spike_detector.record(record_spike)

h.finitialize(-60 * mV)
h.continuerun(200 * ms)

spike_times = np.array(spike_times)
total_spikes = len(spike_times)
print(spike_times)
print(len(spike_times))
print(h.psection())

freq = total_spikes/(tstop)
print(freq)

# print(tnew[1:10])
plt.figure(1)
plt.plot(time, soma_v, color='k')
plt.ylim(-60)
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")
plt.show()
