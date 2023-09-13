from neuron import h
from Cell import Cell
import textwrap

class GPE(Cell):
    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)

    def define_geometry(self):
        self.soma.L = self.soma.diam = 60 # This value will depend on the experimental papers
        # 22.5 is for STN
        self.shape_3D()
        
    def define_biophysics(self):
        #self.soma.Ra = 660
        self.soma.nseg = 1
        self.soma.cm = 1 # Membrane capacitance
        
        # Bias current
        # self.stim = h.IClamp(0.5, sec=self.soma)
        # self.stim.delay = 0
        # self.stim.dur = 1e9
        # self.stim.amp = 10

        # Area = 1590.43 um2
    
        # Defining electrophysiological properties
        self.soma.insert('myions')
        # h("ki0_k_ion = 105")
        # h("ko0_k_ion = 3")
        # h("nao0_na_ion = 108")
        # h("nai0_na_ion = 10")

        self.soma.insert('gpe')
        h("cai0_ca_ion = 5e-6") # Initial intracellular Ca concentration
        h("cao0_ca_ion = 2") # Initial extracellular Ca concentration 
        
        # Rhythmic Spontaneous activity is primarily driven by
        self.soma.gnabar_gpe = 49e-3 # Fast sodium channel (GPE)
        self.soma.gkdrbar_gpe = 57e-3 # Delayed rectifier K channel (repolarization) (GPE)
        self.soma.gkabar_gpe = 5e-3 # A-type potassium channel for delaying depolarization

        # Freq of spontaneous activity depends on
        self.soma.gkcabar_gpe = 1e-3 # AHP Ca2+-dependent K channel, changed to Otsuka's. (GPE)
        self.soma.gcalbar_gpe = 15e-3 # Long-lasting calcium Ca2+ currents
        self.soma.gcatbar_gpe = 5e-3 #Low threshold T-type Ca2+ currents (GPE)

        # Ca dynamics and leak current
        self.soma.kca_gpe = 2 # Ca removal rate (GPE)
        self.soma.gl_gpe = 0.35e-3 # Leak current, changed to Otsuka's. Original value: 0.29e-3 S/cm^2 (GPE)
        