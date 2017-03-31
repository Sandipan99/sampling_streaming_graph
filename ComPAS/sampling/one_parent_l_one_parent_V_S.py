import sampling.variables as vb
import gen_func as gf
import community
import sampling.both_in_l as bil
import sampling.both_present_V_S as bpvs

def del_node_edge_from_sample(y):
	edg=[]
	ind=gf.find_min(vb.deg_node)
	while(ind==y):
		ind=gf.find_min(vb.deg_node)	
	del vb.deg_node[ind]
	vb.V_S.remove(ind)
	del vb.partition[ind]
	for ed in vb.E_S:
		temp2=ed.split("\t")
		if((int(temp2[0])==ind)or(int(temp2[1])==ind)):
			edg.append(ed)
			if(int(temp2[0])==ind):
				vb.deg_node[int(temp2[1])]-=1
			else:
				vb.deg_node[int(temp2[0])]-=1

	for e in edg:
		vb.E_S.remove(e)
		temp2=e.split("\t")
		try:
			vb.G.remove_edge(int(temp2[0]),int(temp2[1]))
		except:
			continue

	vb.G.remove_node(ind)



def one_parent_l_one_parent_V_S(u,v,x,y):
	print str(x)+" parent of "+str(u)+" is in buffer but "+str(y)+" parent of "+str(v)+" is in V_S"
	#print "four new nodes to be inserted"
	#print "Size of sample before: "+str(len(vb.V_S))	
	if len(vb.V_S)>=vb.samp_size:
		#print "sample size: "+str(len(vb.V_S))
		del_node_edge_from_sample(y)
		#print "sample size after deletion: "+str(len(vb.V_S))
	vb.V_S.append(v)
	del vb.l[v]
	vb.E_S.append(str(v)+"\t"+str(y))
	vb.G.add_edge(y,v)
	vb.deg_node[y]+=1
	vb.deg_node[v]=1
	vb.partition[v]=vb.partition[y]


	if (x in vb.l)and(u in vb.l):
		bil.both_in_l(x,u)
	elif (x in vb.V_S)and(u in vb.l):
		if len(vb.V_S)>=vb.samp_size:
			#print "sample size: "+str(len(vb.V_S))
			del_node_edge_from_sample(x)
			#print "sample size after deletion: "+str(len(vb.V_S))
		vb.V_S.append(u)
		del vb.l[u]
		vb.E_S.append(str(u)+"\t"+str(x))
		vb.G.add_edge(u,x)
		vb.deg_node[u]=1
		vb.deg_node[x]+=1
		vb.partition[u] = vb.partition[x]
		vb.modularity_val=community.modularity(vb.partition,vb.G)
	elif (x in vb.V_S)and(u in vb.V_S):
		bpvs.both_present_V_S(x,u)
	elif (x in vb.l)and(u in vb.V_S):
		if(len(vb.V_S)>=vb.samp_size):
			#print "full_sample_size reached"
			#print "sample size: "+str(len(V_S))
			edg=[]
			ind=gf.find_min(vb.deg_node)
			while(ind==u):
				ind=gf.find_min(vb.deg_node)	
			del vb.deg_node[ind]
			vb.V_S.remove(ind)
			del vb.partition[ind]
			for ed in vb.E_S:
				temp2=ed.split("\t")
				if((int(temp2[0])==ind)or(int(temp2[1])==ind)):
					edg.append(ed)
					if(int(temp2[0])==ind):
						vb.deg_node[int(temp2[1])]-=1
					else:
						vb.deg_node[int(temp2[0])]-=1

			for e in edg:
				vb.E_S.remove(e)
				temp2=e.split("\t")
				try:
					vb.G.remove_edge(int(temp2[0]),int(temp2[1]))
				except:
					continue
			vb.G.remove_node(ind)
			#print "sample size after deletion: "+str(len(vb.V_S))

		vb.V_S.append(x)
		del vb.l[x]
		vb.deg_node[x]=1
		vb.deg_node[u]+=1
		vb.E_S.append(str(x)+"\t"+str(u))
		vb.G.add_edge(u,x)
		vb.partition[x] = vb.partition[u]
	else:
		print "this should not print"
	
	#print "Size of sample after: "+str(len(vb.V_S))
