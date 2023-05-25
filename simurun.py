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

def spike_plot(v_vec,t_vec,name,vmin=-80,vmax=20,xtic=2,ytic=100):
	'''
	Takes an array of membrane potentials and outputs a spike plot figure.
	'''
	# Initialize image parameters
	vrange = vmax-vmin
	#
	timeS = [x for x in numpy.arange(0,int(t_vec[-1]+1),h.dt)]
	timeD = numpy.arange(0,int(t_vec[-1]+1),1)
	#
	timeID = [timeS.index(t) for t in timeD[:-1]]
	#
	ht = len(v_vec)
	w = len(timeID)
	step = int(len(t_vec)/w)
	ytic = int(max(timeS)*xtic/(2*ht))
	traces = [[numpy.mean([v_vec[i][x] for x in range(j,j+step,1)]) for j in timeID] for i in range(ht)]
	scaleData = []
	preimage = []
	#
	# Scale data
	for i in range(ht):
		scaleData.append([])
		for j in range(w):
			if traces[i][j]>vmax:
				scaleData[i].append(0)
			elif traces[i][j]<vmin:
				scaleData[i].append(1)
			else:
				scaleData[i].append(-(traces[i][j]-vmax)/vrange)
			#
		#
	# Creates the image	
	for i in range(ht*ytic):
		preimage.append([])
		for j in range(w*xtic):
			preimage[i].append(scaleData[i/ytic][j/xtic])
		#
	#
	image = numpy.array(preimage)
	fig = pyplot.figure()	
	pyplot.imshow(image,cmap=pyplot.cm.gray)
	pyplot.imsave(name,image,cmap=pyplot.cm.gray)
	fig.show()
#
