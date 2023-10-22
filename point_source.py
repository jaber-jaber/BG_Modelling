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

    # plt.figure()
    # for x in np.arange(0, 10):
    #     plt.plot(distances, tr_arrays[x], label='Electrode {x}'.format(x=x))

    # plt.legend(loc='best')
    # plt.grid(True)
    # plt.xlabel('Cell Position')
    # plt.ylabel('Amplitude')
    # plt.show()

    summed_transfer_resistances = np.sum(tr_arrays, axis=0)

    return summed_transfer_resistances

# list_electrodes, list_cells = calculate_distances(45, 55)
# summed_tr = compute_transfer_resistance(list_electrodes, list_cells)
# distances = [(i * 3 + 1) * 30 for i in range(100)]

# plt.figure()
# plt.plot(distances, summed_tr, color='k')
# plt.grid(True)
# plt.xlabel('Cell Position')
# plt.ylabel('Amplitude')
# plt.show()
