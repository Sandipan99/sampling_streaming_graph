import networkx as nx
import community
import matplotlib.pyplot as plt
from copy import deepcopy


def distribution(d):
	d.sort()
	count=1
	x_axis=[]
	y_axis=[]
	for i in xrange(len(d)-1):
		if(d[i]==d[i+1]):
			count+=1
		else:
			x_axis.append(d[i])
			y_axis.append(count)
			count=1

	x_axis.append(d[len(d)-1])
	y_axis.append(count)

	plt.xscale('log')
	plt.yscale('log')

	plt.scatter(x_axis,y_axis)
	plt.show()


def median(data):
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise StatisticsError("no median for empty data")
    if n%2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2

fs=open("partition_file_0.3")  # community file in the form #node_id \t #community_id

partition={}
temp=[]

for line in fs:
	line=line.replace("\n","")
	temp=line.split("\t")
	if(temp[1] not in partition):
		partition[temp[1]]=temp[0]+"\t"
	else:
		partition[temp[1]]+=temp[0]+"\t"

fs.close()

node=[]
edge=[]
degree={}


fs=open("found_sample_0.3")  # sample graph in edge list form each line represents an edge in the file

for line in fs:
	line=line.replace("\n","")
	temp=line.split("\t")

	if(int(temp[0]) not in node):
		node.append(int(temp[0]))
		degree[temp[0]]=1
	else:
		degree[temp[0]]+=1
	if(int(temp[1]) not in node):
		node.append(int(temp[1]))
		degree[temp[1]]=1
	else:
		degree[temp[1]]+=1
	e=temp[0]+"\t"+temp[1]
	e1=temp[1]+"\t"+temp[0]

	if((e not in edge)and(e1 not in edge)):
		edge.append(e)

fs.close()

deg=[]
for key in degree:
	deg.append(degree[key])

#distribution(deg)
deg.sort()

print len(partition)
#degree_sorted=sorted(degree.items(), key=operator.itemgetter(1))
community_size=[]
for key in partition:
	intm=[]
	edge_inside=0
	edge_outside=0
	edge_i=[]
	temp2=[]
	temp=partition[key].split("\t")
	temp2=deepcopy(temp)
	node_inside=len(temp)-1
	print "number of nodes inside: "+str(node_inside)
	community_size.append(node_inside)
	if(node_inside>2):
		internal_degree={}
		edge_node_intra={}
		edge_node_inter={}
		for i in xrange(len(temp)-1):
			intm.append(temp[i])
		for e in edge:
			temp=e.split("\t")
			if((temp[0] in intm)and(temp[1] in intm)):
				edge_inside+=1
				edge_i.append(e)
				if(temp[0] not in internal_degree):
					internal_degree[temp[0]]=1
					edge_node_intra[temp[0]]=1
				else:
					internal_degree[temp[0]]+=1
					edge_node_intra[temp[0]]+=1
				if(temp[1] not in internal_degree):
					internal_degree[temp[1]]=1
					edge_node_intra[temp[1]]=1
				else:
					internal_degree[temp[1]]+=1
					edge_node_intra[temp[1]]+=1
			elif((temp[0] in intm)or(temp[1] in intm)):
				edge_outside+=1
				if(temp[0] in intm):
					if(temp[0] not in edge_node_inter):
						edge_node_inter[temp[0]]=1
					else:
						edge_node_inter[temp[0]]+=1
				elif(temp[1] in intm):
					if(temp[1] not in edge_node_inter):
						edge_node_inter[temp[1]]=1
					else:
						edge_node_inter[temp[1]]+=1
				else:
					continue
			else:
				continue

		average_degree=float(2*edge_inside)/node_inside
		internal_density=float(2*edge_inside)/(node_inside*(node_inside-1))
		print "scoring function based on internal connectivity"
		print "----------------------------------------------"
		print "internal_density: "+str(internal_density)
		print "edge_inside: "+str(edge_inside)
		print "edge_outside: "+str(edge_outside)
		print "average_degree: "+str(average_degree)
		cnt=0
		median_deg=median(deg)
		print "median degree: "+str(median_deg)
		for obj in internal_degree:
			if(internal_degree[obj]>median_deg):
				cnt+=1
		fomd=float(cnt)/node_inside
		print "fomd: "+str(fomd)

		cnt=0
		
		G=nx.Graph()
		triangle={}
		temp1=[]
		for e in edge_i:
			temp1=e.split("\t")
			G.add_edge(int(temp1[0]),int(temp1[1]))
		triangle=nx.triangles(G)
		for key in triangle:
			if(triangle[key]>0):
				cnt+=1
	
		tpr=float(cnt)/node_inside
		print "TPR: "+str(tpr)
		if(edge_outside>0):
			print "scoring functions based on external connectivity"
			print "-----------------------------------------------"
			expansion=float(edge_outside)/node_inside
			print "expansion: "+str(expansion)

			cut_ratio=float(edge_outside)/(node_inside*(len(node)-node_inside))
			print "cut_ratio: "+str(cut_ratio)

			print "scoring function that combines internal and external connectivity"
			print "-----------------------------------------------------------------"					
			

			conductance=float(edge_outside)/((2*edge_inside)+edge_outside)
			print "conductance: "+str(conductance)

			normalized_cut= (float(edge_outside)/(2*(len(edge)-edge_inside)+edge_outside))+conductance
			print "normalized_cut: "+str(normalized_cut)
			

			#print "edge_node_inter: "
			#print edge_node_inter
			intm1=[]
			for i in xrange(len(temp2)-1):
				try:
					x=float(edge_node_inter[temp2[i]])/degree[temp2[i]]
					intm1.append(x)
				except:
					continue
			maximum_odf=max(intm1)
			print "maximum_odf: "+str(maximum_odf)

			average_odf=sum(intm1)/len(intm1)
			print "average_odf: "+str(average_odf)

			cnt=0
			for i in xrange(len(temp2)-1):
				try:
					if(edge_node_inter[temp2[i]]>edge_node_intra[temp2[i]]):
						cnt+=1
				except:
					continue
			flake_odf=float(cnt)/(len(temp2)-1)

			print "flake_odf: "+str(flake_odf)
			print "========================================================="
		else:
			print "isolated community"						
	else:
		continue	

#distribution(community_size)
