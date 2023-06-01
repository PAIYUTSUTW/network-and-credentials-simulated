import setting_environment 
import random
import networkx as nx
import numpy as np
import pickle
import utils
import queue
from collections import deque

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
        bfs_trace = []
        while num != len(self.start):
        # while num != 5:
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
                        store_list = set()
                        original = set()
                        original = [*credlist]
                        # bfs_trace.append([node, neighbor,[*credlist]])
                        for k in self.G.nodes[neighbor].items():
                            if set([k[0]]).intersection(credlist):
                                klist.update(k[0])
                                output[node].append([neighbor,k[0],'Success'])
                                credlist.update(k[1])
                                store_list.update(k[1])
                                # bfs_trace.append([node, neighbor,[*credlist]])
                                if_in = True
                                # print(f'{len(credlist)} cred in ')
                            # else:
                            #     output[node].append([neighbor,k[0],'Failed'])
                        bfs_trace.append([node, neighbor,original,[*store_list]])
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
                num = 0
            if num == len(self.start)-1 and len(list(credlist))!= 5000:
                num = 0
            if len(result) == len(node_list) and len(list(credlist)) == len(self.credlist):
                break
            
            
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
        
        
        return output_list, [credlist],result, bfs_trace
    

    def gat_probility(self,super,admin,user,trace):
        
        super_set, admin_set, user_set = set(super), set(admin), set(user)


        all_trace = deque()
        count = 0

        credd = {}
        for cc in super_set:
            credd[cc]=0
        for cc in admin_set:
            credd[cc]=1
        for cc in user_set:
            credd[cc]=2

        def process_trace(t):
            credll = set()
            for c in self.G.nodes[t[1]].items(): # get all cred in node t[1]
                credll.update(c[1])
            credlll = [*credll]
            # credlll = t[3]
            credlist = [*t[2]] # the creds attacker have


            # access = {k: [] for k in credlist}

            if len(credlll) == 0:
                access = np.zeros([1])
                access[0] = None
            
            else:
                access = np.zeros([len(credlist),len(credlll)])
                for i, c in enumerate(credlist):
                    for j, cll in enumerate(credlll):
                        if credd[c] == 0:
                            access[i,j] = 1
                        elif  credd[c] == 1:
                            access[i,j] = round(random.uniform(0.9, 0.4), 2)
                        elif  credd[c] == 2:
                            access[i,j] = round(random.uniform(0.3, 0.1), 2)
                        # access[c].append(temp)

            return access

        cred_credd = []
        cred_cred = []
        for t in trace:
            cred_cred = []
            credll = set()
            for c in self.G.nodes[t[1]].items(): # get all cred in node t[1]
                credll.update(c[1])
            credlll = [*credll]
            credlist = [*t[2]] # the creds attacker have
            cred_cred = [credlist]
            cred_cred.append(credlll)
            cred_credd.append(cred_cred)

        save_name = rf'probability/cred'
        self.loader.save_as_pickle(cred_credd,save_name)
        # with open(f'test/cred.pickle', 'wb') as f:
        #         pickle.dump(cred_credd, f)

        trace_path=[]
        for t in trace:
            tem = [t[0],t[1]]
            trace_path.append(tem)
        save_name = rf'probability/bfs_path'
        self.loader.save_as_pickle(trace_path,save_name)

        prin = 0
        for t in trace:
            access = process_trace(t)
            all_trace.append(list(access))
            print(prin)
            prin+=1

            if len(all_trace) >= 300:
                save_name = rf'probability/{count}'
                self.loader.save_as_pickle(all_trace,save_name)
                # with open(f'test/{count}.pickle', 'wb') as f:
                #     pickle.dump(all_trace, f)
                count+=1
                all_trace=[]

        # with open(f'test/{count}.pickle', 'wb') as f:
        #     pickle.dump(all_trace, f)
        save_name = rf'probability/{count}'
        self.loader.save_as_pickle(all_trace,save_name)



    




