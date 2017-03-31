import sampling.variables as vb
import gen_func as gf
import community

def one_V_S_one_l(u,v):
	print str(u)+" is in the buffer while "+str(v)+" is in V_S"
	#print "onew new node to be inserted"
	#print "size of sample before: "+str(len(vb.V_S))
	del vb.l[u]
	if(len(vb.V_S)>=vb.samp_size):
		#print "sample size: "+str(len(vb.V_S))
		edg=[]
		ind=gf.find_min(vb.deg_node)
		while(ind==v):
			ind=gf.find_min(vb.deg_node)
		vb.V_S.remove(ind)
		del vb.deg_node[ind]
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
	vb.V_S.append(u)
	vb.E_S.append(str(u)+"\t"+str(v))
	vb.partition[u]=vb.partition[v]
	vb.G.add_edge(u,v)
	vb.deg_node[u]=1
	vb.deg_node[v]+=1	
	vb.modularity_val=community.modularity(vb.partition,vb.G)
	#print "size of sample after: "+str(len(vb.V_S))
