import sampling.variables as vb 
import networkx as nx
import community
from multiprocessing import Process
import sampling.both_present_V_S as bpvs
import sampling.one_V_S_one_new as ovson
import sampling.one_l_one_new as olon
import sampling.both_not_in_l as bnil
import sampling.one_V_S_one_l as ovsol
import sampling.both_in_l as bil
import sampling.gen_func as gf
import sys
import pickle


def mod_opt_sampling(file_name,samp_rate,pop_size,alpha,t_end,ed_th,buff_len,part):
	
	vb.samp_size = int(samp_rate*pop_size) # number of nodes (input from user)

	t_start = 1
	flag = 0 

	vb.edge_density_th = ed_th # input from the user

	temp = []
	temp1 = []

	vb.buf_len = buff_len 


	fs=open(file_name)

	for line in fs:
		line=line.replace("\n","")
		temp=line.split("\t")
		if((int(temp[0])>=t_start)and(int(temp[0])<t_end)):
			u=int(temp[1])   # (u,v) edge is streamed at time t
			v=int(temp[2])
			e=temp[1]+"\t"+temp[2]
			e1=temp[2]+"\t"+temp[1]	
			if(len(vb.V_S)<int(alpha*vb.samp_size)):
				if(u not in vb.V_S):
					vb.V_S.append(u)
					vb.deg_node[u]=0
				if(v not in vb.V_S):
					vb.V_S.append(v)
					vb.deg_node[v]=0
				if((e not in vb.E_S)and(e1 not in vb.E_S)):
					vb.E_S.append(e)
					vb.deg_node[u]+=1
					vb.deg_node[v]+=1
				flag=1
			if((len(vb.V_S)>=int(alpha*vb.samp_size))and(flag==1)):
				flag=0
				print "initial sample formed: now community detection is executed"
				for edge in vb.E_S:
					temp1=edge.split("\t")
					vb.G.add_edge(int(temp1[0]),int(temp1[1]))
				vb.partition=community.best_partition(vb.G) 
				vb.modularity_val=community.modularity(vb.partition,vb.G)
				for key in vb.partition:
					if(vb.partition[key] > vb.max_part_num):
						vb.max_part_num=vb.partition[key]
				part.append(vb.partition)
				print "partition: "+str()
				print "initial partition created"

			else: 
				if int(temp[0])%50 == 0:
					part.append(vb.partition)
				if((e not in vb.E_S)and(e1 not in vb.E_S)):  #checking whether the edge is already present in the sample
					print "streaming edge: "+e+" time: "+temp[0] 
					if((u in vb.V_S)and(v in vb.V_S)):
						print "case1"
						bpvs.both_present_V_S(u,v)
					elif((u not in vb.l)and(u not in vb.V_S)and(v in vb.V_S)):
						print "case2"
						ovson.one_V_S_one_new(u,v)
					elif((u not in vb.l)and(u not in vb.V_S)and(v in vb.l)):
						print "case3"
						olon.one_l_one_new(u,v)
					elif((v not in vb.l)and(v not in vb.V_S)and(u in vb.V_S)):
						print "case4"
						ovson.one_V_S_one_new(v,u)
					elif((v not in vb.l)and(v not in vb.V_S)and(u in vb.l)):
						print "case5"
						olon.one_l_one_new(v,u)	
					elif((u not in vb.l)and(u not in vb.V_S)and(v not in vb.l)and(v not in vb.V_S)):
						print "case6"
						bnil.both_not_in_l(u,v)
					elif((u in vb.l)and(v in vb.V_S)):
						print "case7"
						ovsol.one_V_S_one_l(u,v)
					elif((v in vb.l)and(u in vb.V_S)):
						print "case8"
						ovsol.one_V_S_one_l(v,u)	
					elif((u in vb.l)and(v in vb.l)):
						print "case9"
						bil.both_in_l(u,v)
					else:

						continue
		else:
			break

	fs.close()
	print "found sample"
	print "printing to file"
	ft=open("sampled_network.txt","w")

	for line in nx.generate_edgelist(vb.G):
		temp=line.split(" ")
		ft.write(temp[0]+"\t"+temp[1])
		ft.write("\n")

	ft.close()

	ft=open("partition_file.txt","w")

	for key in vb.partition:
		if key in vb.V_S:
			ft.write(str(key)+"\t"+str(vb.partition[key]))
			ft.write("\n")

	ft.close()

	ft = open("partition_evolution","w")

	pickle.dump(part,ft)

	ft.close()

if __name__=="__main__":

	vb.init()  # defining the global variable
	part = []
	samp_rate = float(sys.argv[3])
	file_name = sys.argv[1]
	pop_size = int(sys.argv[2])
	alpha = 0.4
	t_end = int(sys.argv[4])
	ed_th = 0.5
	buff_len = int(0.0075*samp_rate*pop_size)

	mod_opt_sampling(file_name,samp_rate,pop_size,alpha,t_end,ed_th,buff_len,part)
	

