import numpy

def detect_spikes(t_vec,v_vec,thresh=0,start=100):
	spikes = []
	for i in range(start,len(t_vec)):
		if v_vec[i-1]<thresh and v_vec[i]>thresh:
			spikes.append(t_vec[i])
		#
	#
	spike_num = len(spikes)
	duration = (t_vec[-1]-t_vec[0])/1000
	spike_freq = spike_num/duration

	return spike_freq
#