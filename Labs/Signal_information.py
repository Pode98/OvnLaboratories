import json
import numpy as np
import matplotlib.pyplot as plt

class Lightpath(object):  #Lab5 definita nuova classe
    def __init__(self, power, path, channel):
        self._sig_power = power
        self._path = path
        self._channel = channel
        self._noise_power = 0
        self._latency = 0
        self.Rs = 32.0e9
        self.df = 50.0e9

    @property
    def signal_power(self):
        return self._sig_power

    def set_signal_power(self, value):
        self._sig_power = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def channel(self):
        return self._channel

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value):
        self._noise_power = value

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value):
        self._latency = value

    def add_noise(self, value):
        self.noise_power += value

    def add_latency(self, value):
        self.latency += value

    def next(self):
        self.path = self.path[1:]

class SignalInformation(object):
    def __init__(self,power,path):
        self._signal_power=power
        self._path=path
        self._noise_power=0
        self._latency=0

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,path):
        self._path=path

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self,noise):
        self._noise_power=noise

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,latency):
        self._latency=latency

    def add_noise(self,noise):
        self._noise_power+=noise

    def add_latency(self,latency):
        self._latency+=latency

    def next(self):
        self.path=self.path[1:]
