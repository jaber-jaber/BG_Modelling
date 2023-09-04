from neuron import h, gui
from neuron.units import ms, mV
from STN import STN
from set_network import Network
import matplotlib.pyplot as plt

SSC_network = Network(5)

ps = h.PlotShape(True)
ps.show(0)

h.topology()
h.finitialize(-65 * mV)