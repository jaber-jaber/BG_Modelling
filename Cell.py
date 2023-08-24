from neuron import h

class Cell():
    # Cell template. All other cells in this model will inherit from Cell.

    def __init__(self, x, y, z, theta):

        # Cell in 3D space
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.soma = None
        self.Syn_list = []

        self.create_sections()
        self.define_biophysics()
        self.build_subsets()
        self.define_geometry()
        self._rotate_z(theta)
        self._set_position(x, y, z)

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

    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)


    def _set_position(self, x, y, z):
        for sec in self.all:
            for i in range(sec.n3d()):
                sec.pt3dchange(
                    i,
                    x - self.x + sec.x3d(i),
                    y - self.y + sec.y3d(i),
                    z - self.z + sec.z3d(i),
                    sec.diam3d(i),
                )
        self.x, self.y, self.z = x, y, z

    def _rotate_z(self, theta):
        """Rotate the cell about the Z axis."""
        for sec in self.all:
            for i in range(sec.n3d()):
                x = sec.x3d(i)
                y = sec.y3d(i)
                c = h.cos(theta)
                s = h.sin(theta)
                xprime = x * c - y * s
                yprime = x * s + y * c
                sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))
    # def get_spikes(self):
    #     spiketrain = []
    #     return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)

    # def current_clamp(self):
    #     stim = h.IClamp(self.soma(self.loc))
    #     stim.delay = self.delay
    #     stim.dur = self.dur
    #     stim.amp = self.amp
        
    #     return stim