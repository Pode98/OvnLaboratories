import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c
from Labs.Node import *
from Labs.Line import *
from Labs.Signal_information import *
from Labs.Connections import *


class Network(object):
    def __init__(self):
        self._nodes={}
        self._lines={}
        self._connected = False #Lab4
        self._weighted_paths = None #Lab4
        self._route_space = None #Lab5
        node_json=json.load(open(json.path,'r'))
        for node_label in node_json:
            #create nodes
            node_dict=node_json[node_label]
            node_dict['label']=node_label
            node=Node(node_dict)
            self._nodes[node_label]=node

            #create lines
            for connected_node_label in node_dict['connected_nodes']:
                line_dict={}
                line_label= node_label+connected_node_label
                line_dict['label']=line_label
                node_position=np.array(node_json[node_label]['position'])
                connected_node_position=np.array(node_json[connected_node_label]['position'])
                line_dict['lenght']=np.sqrt(np.sum(node_position-connected_node_position)**2)
                line=line_dict[line_label]
                self._lines[line_label]=line



    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def connected(self):
        return self._connected


    def draw(self):
        nodes=self.nodes
        for node_label in nodes:
            n0=nodes[node_label]
            x0=n0.position[0]
            y0=n0.position[1]
            plt.plot(x0,y0,'go',markersize=10)
            plt.text(x0+20,y0+20,node_label)
            for connected_node_label in n0.connected_nodes:
                n1=nodes[connected_node_label]
                x1=n1.position[0]
                y1=n1.position[1]
                plt.plot([x0,x1],[y0,y1],'b')
        plt.title('Network')
        plt.show()

    def find_paths(self,label1,label2):
        cross_nodes=[key for key in self.nodes.keys() if ((key!=label1)&(key!=label2))]
        cross_lines=self.lines.keys()
        inner_paths={}
        inner_paths['0']=label1
        for i in range(len(cross_nodes)+1):
            inner_paths[str(i+1)]=[]
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i+1)]+=[inner_path + cross_node for cross_node in cross_nodes if ((inner_paths[-1]+cross_node in cross_lines)&(cross_node not in inner_path))]

        paths=[]
        for i in range(len(cross_nodes)+1):
            for path in inner_paths[str(i)]:
                if path[-1] + label2 in cross_lines:
                    paths.append(path+label2)
        return  paths

    def connect(self):
        nodes_dict=self.nodes
        lines_dict=self.lines
        for node_label in nodes_dict:
            node=nodes_dict[node_label]
            for connected_node in node.connected_nodes:
                line_label=node.label+connected_node
                line=lines_dict[line_label]
                line.successive[connected_node]=nodes_dict[connected_node]
                node.successive[line_label]=lines_dict[line_label]
        self._connected = True


    # def propagate(self,signal_information):  #funzione prima di Lab5
    #     path=signal_information.path
    #     start_node=self.nodes[path[0]]
    #     propagated_signal_information=start_node.propagate(signal_information)
    #     return  propagated_signal_information

    def propagate(self,lightpath, occupation=False): #Aggiornata a Lab5
        path=lightpath.path
        start_node=self.nodes[path[0]]
        propagated_lightpath=start_node.propagate(lightpath,occupation)
        return  propagated_lightpath


    #Lab4
    @property
    def weighted_paths(self):
        return self._weighted_paths

    def set_weighted_paths(self, signal_power):#Modifica Lab5 con implementazione route space
        if not self.connected:
            self.connect()
        node_labels = self.nodes.keys()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []

        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node + '->'
                paths.append(path_string[:-2])

                # Propagation
                signal_information = SignalInformation(signal_power, path)
                signal_information = self.propagate(signal_information,occupation=False)
                latencies.append(signal_information.latency)
                noises.append(signal_information.noise_power)
                snrs.append(10 * np.log10(signal_information.signal_power / signal_information.noise_power) )

        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        self._weighted_paths = df
        #Aggiunta da Lab5
        route_space = pd.DataFrame()
        route_space['path'] = paths
        for i in range(10):
            route_space[str(i)] = ['free']*len(paths)
            self._route_space = route_space

    #Lab3 --ridefinita in Lab4 sotto
    #def find_best_latency(self, input_node, output_node):
    #   all_paths = self.weighted_paths.path.values
    #  inout_paths = [path for path in all_paths if ((path[0] == input_node) and (path[-1] == output_node))]
    #    inout_df = self.weighted_paths.loc[
    #        self.weighted_paths.path.isin(inout_paths)]
    #    best_latency = np.min(inout_df.latency.values)
    #    best_path = inout_df.loc[
    #        inout_df.latency == best_latency].path.values[0].replace('->', '')
    #    return best_path

    def stream(self, connections, best='latency'): #Aggiornato a Lab5
        streamed_connections = []
        for connection in connections:
            input_node = connection.input_node
            output_node = connection.output_node
            signal_power = connection.signal_power
            #self.set_weighted_paths(signal_power) Lab3
            self.set_weighted_paths(1)  #Lab4
            if best == 'latency':
                path = self.find_best_latency(input_node, output_node)
            elif best == 'snr':
                path = self.find_best_snr(input_node, output_node)
            else:
                print('ERROR: best input not recognized.Value:', best)
                continue
            # if path: #added condition for Lab4 on the path
            #     in_signal_information = SignalInformation(signal_power, path)
            #     out_signal_information = self.propagate(in_signal_information)
            #     connection.latency = out_signal_information.latency
            #     noise = out_signal_information.noise_power
            #     connection.snr = 10 * np.log10(signal_power / noise)
            if path: #Condiione aggiornata a Lab5
                path_occupancy = self.route_space.loc[self.route_space.path == path].T.values[1:]
                channel = [i for i in range(len(path_occupancy)) if path_occupancy[i] =='free'][0]
                path = path.replace('->', '')
                in_lightpath = Lightpath(signal_power, path, channel)
                out_lightpath = self.propagate(in_lightpath, True)
                connection.latency = out_lightpath.latency
                noise_power = out_lightpath.noise_power
                connection.snr = 10 * np.log10(signal_power / noise_power)
                self.update_route_space(path, channel)
            else:
                connection.snr=0
                connection.latency='None'
            streamed_connections.append(connection)
        return streamed_connections

    #due metodi aggiunti (lab5)
    @staticmethod
    def path_to_line_set(path):
        path = path.replace('->', '')
        return set([path[i] + path[i + 1] for i in range(len(path) - 1)])

    def update_route_space(self, path, channel):
        all_paths = [self.path_to_line_set(p) for p in self.route_space.path.values]
        states = self.route_space[str(channel)]
        lines = self.path_to_line_set(path)
        for i in range(len(all_paths)):
            line_set = all_paths[i]
            if lines.intersection(line_set):
                states[i] = 'occupied'
        self.route_space[str(channel)] = states

    #es7 Lab4
    #Modifica Lab5 es4 in modo da gestire la channel occupancy (tutti e tre i metodi)

    # def available_paths(self, input_node, output_node):    #Funzione da Lab4
    #     if self.weighted_paths is None:
    #         self.set_weighted_paths(1)
    #     all_paths = [path for path in self.weighted_paths.path.values
    #         if ((path[0] == input_node) and (path[-1] == output_node))]
    #     unavailable_lines = [line for line in self.lines
    #         if self.lines[line].state =='occupied']
    #     available_paths = []
    #     for path in all_paths:
    #         available = True
    #         for line in unavailable_lines:
    #             if line[0] + '->' + line[1] in path:
    #                 available = False
    #                 break
    #         if available:
    #             available_paths.append(path)
    #     return available_paths

    def available_paths(self, input_node, output_node): #Funione ridefinita in contesto a Lab5
        if self.weighted_paths is None:
            self.set_weighted_paths(1)
        all_paths = [path for path in self.weighted_paths.path.values
                 if ((path[0] == input_node) and (path[-1] == output_node))]
        available_paths = []
        for path in all_paths:
            path_occupancy = self.route_space.loc[self.route_space.path == path].T.values[1:]
            if 'free' in path_occupancy:
                available_paths.append(path)
        return available_paths

    def find_best_snr(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_snr = np.max(inout_df.snr.values)
            #best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0].replace('->', '')
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0] #da Lab5
        else:
            best_path = None
        return best_path

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_latency = np.min(inout_df.latency.values)
            #best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0].replace('->', '')
            best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0]#da Lab5
        else:
            best_path = None
        return best_path

    #Lab5
    @property
    def route_space(self):
        return self._route_space
