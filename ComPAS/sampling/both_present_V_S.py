import sampling.variables as vb
import community
from copy import deepcopy

def both_present_V_S(u,v):
	u_c=vb.partition[u]   # u_c community of u in the current sample
	v_c=vb.partition[v]   # v_c community of v in the current sample
	if(u_c==v_c):  # case 1.1 when u and v both belong to the same community
		print "both "+str(u)+" "+str(v)+" are present in the same community"
		if(u_c not in vb.edge_count_part): 
			part_intm=[]
			for key in vb.partition:
				if(vb.partition[key]==u_c):
					part_intm.append(key)
			edge_count=0
			for edge in vb.E_S:
				temp1=edge.split("\t")
				#if((int(temp1[0]) in part_intm)and(int(temp1[1]) in part_intm)):
				if((vb.partition[int(temp1[0])]==u_c)and(vb.partition[int(temp1[1])]==u_c)):
					edge_count+=1
			n=len(part_intm)
			vb.node_count_part[u_c]=n
			vb.edge_count_part[u_c]=edge_count
			n=n*(n-1)/2
			edge_density=float(edge_count)/n  # calculate edge density of the partition
		else:
			n=vb.node_count_part[u_c]
			n=n*(n-1)/2
			edge_density=float(vb.edge_count_part[u_c])/n
		if(edge_density<vb.edge_density_th):
			vb.E_S.append(str(u)+"\t"+str(v))    #add edge to the sample
			vb.G.add_edge(u,v)  # add aedge to the graph
			vb.modularity_val=community.modularity(vb.partition,vb.G) #recalculate modularity
			vb.deg_node[u]+=1
			vb.deg_node[v]+=1
			vb.edge_count_part[u_c]+=1
		#else:
		#	print "no edge added as the edge density is above threshold"
			#continue         #ignore 


	else:        # case 1.2 when u and v belong to two different communities 
			# case 1.2.1  check whether by putting u in v's community the modularity increases
		print "the nodes "+str(u)+" "+str(v)+" belong to two different communities"
		partition_intm_1=deepcopy(vb.partition)
		vb.G.add_edge(u,v)
		partition_intm_1[u]=v_c
		mod_val_1=community.modularity(partition_intm_1,vb.G)
		mod_val_c=vb.modularity_val
		intm=[]
		intm1=[]
		intm.append(u)
		while(mod_val_1>mod_val_c):
			for i in intm:
				for n in vb.G.neighbors(i):
					partition_intm_1[n]=v_c
					intm1.append(n)
			intm=[]
			intm=deepcopy(intm1)
			intm1=[]
			mod_val_c=mod_val_1
			mod_val_1=community.modularity(partition_intm_1,vb.G)
			
			#case 1.2.2 check whether by putting v in u's community the modularity increases
		partition_intm_2=deepcopy(vb.partition)
		partition_intm_2[v]=u_c
		mod_val_2=community.modularity(partition_intm_2,vb.G)
		mod_val_c=vb.modularity_val
		intm=[]
		intm1=[]
		intm.append(v)
		while(mod_val_2>mod_val_c):
			for i in intm:
				for n in vb.G.neighbors(i):
					partition_intm_1[n]=u_c
					intm1.append(n)
			intm=[]
			intm=deepcopy(intm1)
			intm1=[]
			mod_val_c=mod_val_2
			mod_val_2=community.modularity(partition_intm_2,vb.G)

			#case 1.2.3 check whether there is a split and a new community is formed
		partition_intm_3=deepcopy(vb.partition)
	
		intm=[]
		intm1=[]
		partition_intm_3[u]=vb.max_part_num+1
		partition_intm_3[v]=vb.max_part_num+1
		intm.append(u)
		intm.append(v)
		mod_val_3=community.modularity(partition_intm_3,vb.G)
		mod_val_c=vb.modularity_val

		while(mod_val_3>mod_val_c):
			for i in intm:
				for n in vb.G.neighbors(i):
					partition_intm_1[n]=u_c
					intm1.append(n)
			intm=[]
			intm=deepcopy(intm1)
			intm1=[]
			mod_val_c=mod_val_3
			mod_val_3=community.modularity(partition_intm_3,vb.G)

		intm=[vb.modularity_val,mod_val_1,mod_val_2,mod_val_3]
		if(max(intm)==vb.modularity_val):
			vb.G.remove_edge(u,v)
		else:
			vb.modularity_val=max(intm)
			vb.deg_node[u]+=1
			vb.deg_node[v]+=1
			vb.E_S.append(str(u)+"\t"+str(v))
			if(max(intm)==mod_val_1):
				vb.partition=deepcopy(partition_intm_1)
			elif(max(intm)==mod_val_2):
				vb.partition=deepcopy(partition_intm_2)
			else:
				vb.partition=deepcopy(partition_intm_3)
				vb.max_part_num+=1


