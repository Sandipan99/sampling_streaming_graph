import sampling.variables as vb
import gen_func as gf
import both_present_V_S as bpvs
import one_parent_l_one_parent_V_S as oplopvs
import community
import networkx as nx

def delete_node_from_sample():
	edg=[]
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
def both_not_in_l(u,v):
	print "neither "+str(u)+" nor "+str(v)+" are in V_S or buffer"	
	#print "size of the sample before: "+str(len(vb.V_S))
	if(gf.check_full(vb.l)==1):
		#print "two nodes to be inserted"	
		# inserted the new nodes to the buffer
		a_1 = u
		a_2 = v

		u = gf.elem_to_remove(vb.l)
		v = gf.elem_to_remove(vb.l)

		while (u==v):
			v = gf.elem_to_remove(vb.l)

		x = vb.parent[u]
		y = vb.parent[v]
		#print "selected nodes: "+str(u)+" with parent: "+str(x)
		#print "selected nodes: "+str(v)+" with parent: "+str(y)
		#print "parents are "+str(x)+" "+str(y)
		if((x==v)and(y==u)):
			print "both the parents "+str(x)+" "+str(y)+" are parents of each other"
			if(len(vb.V_S)>=vb.samp_size):
				#print "full_sample_size reached"
				#print "sample size: "+str(len(vb.V_S))
				for i in xrange(2):
					edg=[]
					ind=gf.find_min(vb.deg_node)	
					del vb.deg_node[ind]
					del vb.partition[ind]
					vb.V_S.remove(ind)	
					
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
			vb.V_S.append(v)
			vb.E_S.append(str(u)+"\t"+str(v))
			vb.G.add_edge(u,v)
			del vb.l[u]
			del vb.l[v]
			vb.deg_node[u]=1
			vb.deg_node[v]=1	
			vb.partition[u]=vb.max_part_num+1
			vb.partition[v]=vb.max_part_num+1
			vb.modularity_val=community.modularity(vb.partition,vb.G)
			vb.max_part_num+=1
		elif((x in vb.V_S)and(y in vb.V_S)):
			if(x!=y):
				#print "both the parents "+str(x)+" "+str(y)+" are in V_S"
				if(len(vb.V_S)>=vb.samp_size):
					print "full_sample_size reached"
					print "sample size: "+str(len(vb.V_S))
					for i in xrange(2):
						edg=[]
						ind=gf.find_min(vb.deg_node)
						while((ind==x)or(ind==y)):
							ind=gf.find_min(vb.deg_node)	
						del vb.deg_node[ind]
						del vb.partition[ind]
						vb.V_S.remove(ind)
						
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
				vb.V_S.append(v)
				vb.E_S.append(str(u)+"\t"+str(x))
				vb.E_S.append(str(v)+"\t"+str(y))
				vb.G.add_edge(x,u)
				vb.G.add_edge(y,v)
				del vb.l[u]
				del vb.l[v]
				vb.deg_node[x]+=1
				vb.deg_node[y]+=1
				vb.deg_node[u]=1
				vb.deg_node[v]=1
				vb.partition[u]=vb.partition[x]
				vb.partition[v]=vb.partition[y]
				vb.modularity_val=community.modularity(vb.partition,vb.G)
				#bpvs.both_present_V_S(u,v)	
			else:
				print "both the nodes have same parent and are both in V_S"
				if(len(vb.V_S)>=vb.samp_size):
					#print "full_sample_size reached"
					#print "sample size: "+str(len(vb.V_S))
					for i in xrange(2):
						edg=[]
						ind=gf.find_min(vb.deg_node)
						while(ind==x):
							ind=gf.find_min(vb.deg_node)	
						del vb.deg_node[ind]
						del vb.partition[ind]
						vb.V_S.remove(ind)
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
					#print "removing two nodes from the sample size: "+str(len(vb.V_S))
				vb.V_S.append(u)
				vb.V_S.append(v)
				vb.G.add_edge(x,u)
				vb.G.add_edge(x,v)
				#vb.G.add_edge(u,v)
				del vb.l[u]
				del vb.l[v]
				vb.E_S.append(str(x)+"\t"+str(u))
				vb.E_S.append(str(x)+"\t"+str(v))
				#vb.E_S.append(str(u)+"\t"+str(v))
				vb.deg_node[x]+=2
				vb.deg_node[u]=1
				vb.deg_node[v]=1
				vb.partition[u]=vb.partition[x]
				vb.partition[v]=vb.partition[x]
				vb.modularity_val=community.modularity(vb.partition,vb.G)	
		elif((x in vb.l)and(y in vb.V_S)):
			oplopvs.one_parent_l_one_parent_V_S(u,v,x,y)	
		elif((y in vb.l)and(x in vb.V_S)):
			oplopvs.one_parent_l_one_parent_V_S(v,u,y,x)
		elif((x in vb.l)and(y in vb.l)):
			if(x!=y):
				print "both the parents "+str(x)+" "+str(y)+" are in buffer"
				if(len(vb.V_S)>=vb.samp_size):
					#print "full_sample_size reached"
					#print "sample size: "+str(len(vb.V_S))
					delete_node_from_sample()
					#print "sample size after deletion: "+str(len(vb.V_S))
						
				vb.V_S.append(u)
				if(len(vb.V_S)>=vb.samp_size):
					#print "full_sample_size reached"
					#print "sample size: "+str(len(vb.V_S))
					delete_node_from_sample()
					#print "sample size after deletion: "+str(len(vb.V_S))

				vb.V_S.append(x)

				del vb.l[u]
				del vb.l[x]
				vb.partition[u] = vb.max_part_num+1
				vb.partition[x] = vb.max_part_num+1
				vb.deg_node[u]=1
				vb.deg_node[x]=1
				vb.E_S.append(str(u)+"\t"+str(x))
				vb.G.add_edge(u,x)
				vb.max_part_num+=1
				if (y in vb.V_S)and(v in vb.V_S):
					bpvs.both_present_v_s(v,y) 
				elif (y in vb.V_S)and(v in vb.l):
					if(len(vb.V_S)>=vb.samp_size):
						#print "full_sample_size reached"
						#print "sample size: "+str(len(vb.V_S))
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
						#print "sample size after deletion: "+str(len(vb.V_S))

					vb.V_S.append(v)
					del vb.l[v]
					vb.deg_node[v]=1
					vb.deg_node[y]+=1
					vb.E_S.append(str(v)+"\t"+str(y))
					vb.G.add_edge(v,y)
					vb.partition[v] = vb.partition[y]
				elif (y in vb.l)and(v in vb.l):
					if(len(vb.V_S)>=vb.samp_size):
						#print "sample size before deletion: "+str(len(vb.V_S))
						delete_node_from_sample()
						#print "sample size after deletion: "+str(len(vb.V_S))
					vb.V_S.append(v)
					if(len(vb.V_S)>=vb.samp_size):
						#print "sample size before deletion: "+str(len(vb.V_S))
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
						#print "sample size after deletion: "+str(len(vb.V_S))	
						vb.G.remove_node(ind)
					vb.V_S.append(y)
					del vb.l[v]
					del vb.l[y]
					vb.deg_node[v]=1
					vb.deg_node[y]=1
					vb.E_S.append(str(v)+"\t"+str(y))
					vb.G.add_edge(v,y)
					vb.partition[v] = vb.max_part_num+1
					vb.partition[y] = vb.max_part_num+1
					vb.max_part_num+=1
				elif (y in vb.l)and(v in vb.V_S):
					if(len(vb.V_S)>=vb.samp_size):
						edg=[]
						ind=gf.find_min(vb.deg_node)
						while(ind==v):
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
					vb.V_S.append(y)
					vb.deg_node[y] = 1
					vb.deg_node[v]+= 1
					vb.E_S.append(str(v)+"\t"+str(y))	
					vb.G.add_edge(v,y)
					vb.partition[y] = vb.partition[v]
				else:
					print "this should not print"	
				vb.modularity_val=community.modularity(vb.partition,vb.G)	
			else:
				print "both the nodes have same parent and parent is in buffer"
				if(len(vb.V_S)>=vb.samp_size):
					#print "sample size: "+str(len(vb.V_S))
					for k in xrange(3):
						edg=[]
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

				vb.V_S.append(u)
				vb.V_S.append(v)
				vb.V_S.append(x)
				del vb.l[u]
				del vb.l[v]
				vb.deg_node[u]=1
				vb.deg_node[v]=1
				vb.deg_node[x]=2
				#vb.E_S.append(str(u)+"\t"+str(v))
				vb.E_S.append(str(u)+"\t"+str(x))
				vb.E_S.append(str(v)+"\t"+str(x))
				#vb.G.add_edge(u,v)
				vb.G.add_edge(u,x)
				vb.G.add_edge(v,x)
				del vb.l[x]
				vb.partition[x]=vb.max_part_num+1
				vb.partition[u]=vb.max_part_num+1
				vb.partition[v]=vb.max_part_num+1	
				vb.max_part_num+=1
			vb.modularity_val = community.modularity(vb.partition,vb.G)
			
		else:
			print "deletion of one or both the parents"
			del vb.l[u]
			del vb.l[v]
		vb.l[a_1] = 1
		vb.l[a_2] = 1
		vb.parent[a_1] = a_2
		vb.parent[a_2] = a_1
	
	else:
		vb.l[u]=1
		if gf.check_full(vb.l)==1:
			#print "size of the sample before: "+str(len(vb.V_S))
			x = gf.elem_to_remove(vb.l)
			while x==u:
				x = gf.elem_to_remove(vb.l)
			y = vb.parent[x]
			if y in vb.V_S: # parent in sample V_S
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
					#print "sample size: "+str(len(vb.V_S))
					for k in xrange(2):
						edg=[]
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
					#print "sample size after dletion: "+str(len(vb.V_S))
				vb.V_S.append(x)
				vb.V_S.append(y)
				vb.E_S.append(str(y)+"\t"+str(x))
				vb.G.add_edge(y,x)
				del vb.l[y]
				del vb.l[x]
				vb.deg_node[y] = 1
				vb.deg_node[x] = 1
				vb.partition[x] = vb.max_part_num+1
				vb.partition[y] = vb.max_part_num+1 
				vb.max_part_num+=1
				vb.modularity_val = community.modularity(vb.partition,vb.G)

			else:
				print "This should not print"	

		vb.l[v]=1
		vb.parent[u]=v
		vb.parent[v]=u
	#print "size of the sample after: "+str(len(vb.V_S))
