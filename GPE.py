from neuron import h
from Cell import Cell
import textwrap

class GPe(Cell):
    name = "GPe"
    
    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)

    def define_geometry(self):
        self.soma.L = self.soma.diam = 29 # Type II GP neuron
        # 22.5 is for STN
        self.shape_3D()
        
    def define_biophysics(self):
        #self.soma.Ra = 660
        self.soma.nseg = 1
        self.soma.cm = 1 # Membrane capacitance (Standard set for GPE)
        
        self.soma.insert('myions')
        self.soma.insert('gpe')
        
        h("cai0_ca_ion = 5e-6") # Initial intracellular Ca concentration
        h("cao0_ca_ion = 2") # Initial extracellular Ca concentration 

        self.soma.gnabar_gpe = 0.04 # Fast sodium channel (GPE)
        self.soma.gkdrbar_gpe = 0.0042 # Delayed rectifier K channel (repolarization) (GPE)

        self.soma.gkcabar_gpe = 0.1e-3 # AHP Ca2+-dependent K channel, changed to Otsuka's. (GPE)
        self.soma.gcatbar_gpe = 6.7e-5 #Low threshold T-type Ca2+ currents (GPE)

        self.soma.kca_gpe = 2 # Ca removal rate (GPE)
        self.soma.gl_gpe = 4e-5 # Leak current, changed to Otsuka's. Original value: 0.29e-3 S/cm^2 (GPE)
        