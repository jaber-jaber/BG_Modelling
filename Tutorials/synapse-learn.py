from neuron import h

# nc = h.NetCon(source -> pointer to pre-synaptic membrane potential (v_pre), target -> synaptic mechanism
# that can receive events)

# nc = h.Netcon(source_ref_v, target[, threshold, delay, weight, sec = section])

# Defaults
# nc.threshold = 10
# nc.delay = 1
# nc.weight[0] = 0 -> array

# NMODL specification for post-synaptic cell (here's what to do when you receive event)
# NET_RECEIVE (weight(uS))