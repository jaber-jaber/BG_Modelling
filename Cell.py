from neuron import h

"""
    Base cell class implementation with parameters & code derived from:

    Terman, D., Rubin, J.E., Yew, A.C. and Wilson, C.J., 2002. 
	"Activity patterns in a model for the subthalamopallidal 
	network of the basal ganglia." 
	Journal of Neuroscience, 22(7), pp.2963-2976.

"""

class Cell():
    # Cell template. All other cells in this model will inherit from Cell.

    def __init__(self):

        # Cell in 3D space
        self.x = 0
        self.y = 0
        self.z = 0

        # Defining the soma, array of synapses and "Iscale"
        
        self.soma = None
        self.Syn_list = []
        self.Iscale = 0

        # Cell methods (equivalent of procs in HOC)
        self.create_sections()
        self.define_biophysics()
        self.define_geometry()

    def create_sections(self):
        # Sections in the form of:
        # h.Section(name='soma', cell=self)
        # or h.Section(name='dendrite', cell=self)

        
        raise NotImplementedError("Sections were not created.")

    def define_geometry(self):
        # Set the 3D geometry of the cell.
        raise NotImplementedError("Cell geometries have not been created.")

    def define_biophysics(self):
        # Define biophysics of the cell (assign membrane properties)
        raise NotImplementedError("Biophysics of the cell have not been defined.")

    def self_con(self, threshold=10):
        netcon = h.NetCon(self.soma(0.5)._ref_v, self.soma)
        netcon.threshold = threshold
        return netcon

    def get_spikes(self):
        spiketrain = []
        return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)

    def current_clamp(self):
        stim = h.IClamp(self.soma(self.loc))
        stim.delay = self.delay
        stim.dur = self.dur
        stim.amp = self.amp
        
        return stim

    #def build_subsets(self):
       # self.all = h.SectionList()
       # self.all.wholetree(sec=self.soma)
        
    def set_position(self, x, y, z):
        for sec in self.all:
            for i in range(int(h.n3d())):
                h.pt3dchange(i, \
                    x-self.x3d(i), \
                    y-self.y3d(i), \
                    z-self.z3d(i), \
                    h.diam3d(i))
        self.x = x; self.y = y; self.z = z;

    def shape_3D(self):
        slength = self.soma.L
        self.soma.push()
        h.pt3dclear()
        h.pt3dadd(0, 0, 0, self.soma.diam)
        h.pt3dadd(slength, 0, 0, self.soma.diam)
        h.pop_section()
