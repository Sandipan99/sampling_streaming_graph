import sampling.variables as vb

def both_in_l(u,v):
	print "both the nodes "+str(u)+" "+str(v)+" are in buffer"
	vb.l[u]+=1
	vb.l[v]+=1
	
