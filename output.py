from neuron import h, gui
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
from scipy.fft import fft, fftshift, fftfreq
import scipy.signal as signal

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


# with open('pickles/Differential_Recording_LFP_1_5Hz.pkl', 'rb') as f:
#     data1 = pickle.load(f)

# with open('pickles/Differential_Recording_LFP_1_20Hz.pkl', 'rb') as f:
#     data2 = pickle.load(f)

# with open('pickles/Differential_Recording_LFP_1_45Hz.pkl', 'rb') as f:
#     data3 = pickle.load(f)

with open('pickles/Differential_Recording_130Hz_DBS.pkl', 'rb') as f:
    LFPDBS = pickle.load(f)

# # Load the time data from the 5th pickle file
with open('pickles/time.pkl', 'rb') as f:
    times = pickle.load(f)


# plt.figure()
# plt.plot(lfptimes, data1)
# plt.plot(lfptimes, data2)
# plt.plot(lfptimes, data3)
# plt.plot(lfptimes, data4)
# plt.show()

start = 0
stop = 5000
num_values = 499999

time = np.linspace(0, 5000, num_values)

# plt.figure()
# plt.plot(LFPDBS)
# plt.show()

# with open('pickles/STN_RasterPlot_NOSTIM2.pkl', 'rb') as f:
#         pots = pickle.load(f)

# with open('pickles/STN_RasterPlot_Delayed1Sec.pkl', 'rb') as f:
#         dbs_pots = pickle.load(f)

# with open('pickles/STN_RasterPlot_FULLSTIM.pkl', 'rb') as f:
#         dbs_fullpots = pickle.load(f)

# with open('pickles/3sectime.pkl', 'rb') as f:
#         time = pickle.load(f)

# time_arr = [round(t, 1) for t in time]

# df1 = pd.DataFrame(pots, columns=time_arr)
# df2 = pd.DataFrame(dbs_pots, columns=time_arr)
# df3 = pd.DataFrame(dbs_fullpots, columns=time_arr)
# fig, axs = plt.subplots(1, 3, figsize= (12, 4))
# fig.suptitle('Heatmap of Cell Network')

# axs[0].set_title('STN Network Stim OFF')
# axs[1].set_title('STN Network Stim ON - Delayed 1 sec')
# axs[2].set_title('STN Network Stim ON - Full Simulation')

# sns.heatmap(df1, cmap='viridis', vmin=-63, vmax=40, ax=axs[0])
# sns.heatmap(df2, cmap='viridis', vmin=-63, vmax=40, ax=axs[1])
# sns.heatmap(df3, cmap='viridis', vmin=-63, vmax=40, ax=axs[2])

# cbar = axs[0].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# cbar = axs[1].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# cbar = axs[2].collections[0].colorbar
# cbar.set_label('Membrane Potential (mV)')

# for ax in axs.flat:
#     ax.set(xlabel='Time (ms)', ylabel='Cell #')

# for ax in axs.flat:
#     ax.label_outer()

# plt.show()

def LFP_filtering(data):

    window_size = 5000
    weights = np.repeat(1.0, window_size)/window_size
    smoothed_data = np.convolve(data, weights, 'valid')
    
    time = np.linspace(0, 5000, len(smoothed_data))

    return smoothed_data, time

# smoothed_data, time = LFP_filtering(LFPDBS)

# plt.figure(1)
# plt.plot(time, smoothed_data, color='k')
# plt.xlabel('Time')
# plt.ylabel('Voltage')
# plt.show()

def plot_psd(data):

    cutoff = 0.1
    sample_rate = 100
    nyq = 0.5 * sample_rate

    order = 3
    b, a = signal.butter(order, cutoff / nyq, btype='high')

    filtered_LFP = signal.filtfilt(b, a, data)

    n_samples_in_window = int((0 - 2000) / 0.01) + 1
    lfp_data_window = filtered_LFP[:n_samples_in_window]

    t = np.arange(0, len(filtered_LFP)) / sample_rate

    fftdata = fft(lfp_data_window)
    frequencies = fftfreq(len(lfp_data_window), 1/sample_rate)

    return fftdata, frequencies, filtered_LFP, t

# fftdata, frequencies, filtered_data, timelfp = plot_psd(smoothed_data)
# magnitude = np.abs(fftdata)

# peaks, _ = signal.find_peaks(magnitude, height=50)
# peak_frequencies = frequencies[peaks]
# peak_magnitudes = magnitude[peaks]

# print("Peak Freq: ", peak_frequencies)

# plt.figure()
# plt.plot(timelfp, filtered_data, color='k', label='Filtered & Smoothed LFP')
# plt.plot(timelfp, smoothed_data, color='r', label='Smoothed LFP')
# plt.xlabel('Time (ms)')
# plt.ylabel('Voltage (uV)')
# plt.legend(loc='best')
# plt.show()

# sample_rate = 100
# time_window = 2000
# nperseg = time_window * sample_rate // 1000

# overlapp = 50
# noverlap = int(nperseg * (overlapp / 100))

# freqs, psd = signal.welch(filtered_data[:nperseg], fs=sample_rate, nperseg=nperseg, noverlap=noverlap)
# plt.figure()
# plt.semilogy(freqs, psd)
# plt.show()
# plt.figure()
# plt.plot(frequencies, magnitude, color='k')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.xlim(0, 2)
# plt.show()
# plt.figure(figsize=(10, 6))
# plt.psd(data_filtered, Fs=1/0.01)
# plt.show()