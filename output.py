from neuron import h, gui
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from LFPsimpy import LfpElectrode

def find_closest(lst, target):
    lst_np = np.array(lst)
    idx = (np.abs(lst_np - target)).argmin()
    return idx

def mem_potentials(t, spike_vecs, pot_vecs):
    potentials = [[0 for _ in range(len(t))] for _ in range(len(spike_vecs))]
    idx = [[0 for _ in range(len(vec))] for vec in spike_vecs]
    pyt = t.to_python()

    for num_vectors, spike_vec in enumerate(spike_vecs):
        for num_spikes, spike_time in enumerate(spike_vec):
            idx[num_vectors][num_spikes] = find_closest(pyt, spike_time)
            potentials[num_vectors][idx[num_vectors][num_spikes]] = pot_vecs[num_vectors][idx[num_vectors][num_spikes]]
    
    return potentials

def plotmap(pots, t):
    df = pd.DataFrame(pots, columns=t)
    sns.heatmap(df, cmap='crest', xticklabels=True, yticklabels=100)
    plt.show()