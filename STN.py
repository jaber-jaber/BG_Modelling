from neuron import h
from Cell import Cell
import textwrap

class STN(Cell):
    name = "STN"

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)

    def define_geometry(self):
        self.soma.L = self.soma.diam = 22.5
        self.shape_3D()

    def define_biophysics(self):
        #self.soma.Ra = 660
        self.soma.nseg = 1
        self.soma.cm = 1
        
        self.stim = h.IClamp(0.5, sec=self.soma)
        self.stim.delay = 0
        self.stim.dur = 1e9
        self.stim.amp = 0
        # Area = 1590.43 um2

        # Defining electrophysiological properties
        self.soma.insert('myions')
        # h("ki0_k_ion = 105")
        # h("ko0_k_ion = 3")
        # h("nao0_na_ion = 108")
        # h("nai0_na_ion = 10")
        self.soma.insert('extracellular')

        self.soma.insert('stn')
        h("cai0_ca_ion = 5e-6") # Initial intracellular Ca concentration
        h("cao0_ca_ion = 2") # Initial extracellular Ca concentration
        
        # Rhythmic Spontaneous activity is primarily driven by
        self.soma.gnabar_stn = 49e-3 # Fast sodium channel
        self.soma.gkdrbar_stn = 57e-3 # Delayed rectifier K channel (repolarization)
        self.soma.gkabar_stn = 5e-3 # A-type potassium channel for delaying depolarization

        # Freq of spontaneous activity depends on
        self.soma.gkcabar_stn = 1e-3 # AHP Ca2+-dependent K channel, changed to Otsuka's.
        self.soma.gcalbar_stn = 15e-3 # Long-lasting calcium Ca2+ currents
        self.soma.gcatbar_stn = 5e-3 # Low threshold T-type Ca2+ currents

        # Ca dynamics and leak current
        self.soma.kca_stn = 2 # Ca removal rate
        self.soma.gl_stn = 0.35e-3 # Leak current, changed to Otsuka's. Original value: 0.29e-3 S/cm^2
        