import setting_environment 
import random
import networkx as nx
import numpy as np
import pickle
import utils
import queue


class attack:
    def __init__(self,graph, credlist,startpoint):
        self.G = graph
        self.credlist = credlist
        self.startpoint = random.choice(startpoint)
        self.start = startpoint[0:10]
        self.loader = utils.uti(True)

    def bfs(self,save_name='result_bfs'):
        bfs_tree = nx.bfs_tree(self.G, self.startpoint)
        s=0
        f=0
        result=[]
        print('attacker is attacking now......')
        steps = bfs_tree.edges()
        for st in steps:
            for cred in self.credlist:
                if cred in self.G.nodes[st[1]]:
                    # print(f'machien: {st[0]}  machine: {st[1]} cred:{cred} Success')
                    result.append([st[0],st[1],cred,'Success'])
                    # dic = {'source_machien': {st[0]},  'target_machien': {st[1]}, 'credential':{cred}, 'result':'Success'}
                    # result.append(dic)
                    # s=s+1
                else:
                    # print(f'machien: {st[0]}  machine: {st[1]} cred:{cred} Failed')
                    result.append([st[0],st[1],cred,'Failed'])
                    # dic = {'source_machien': {st[0]},  'target_machien': {st[1]}, 'credential':{cred}, 'result':'Failed'}
                    # result.append(dic)
                    # f=f+1
        # print(s,f)
        self.loader.save_as_pickle(result,save_name)
        
        header = ['source_machien','target_machien','credential','result']
        self.loader.save_as_csv(header,result,save_name)

        return result
    
    def lazy_bfs(self,save_name='result_bfs_lazy'):

        node_list = list(self.G.nodes())
        if_in = False
        result = []
        # result.append(self.startpoint)
        # output=[]
        output = {}
        for k in self.G.nodes:
            output[k] = []
        credlist = set()
        for s in self.start:
            result.append(s)
            for k in self.G.nodes[s].items():
                credlist.update(k[1])
        # credlist = [*set(credlist)]
        num = 0
        
        while num != len(self.start):
        # while num != 1:
            q = queue.Queue()
            q.put(self.start[num])
            visited = set()

            while not q.empty():
                node = q.get()
                if node not in visited:
                    visited.add(node)
                    # print(node)
                    for neighbor in self.G.neighbors(node):
                        klist=set()
                        for k in self.G.nodes[neighbor].items():
                            if set([k[0]]).intersection(credlist):
                                klist.update(k[0])
                                output[node].append([neighbor,k[0],'Success'])
                                credlist.update(k[1])
                                if_in = True
                                # print(f'{len(credlist)} cred in ')
                            # else:
                            #     output[node].append([neighbor,k[0],'Failed'])
                        for cred in credlist:
                            if {cred}.isdisjoint(klist) :
                                output[node].append([neighbor,cred,'Failed'])

                        # credlist = [*set(credlist)]
                        if if_in is True:
                            if_in = False
                            q.put(neighbor)
            print(f'{len(list(credlist))} I am cred')
            
            result.extend(visited)
            result = [*set(result)]
            # result = [set(node for node in visited)]
            print(f'{len(result)} Iam result')

            if num == len(self.start)-1 and len(result)!=len(node_list):
                num=0
            if num == len(self.start)-1 and len(list(credlist))!= 5000:
                num = 0
            
            
        # with open('result/temp.txt', 'w') as f:
        #     f.write(str(result) + '\n')#


            num += 1
            print(num)
        
        header = ['source_machien','target_machien','credential','result']
        output_list = []
        for value in output.items():
            for va in value[1]:
                v=va.copy()
                v.insert(0,value[0])
                output_list.append(v)


        self.loader.save_as_csv(header,output_list,save_name)
        
        
        return output_list, [credlist],result

    




