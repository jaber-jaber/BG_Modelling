from neuron import h
from neuron.units import sec, ms
from STN import STN
from GPE import GPe

class Network():
    # Network of N STN cells arranged in a row.
    def __init__(self, N):
        self.N = N
        self.NumGPe = 3*N
        self.create_cells(N)
        self.channel_struct()
        self.exc_connections()
        self.inhb_connections()
        self.set_netcons()

    def create_cells(self, N):
        self.stn_cells1 = []
        self.gpe_cells = []
        space = 30

        for i in range(N):
            stn = STN(i, 0, 0, 0, 'stn')
            stn._set_position((i*3+1) * space, 10, 0)
            self.stn_cells1.append(stn)

        for i in range(self.NumGPe):
            gpe = GPe(i, 0, 0, 0, 'gpe')
            gpe._set_position(i*space, -1000, 0)
            self.gpe_cells.append(gpe)

    def channel_struct(self):
        """ Function to build all functional channels given N number of cells in the network.
        1:3 ratio between STN cells and GPe cells."""

        self.channels = [] # List of all functional channels

        for i, j in enumerate(self.stn_cells1):
            # i = position of cell (0, 1, etc)
            # j = reference to cell object

            numgpe = i * 3 # number of GPe cells

            # Create "channel" which is a list containing 1 STN cell and 3 GPe cells
            channel = [j, self.gpe_cells[(numgpe-1)%self.NumGPe], self.gpe_cells[numgpe], self.gpe_cells[(numgpe+1)%self.NumGPe]]
            self.channels.append(channel)

    def exc_connections(self):
        """Excitatory connections based on Hahn and McIntyre's functional channel paradigm.
        1 STN cell -> 3 GPe cells in its channel."""

        self.synapse_list = [] # List of synapse point processes
        self.exc_cons = [] # List of NetCon objects connecting 1 STN cell to all 3 GPe cells within its channel

        print(self.channels)

        for channel in self.channels:
            for i in channel[1:]:
                # i = GPe cell
                
                nc = h.NetCon(channel[0].soma(0.5)._ref_v, i.Syn_list[0][0], sec=channel[0].soma)
                # source = STN cell
                # target = GPe cell's inserted AMPA pointprocess (see Cell.py)

                self.exc_cons.append(nc) 

            for gpe in channel[1:4]:

                # Append AMPA pointprocess (Synapse)
                self.synapse_list.append(gpe.Syn_list[0])
            
        print(f"List of excitatory connections in the channel: {self.exc_cons} \n")
        
    def inhb_connections(self):
        """Inhibitory connections as based on Hahn and McIntyre's functional channel paradigm.
        Each GPe cell inhibits 2 GPe cells within its own channel.
        Each GPe cell inhibits 4 neighbouring GPe cells.
        Each GPe cell inhibits 2 neighbouring STN cells."""
        self.nb_cons = []
        self.stn_cons = []
        self.nclist = []
        self.pnclist = []
        self.nnclist = []
        self.prnclist = []

        for channel in self.channels:
            for gpe in channel[1:]: # For each GPe cell in the channel
                
                for channel_nb in channel[1:]: # For each neighbour to the GPe cell
                    if gpe != channel_nb: # Don't connect cell to itself
                        nb_nc = h.NetCon(gpe.soma(0.5)._ref_v, channel_nb.Syn_list[0][1], sec=gpe.soma)
                        self.nb_cons.append(nb_nc)
                        # source = GPe cell
                        # target = Neighbouring GPe cell's GABAa pointprocess (see Cell.py)
        
        print(f"List of inhibitory connections between the GPe cell and its neighbours: {self.nb_cons} \n")

        if len(self.channels) > 1:
            for k in range(len(self.channels)):
                current = self.channels[k]
                after = self.channels[(k+1) % len(self.channels)]
                prev = self.channels[(k-1) % len(self.channels)]

                nnlist = self.channels[(k+2) % len(self.channels)]
                prprlist = self.channels[(k-2) % len(self.channels)]

                for i in range(1, len(current)):
                    gpe = current[i]
                    nenc = h.NetCon(gpe.soma(0.5)._ref_v, after[0].Syn_list[0], sec=gpe.soma)
                    nc2 = h.NetCon(gpe.soma(0.5)._ref_v, prev[0].Syn_list[0], sec=gpe.soma)
                    self.stn_cons.append([nenc, nc2])

                for j in range(1, len(current)):
                    gpe = current[j]

                    for p in range(1, 4):
                        nc3 = h.NetCon(gpe.soma(0.5)._ref_v, after[p].Syn_list[0][1], sec=gpe.soma)
                        pnc = h.NetCon(gpe.soma(0.5)._ref_v, prev[p].Syn_list[0][1], sec=gpe.soma)
                        self.nclist.append(nc3)
                        self.pnclist.append(pnc)
                    
                    nnc = h.NetCon(gpe.soma(0.5)._ref_v, nnlist[1].Syn_list[0][1], sec=gpe.soma)
                    self.nnclist.append(nnc)
                    prnc = h.NetCon(gpe.soma(0.5)._ref_v, prprlist[1].Syn_list[0][1], sec=gpe.soma)
                    self.prnclist.append(prnc)
                    
        print(f"List of inhibitory connections between the GPe cell and the STN cell in its own channel: {self.stn_cons} \n")
        print(f"List of inhibitory connections between the GPe cell and the subsequent neighbouring channel: {self.nclist} \n")
        print(f"List of inhibitory connections between the GPe cell and the previous neighbouring channel: {self.pnclist} \n")
        print(f"List of inhibitory connections between the GPe cell and the succeeding neighbouring channel: {self.nnclist} \n")
        print(f"List of inhibitory connections between the GPe cell and the preceding neighbouring channel: {self.prnclist} \n")

        # for connect in self.stn_cons:
        #     for netcon in connect:
        #         source, target = netcon.preseg(), netcon.postseg()
        #         print(source, target)
            # Print a list of each source and its target in the NetCon list to validate
            # connections are correct
    def set_netcons(self):
        
        stngpew = 1e-6
        gpegpew = 1e-3
        gpestnw = 1e-3
        
        stngpedel = 0 * ms
        gpegpedel = 0 * ms
        gpestndel = 0 * ms

        for exc_netcon in self.exc_cons:
            exc_netcon.delay = stngpedel
            exc_netcon.weight[0] = stngpew
            
        for nb_netcon in self.nb_cons:
            nb_netcon.delay = gpegpedel
            nb_netcon.weight[0] = gpegpew
            
        for conlist in self.stn_cons:
            for stn_con in conlist:
                stn_con.delay = gpestndel
                stn_con.weight[0] = gpestnw

        for nc_con in self.nclist:
            nc_con.delay = gpegpedel
            nc_con.weight[0] = gpegpew
        
        for pnc_con in self.pnclist:
            pnc_con.delay = gpegpedel
            pnc_con.weight[0] = gpegpew

        for nnc_con in self.nnclist:
            nnc_con.delay = gpegpedel
            nnc_con.weight[0] = gpegpew

        for prnc_con in self.prnclist:
            prnc_con.delay = gpegpedel
            prnc_con.weight[0] = gpegpew
