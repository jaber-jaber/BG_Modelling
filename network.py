from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
import matplotlib.pyplot as plt

stn_cells = []
N = 5

for i in range(N):
    stn = STN(i)
    stn._set_position(i*5, 0, i+100)
    stn_cells.append(stn)


ps = h.PlotShape(True)
ps.show(0)

h.topology()
h.finitialize(-65 * mV)