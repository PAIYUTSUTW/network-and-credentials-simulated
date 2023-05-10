import random
import networkx as nx
import numpy as np
import utils
class set_environment:
    def __init__(self, machine_num):
        
        self.machine_num = machine_num
        self.ramdomly_building_edge()



        # self.G = nx.random_internet_as_graph(self.machine_num)
        # self.ramdomly_building_edge_AS()
        
        self.setting_creds()
        self.distributing_creds()
        self.loader = utils.uti()
        self.loader.dump_graph(self.G)
        # self.save_creddict_as_csv()


    def ramdomly_building_edge_AS(self):
        
        for g in self.G.nodes():
            if 'type' in  self.G.nodes[g]:
                del self.G.nodes[g]['type']
            if 'peers' in self.G.nodes[g]:
                del self.G.nodes[g]['peers']

        computers = ["comp" + str(i) for i in range(0, self.machine_num)]
        mapping = dict(zip(self.G, computers))
        self.G = nx.relabel_nodes(self.G, mapping)

    
    def ramdomly_building_edge(self):
        computers = ["comp" + str(i) for i in range(0, self.machine_num)]
        self.G = nx.Graph()
        self.G.add_nodes_from(computers)
        while not nx.is_connected(self.G):
            computer1 = random.choice(computers)
            computer2 = random.choice(computers)
            if computer1 != computer2 and not self.G.has_edge(computer1, computer2):
                self.G.add_edge(computer1, computer2)
    
    def get_graph(self):
        return self.G
    
    def get_cred_and_startpoint(self):
        return self.credentials, self.user_machine
    
    def generating_cred(self,creating_cred_num): # generating a list of cred
        credentials = ["cred" + str(i) for i in range(0, creating_cred_num)]
        random.shuffle(credentials)
        length_cred = len(credentials)
        self.superuser = credentials[0:int(length_cred*0.3)] #taking 3/10 as super cred
        self.administrative = credentials[int(length_cred*0.3):int(length_cred*0.9)]#taking 6/10 as admin cred
        self.user = credentials[int(length_cred*0.9):]#taking 1/10 as user cred
        self.credentials = credentials
    
    def setting_creds(self):
        #########################################################################
        #cred a a dict to telling which cred can be use to get whcih set of creds
        #For example this function would create a dict in below format
        #cred1:cred5,cred7,cred9
        #cred2:cred6,cred11,cred12
        #cre88:........
        #cred100:......
        #########################################################################
        self.generating_cred((self.machine_num*5))#the number of cred is machine * 5
        self.dict_of_supercred={}
        self.dict_of_admincred={}
        self.dict_of_usercred={}
        # len_of_user=int(len(self.user))
        #selecting using which supercred can retrieve which admincreds and usercreds # it will be duplicated
        for cred in self.superuser:
            len_of_user=int(len(self.user))
            len_of_admin=int(len(self.administrative))
            temp=random.choices(self.user,k=random.randint(int(len_of_user*0.05),int(len_of_user*0.1)))
            temp.extend(random.choices(self.administrative,k=random.randint(int(len_of_admin*0.02),int(len_of_admin*0.07))))
            self.dict_of_supercred[cred]=temp
        
        for cred in self.administrative:
            rand_num = random.randint(0,5)
            len_of_user=int(len(self.user))
            len_of_admin=int(len(self.administrative))
            temp=random.choices(self.user,k=random.randint(int(len_of_user*0.01),int(len_of_user*0.06)))
            temp.extend(random.choices(self.administrative,k=random.randint(int(len_of_admin*0.01),int(len_of_admin*0.04))))
            if rand_num == 0:
                temp.extend(random.choices(self.superuser,k=random.randint(int(len_of_admin*0.01),int(len_of_admin*0.1))))
            self.dict_of_admincred[cred]=temp
        
        for cred in self.user:
            rand_num = random.randint(0,5)
            len_of_user=int(len(self.user))
            temp=random.choices(self.user,k=random.randint(int(len_of_user*0.01),int(len_of_user*0.06)))
            if rand_num == 0:
                temp.extend(random.choices(self.administrative,k=random.randint(int(len_of_admin*0.01),int(len_of_admin*0.1))))
            self.dict_of_usercred[cred]=temp

    def get_cred_dict(self):
        self.loader.save_as_pickle(self.dict_of_supercred,'highest_level_credential')
        self.loader.save_as_pickle(self.dict_of_admincred,'middle_level_credential')
        self.loader.save_as_pickle(self.dict_of_usercred,'lowest_level_credential')
        return self.dict_of_supercred, self.dict_of_admincred, self.dict_of_usercred
    
    # def save_creddict_as_csv(self):
    #     row = []
    #     credlis = []
    #     for dic in self.dict_of_supercred.items():
    #         row.append(dic[0])
    #         credlis.append(dic[1])
        
    #     utils.save_as_csv(row,credlis,'supercred')
        


    
    def get_random_num(self,start,end):
        return random.randint(start,end)

    
    def machine_randomly_choice_cred(self,machine,credlist):
        len_of_mach=len(machine)
        listDict = {}
        for i in range(0, len_of_mach):
            listDict["Computer"+str(i)] = []

        # print(len_of_mach)
        for cred in credlist.items():
            listDict[f'Computer{random.randint(0,len_of_mach-1)}'].append(cred)#not all computer #must be revsied
        
        
        
        for m,di in zip(machine,listDict.items()):
            for j in range(len(di[1])):
                self.G.nodes[m][di[1][j][0]] = di[1][j][1]

        # return listDict




    def machine_randomly_choice_part(self,credlist,part):
        keys=list(credlist.keys())
        random.shuffle(keys)
        di=[(key, credlist[key]) for key in keys]
        di=dict(di[0:int(len(di)*part)])

        return di


    
    def distributing_creds(self):
        supermachine=[]
        admin_machine=[]
        user_machine=[]
        degreee_of_nodes = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        for i,mach in enumerate(degreee_of_nodes): # according degree to assign the level of machines
            if i < int(self.machine_num*0.05):
                supermachine.append(degreee_of_nodes[i][0])
            if mach[1] >= 2 and i> int(self.machine_num*0.05):
                admin_machine.append(degreee_of_nodes[i][0])
            if mach[1] == 1 and i> int(self.machine_num*0.05):
                user_machine.append(degreee_of_nodes[i][0])
        
        
        self.machine_randomly_choice_cred(supermachine,self.dict_of_supercred)
        di=self.machine_randomly_choice_part(self.dict_of_admincred,0.2)
        self.machine_randomly_choice_cred(supermachine,di)





        self.machine_randomly_choice_cred(admin_machine,self.dict_of_admincred)
        di=self.machine_randomly_choice_part(self.dict_of_usercred,0.1)
        self.machine_randomly_choice_cred(admin_machine,di)

        self.machine_randomly_choice_cred(user_machine,self.dict_of_usercred)

        self.user_machine = user_machine




        
        
    

