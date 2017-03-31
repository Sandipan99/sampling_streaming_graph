import sampling.variables as vb
import networkx as nx
import community
import gen_func as gf

def one_l_one_new(u,v):
	print str(u)+ " is not in V_S or in buffer but "+str(v)+" is in buffer"
	#print "Size of sample before: "+str(len(vb.V_S))
	vb.l[u] = 1
	vb.parent[u] = v
	vb.l[v]+= 1
	if(gf.check_full(vb.l)==1):	
		v = gf.elem_to_remove(vb.l)
		if((vb.parent[v] in vb.l)and(vb.parent[v] not in vb.V_S)):
			#print "two new nodes to be inserted"
			if(len(vb.V_S)>=vb.samp_size):
				#print "sample size before deletion: "+str(len(vb.V_S))
				for i in xrange(2):
					edg=[]
					ind=gf.find_min(vb.deg_node)
					while(ind==vb.parent[v]):
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
				#print "sample size before deletion: "+str(len(vb.V_S))
			vb.V_S.append(vb.parent[v])
			vb.V_S.append(v)
			vb.E_S.append(str(v)+"\t"+str(vb.parent[v]))
			vb.G.add_edge(v,vb.parent[v])
			del vb.l[v]
			del vb.l[vb.parent[v]]
			vb.deg_node[v]=1
			vb.deg_node[vb.parent[v]]=1
			vb.partition[v]=vb.max_part_num+1
			vb.partition[vb.parent[v]]=vb.max_part_num+1
			vb.max_part_num+=1
		elif(vb.parent[v] in vb.V_S):
			if(vb.parent[v] in vb.l):
				del vb.l[vb.parent[v]]
			#print "one new node to be inserted"
			if(len(vb.V_S)>=vb.samp_size):
				#print "sample size: "+str(len(vb.V_S))
				edg=[]
				ind=gf.find_min(vb.deg_node)
				while(ind==vb.parent[v]):
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
			vb.deg_node[v]=1
			vb.V_S.append(v)
			vb.E_S.append(str(v)+"\t"+str(vb.parent[v]))
			vb.G.add_edge(v,vb.parent[v])
			del vb.l[v]
			vb.deg_node[vb.parent[v]]+=1
			vb.partition[v]=vb.partition[vb.parent[v]]

		else:
			# parent got deleted....remove it from the buffer
			del vb.l[v]
		vb.modularity_val=community.modularity(vb.partition,vb.G)
	#print "Size of sample after: "+str(len(vb.V_S))
