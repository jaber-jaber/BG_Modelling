import numpy as np
import matplotlib.pyplot as plt

def calculate_distances(start, end):

    x = np.arange(start, end + 1)
    
    list_electrodes = np.column_stack(((x * 3 + 1) * 30, np.full_like(x, 10)))

    list_cells = np.column_stack(((np.arange(100) * 3 + 1) * 30, np.zeros(100)))

    return list_electrodes, list_cells

def compute_transfer_resistance(list_electrodes, list_cells):
    tr_arrays = []
    sigma = 0.3

    for electrode_x, electrode_y in list_electrodes:
        # Calculate the Euclidean distance between the electrode and each cell
        distances = np.sqrt((list_cells[:, 0] - electrode_x)**2 + (list_cells[:, 1] - electrode_y)**2)
        # Calculate tr for each distance and append the resulting array to tr_arrays
        tr_arrays.append(1 / (4 * np.pi * sigma * distances))

    summed_transfer_resistances = np.sum(tr_arrays, axis=0)

    return summed_transfer_resistances