from neuron import h, gui
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
from scipy.signal import welch, butter, filtfilt, sosfiltfilt, lfilter, cheby1, find_peaks
from scipy.interpolate import splrep, splev
from scipy.fft import fft, fftfreq
from scipy.integrate import simpson

""" Produce heatmaps or raster plots.
LFP filtering.

"""

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

def raster_plot(cell_list):
    network_array = []

    for cell in cell_list:
        spike_times = h.Vector()
        nc = h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma)
        nc.threshold = 35
        nc.record(spike_times)
        network_array.append(spike_times)

    return network_array

def LFP_filtering(data):

    window_size = 1000
    weights = np.repeat(1.0, window_size)/window_size
    smoothed_data = np.convolve(data, weights, 'valid')
    
    time = np.linspace(0, 5000, len(smoothed_data))

    return smoothed_data, time

def calculate_BandPower(filename):

    with open(filename, 'rb') as f:
        data_S = pickle.load(f)

    T = 0.1
    Fs = 1000

    nyq = 0.5*Fs
    lowcut = 22/nyq
    highcut = 30/nyq
    rp = 0.5
    order = 4
    tail_length = 10000

    b, a = cheby1(order, rp, [lowcut, highcut], 'band')

    lfp_beta_signal = filtfilt(b, a, data_S)

    lfp_beta_signal_rectified = np.absolute(lfp_beta_signal)
    
    avg_beta_power = np.mean(lfp_beta_signal_rectified)

    return avg_beta_power
