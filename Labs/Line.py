import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c
from Labs.Node import *
from Labs.Signal_information import *


class Line(object):

    def __init__(self,line_dict):
        self._label=line_dict['label']
        self._lenght=line_dict['lenght']
        self._state=['free']*10 #Lab5 trasformato il campo in vettore
        self._successive={} #Node

    @property
    def label(self):
        return self._label

    @property
    def lenght(self):
        return self._lenght

    @property       #Lab4
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        #state = state.lower().strip()
        state = [s.lower().strip() for s in state] #aggiunta in Lab5
        #if state in ['free', 'occupied']:vecchia condizione
        if set(state).issubset(set(['free', 'occupied'])): #Modifica Lab5, dovuto da aggiornamento a vettore
            self._state = state
        else:
            print('ERROR: line state not recognized.Value:', set(state) - set(['free', 'occupied'])) #aggiunta a Lab5
            #print('ERROR: line state not recognized.Value:', state) vecchia condizione

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self,successive):
        self._successive=successive

    def latency_generation(self):
        latency=self._lenght/(c*2/3)
        return latency

    def noise_generation(self,signal_power):
        noise=signal_power/(2*self._lenght)
        return noise

    def propagate(self,lightpath,occupation=False): #sostituito SignalInformation con Lightpath Lab5
        #latency
        latency=self.latency_generation()
        lightpath.add_latency(latency)

        #noise
        signal_power= lightpath.signal_power
        noise=self.noise_generation(signal_power)
        lightpath.add_noise(noise)

        #state
        if occupation:  #Condizione aggiornata da Lab5
            channel = lightpath.channel
            new_state = self.state.copy()
            new_state[channel] = 'occupied'
            self.state = new_state

        node=self.successive[lightpath.path[0]]
        lightpath=node.propagate(lightpath,occupation)
        return lightpath
