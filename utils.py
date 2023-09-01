import pickle
import csv
import pandas as pd
import os
import networkx as nx
from natsort import natsorted
import pandas

class uti:
    def __init__(self,att=False):
        if not os.path.isdir('result'):
                os.mkdir('result')

        numeric_elements = natsorted(os.listdir('result'))
        lis =  [element for element in numeric_elements if element.strip().lstrip('-').replace('.', '', 1).isdigit()]
        if '0' not in lis and att == False:
            os.mkdir('result/0')
            os.mkdir('result/0/probability')
            self.num = 0 
        if '0' in lis and att == False:
            self.num = int(lis[-1])+1
            os.mkdir(f'result/{self.num}')
            os.mkdir(f'result/{self.num}/probability')
        if att == True:
            self.num = int(lis[-1])

    def save_as_pickle(self,result,save_name):
        with open(f'result/{self.num}/{save_name}.pickle', 'wb') as f:
            pickle.dump(result, f)

    def save_as_csv(self,header, result, save_name):
        # header = ['source_machien','target_machien','credential','result']
        # with open('countries.csv', 'w', encoding='UTF8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(header)
        #     writer.writerow(result)


        writer = pd.DataFrame(columns=header,data=result)
        writer.to_csv(f'result/{self.num}/{save_name}.csv',encoding = 'UTF8')

    def dump_graph(self,G):
        # nx.write_yaml(G, 'result/network_topo.yaml')
        # nx.write_gexf(G, 'result/network_topo.gexf')
        # nx.write_graphml(G, 'result/network_topo.graphml')
        with open(f'result/{self.num}/network_topo.gpickle', 'wb') as f:
            pickle.dump(G, f, pickle.HIGHEST_PROTOCOL) 

    def load_graph(self):
        with open(f'result/{self.num}/network_topo.gpickle', 'rb') as f:
            G = pickle.load(f)

            return G
    
    def get_degrees(self,G):
        degreee_of_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)

        return degreee_of_nodes
    
    def get_hop(self,G):
        degree = self.get_degrees(G)
        hop_lengths = nx.single_source_shortest_path_length(G, degree[0][0])
        self.save_as_pickle(hop_lengths,'hop')

        return hop_lengths
    
    def get_cred_in_comp(self,G):
        dict_comp_cred = {}
        for g in list(G.nodes()):
            temp = set()
            for i in G.nodes[g].items():
                temp.update(set(i[1]))
                # print(len(i[1]))
            dict_comp_cred[g] = [*temp]

        self.save_as_pickle(dict_comp_cred,'comp_cred')

        return dict_comp_cred

