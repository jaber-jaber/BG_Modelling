from neuron import h, gui
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
from scipy.signal import butter, lfilter

def mem_potentials(pot_vecs, filename=None, pickle=False):
    potentials = [[pot for pot in pot_vec] for pot_vec in pot_vecs]

    if (pickle == True):
        with open(f'pickles/{filename}', 'wb') as f:
            pickle.dump(potentials, f)

    return potentials

def plotmap(pots, t, filename=None, pickle=False):
    t = [round(time, 1) for time in t]

    if pickle == True:
        with open(f'pickles/{filename}', 'rb') as f:
            pots = pickle.load(f)

    df = pd.DataFrame(pots, columns=t)
    plt.title('Heatmap of Cell Network')
    ax = sns.heatmap(df, cmap='viridis', vmin=-63, vmax=40)
    cbar = ax.collections[0].colorbar
    cbar.set_label('Membrane Potential (mV)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Cell #')
    plt.show()

# with open('pickles/STN_network_DBS_500ms.pkl', 'rb') as f:
#         dbs_pots = pickle.load(f)

# with open('pickles/STN_network_noDBS_500ms.pkl', 'rb') as f:
#         pots = pickle.load(f)

# fig, axs = plt.subplots(1, 2)
# fig.suptitle('Heatmap of Cell Network')

# axs[0].set_title('STN Network Stim OFF')
# axs[1].set_title('STN Network Stim ON')

# sns.heatmap(pots, cmap='viridis', vmin=-63, vmax=40, ax=axs[0])
# sns.heatmap(dbs_pots, cmap='viridis', vmin=-63, vmax=40, ax=axs[1])
# cbar = axs[0].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# cbar = axs[1].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# for ax in axs.flat:
#     ax.set(xlabel='Time (ms)', ylabel='Cell #')

# for ax in axs.flat:
#     ax.label_outer()

# plt.show()

def LFP_filtering(data):
    with open(f'{data}', 'rb') as f:
        data = pickle.load(f)

    window_size = 100
    weights = np.repeat(1.0, window_size)/window_size
    smoothed_data = np.convolve(data, weights, 'valid')
    
    new_dt = 0.01 * window_size
    time = np.arange(0, len(smoothed_data) * new_dt, new_dt)

    return smoothed_data, time