from neuron import h
from STN import STN

class Network():
    # Network of N cells arranged in a row.
    def __init__(self, N):
        self.N = N
        self.NumGPe = 3*N
        self.create_cells(N)
        self.channel_struct()
        self.exc_connections()
        self.inhb_connections()

    def create_cells(self, N):
        self.stn_cells1 = []
        self.stn_cells2 = []

        for i in range(N):
            stn = STN(i, 0, 0, 0, 'stn')
            stn._set_position(i*30, 10, 0)
            self.stn_cells1.append(stn)
        
        for i in range(self.NumGPe):
            stn = STN(i, 0, 0, 0, 'gpe')
            stn._set_position(i*30, -20, 0)
            self.stn_cells2.append(stn)

    def channel_struct(self):
        self.channels = []

        for i, j in enumerate(self.stn_cells1):
            numgpe = i * 3
            channel = [j, self.stn_cells2[(numgpe-1)%self.NumGPe], self.stn_cells2[numgpe], self.stn_cells2[(numgpe+1)%self.NumGPe]]
            self.channels.append(channel)

    def exc_connections(self):
        self.synapse_list = []
        self.exc_cons = []
        print(self.channels)

        for channel in self.channels:
            for i in channel[1:]:
                nc = h.NetCon(channel[0].soma(0.5)._ref_v, i.Syn_list[0][0], sec=channel[0].soma)
                self.exc_cons.append([nc])

            for gpe in channel[1:4]:
                self.synapse_list.append(gpe.Syn_list[0])

        for con in self.exc_cons:
            con.weight[0] = 0
            con.delay = 500
        
        print(self.exc_cons)
        print(self.synapse_list)

    def inhb_connections(self):
        self.inhb_cons = []

        for channel in self.channels:
            for gpe in channel[1:4]:
                pass

### Code to configure ###

# synapses = [[None for _ in range(num_cells)] for _ in range(num_cells)]
#     netcons = [[None for _ in range(num_cells)] for _ in range(num_cells)]

#     for i in range(num_cells):
#         for j in range(num_cells):
#             if i != j:  # Don't connect a cell to itself
#                 synapses[i][j] = h.ExpSyn(Cells_List[j](0.5))
#                 netcons[i][j] = h.NetCon(Cells_List[i](0.5)._ref_v, synapses[i][j], sec=Cells_List[i])
#                 netcons[i][j].weight[0] = 0.04
#                 netcons[i][j].delay = 5
#     ```
