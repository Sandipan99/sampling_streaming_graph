import sampling.variables as vb
import gen_func as gf
import community

def one_V_S_one_new(u,v):
	print str(u)+ " is not in V_S or in buffer but "+str(v)+" is in V_S"
	#print "size of the sample before: "+str(len(vb.V_S))
	vb.parent[u]=v 
	if(gf.check_full(vb.l)==1):
		x = gf.elem_to_remove(vb.l)
		y = vb.parent[x]
		if y in vb.V_S: # parent in sample V_S
			#print "one new node to be inserted"
			if(len(vb.V_S)>=vb.samp_size):
				#print "sample size: "+str(len(vb.V_S))
				edg=[]
				ind=gf.find_min(vb.deg_node)
				while(ind==y):
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
			vb.V_S.append(x)
			vb.E_S.append(str(y)+"\t"+str(x))
			vb.G.add_edge(y,x)
			del vb.l[x]
			vb.deg_node[y]+=1
			vb.deg_node[x]=1
			vb.partition[x] = vb.partition[y]
			vb.modularity_val = community.modularity(vb.partition,vb.G)
		elif y in vb.l:
			if(len(vb.V_S)>=vb.samp_size):
				for  i in xrange(2):
					#print "sample size: "+str(len(vb.V_S))
					edg=[]
					ind=gf.find_min(vb.deg_node)
					while(ind==y):
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
			vb.V_S.append(x)
			vb.V_S.append(y)
			vb.E_S.append(str(y)+"\t"+str(x))
			vb.G.add_edge(y,x)
			del vb.l[x]
			del vb.l[y]
			vb.deg_node[y]=1
			vb.deg_node[x]=1
			vb.partition[x] = vb.max_part_num + 1;
			vb.partition[y] = vb.max_part_num + 1;
			vb.max_part_num += 1;
			vb.modularity_val = community.modularity(vb.partition,vb.G)

		else:
			print "parent got deleted"	
	#print "size of the sample after: "+str(len(vb.V_S))
	vb.l[u] = 1
