import pickle
import csv
import pandas as pd
import os
import networkx as nx
from natsort import natsorted

class uti:
    def __init__(self,att=False):
        if not os.path.isdir('result'):
                os.mkdir('result')

        lis = natsorted(os.listdir('result'))
        if '0' not in lis and att == False:
            os.mkdir('result/0')
            self.num = 0 
        if '0' in lis and att == False:
            self.num = int(lis[-1])+1
            os.mkdir(f'result/{self.num}')
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