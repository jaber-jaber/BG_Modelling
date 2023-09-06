from neuron import h

class Cell():
    # Cell template. All other cells in this model will inherit from Cell.

    def __init__(self, cid, x, y, z):

        self.cid = cid
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

    def shape_3D(self):
        len1 = self.soma.L
        self.soma.push()
        h.pt3dclear()
        h.pt3dadd(0, 0, 0, self.soma.diam)
        h.pt3dadd(len1, 0, 0, self.soma.diam)
        h.pop_section()

    def create_synapse(self, cell_type):

        if cell_type == 'stn':
            syn = h.GABAa_S(self.soma(0.5))

        self.Syn_list.append(syn)