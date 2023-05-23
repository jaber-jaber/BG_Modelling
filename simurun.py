from neuron import h
from matplotlib import pyplot
import numpy

def set_recording_vectors(Cell):
	"""Set soma, dendrite, and time recording vectors on the cell.
	#
	:param cell: Cell to record from.
	:return: the soma, dendrite, and time vectors as a tuple.
	"""
	soma_v_vec = h.Vector()   # Membrane potential vector at soma
	t_vec = h.Vector()        # Time stamp vector
	soma_v_vec.record(Cell.soma(0.5)._ref_v)
	t_vec.record(h._ref_t)
	#
	return soma_v_vec, t_vec
#
def simulate(tstop):
	"""Initialize and run a simulation.
	#
	:param tstop: Duration of the simulation.
	"""
	h.tstop = tstop
	h.run()
#
def show_output(soma_v_vec, t_vec, clear_fig=True):	
	"""Draw the output.
	#
	:param soma_v_vec: Membrane potential vector at the soma.
	:param dend_v_vec: Membrane potential vector at the dendrite.
	:param t_vec: Timestamp vector.
	:param clear_fig: Flag to clear the figure or draw on top of
	#        previous results.
	"""
	if clear_fig:
		pyplot.clf()
		pyplot.figure(1) # Default figsize is (8,6)
	soma_plot = pyplot.plot(t_vec, soma_v_vec, color='black',label='soma')
	pyplot.legend()
	pyplot.xlabel('time (ms)')
	pyplot.ylabel('mV')
	#pyplot.axis([0,1000,-100,100])
	pyplot.show()
#
