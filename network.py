from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
import matplotlib.pyplot as plt

stn_cells = []
N = 5

for i in range(N):
    stn = STN(i, 0, 0, 0)
    stn._set_position(i*30, 0, 0)
    stn_cells.append(stn)

ps = h.PlotShape(True)
ps.show(0)
ps.color(2, sec=stn_cells[1].soma)

h.topology()
h.finitialize(-65 * mV)