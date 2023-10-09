from neuron import h, gui
from neuron.units import ms, mV, sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pickle

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
    sns.heatmap(df, cmap='viridis', vmin=-63, vmax=40)
    plt.show()