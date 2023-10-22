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

# with open('pickles/130Hz_2.5_3sec.pkl', 'rb') as f:
#     data1 = pickle.load(f)

# sliced_data = data1[100000:len(data1)-1]

# lfptimes = np.linspace(0, 2000, len(sliced_data))
# print(len(lfptimes), len(sliced_data))

# plt.figure()
# plt.plot(lfptimes, sliced_data, color='k')
# plt.xlabel('Time (ms)')
# plt.ylabel('Amplitude (uV)')
# plt.show()


# sample_rate = 100
# nperseg = len(sliced_data) // 8

# overlapp = nperseg // 2

# freqs, psd = welch(sliced_data, fs=sample_rate, nperseg=nperseg, noverlap=overlapp)

# plt.figure()
# plt.semilogy(freqs, psd)
# plt.show()

# with open('pickles/Differential_Recording_LFP_1_20Hz.pkl', 'rb') as f:
#     data2 = pickle.load(f)

# with open('pickles/Differential_Recording_LFP_1_45Hz.pkl', 'rb') as f:
#     data3 = pickle.load(f)
# plt.figure()
# plt.plot(lfptimes, data1)
# plt.plot(lfptimes, data2)
# plt.plot(lfptimes, data3)
# plt.plot(lfptimes, data4)
# plt.show()

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

    window_size = 1000
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

def calculate_BandPower(filename):

    with open(filename, 'rb') as f:
        data = pickle.load(f)

    data_S = data[0:50000]
    
    t = np.linspace(0, len(data_S)/10000, len(data_S))
    nperseg = len(data_S)//8
    nvp = nperseg // 2

    freqs, psd = welch(data_S, fs=1000, nperseg=nperseg, noverlap=nvp)

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

    plt.figure()
    plt.plot(t, lfp_beta_signal_rectified, color='k')
    # plt.plot(t, data_S, color='r', label='Unfiltered STN LFP DBS=OFF')
    plt.xlabel('Time (s)')
    plt.ylabel('uV')
    plt.title('Beta-Filtered Rectified STN LFP')
    plt.show()
    
    avg_beta_power = np.mean(lfp_beta_signal_rectified)

    return avg_beta_power

# files = ["pickles/20Hz_2.5_10khz_3sec.pkl", "pickles/40Hz_2.5_10khz_3sec.pkl", "pickles/60Hz_2.5_10khz_3sec.pkl", 
#          "pickles/90Hz_2.5_10khz_3sec.pkl", "pickles/130Hz_2.5_10khz_3sec.pkl","pickles/160Hz_2.5_10khz_3sec.pkl",
#          "pickles/210Hz_2.5_10khz_3sec.pkl", "pickles/250Hz_2.5_10khz_3sec.pkl", "pickles/300Hz_2.5_10khz_3sec.pkl", "pickles/330Hz_2.5_10khz_3sec.pkl"]

pow1 = calculate_BandPower('pickles/130Hz_2.5_10khz_3sec.pkl')

# amp_files = ["pickles/130Hz_0.5_5sec.pkl", "pickles/13    0Hz_3_5sec.pkl"]

# powers = []
# freqs = [20, 40, 60, 90, 130, 160, 210, 250, 300, 330]

# # # pow1 = calculate_BandPower("pickles/130Hz_0.5_5sec.pkl")
# for i in files:
#     power = calculate_BandPower(i)
#     powers.append(power)
#     print(power)

# tck = splrep(freqs, powers, s=0)
# xnew = np.linspace(min(freqs), 400, 100)
# ynew = splev(xnew, tck)

# z = np.polyfit(xnew, ynew, 3)

# plt.figure()
# plt.plot(xnew, ynew, color='k')
# plt.plot(freqs, powers, 'ro')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('STN LFP Beta Band Power')
# plt.show()