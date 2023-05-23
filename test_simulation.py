from neuron import h, gui
from STN import STN
from simurun import set_recording_vectors, simulate, show_output

exec(open("./STN.py").read())

STN_cell = STN()

h.topology()

soma_v_vec, t_vec = set_recording_vectors(STN_cell)
tstop = STN_cell.dur = 700
STN_cell.dur = 500
STN_cell.amp = 60
STN_cell.delay = 1
stim = STN_cell.current_clamp()

simulate(tstop)

show_output(soma_v_vec, t_vec)