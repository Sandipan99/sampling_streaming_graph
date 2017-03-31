import networkx as nx

def init():
	global buf_len
	buf_len = 0
	global V_S
	V_S = []
	global E_S
	E_S = []
	global G
	G = nx.Graph()
	global deg_node
	deg_node = {}
	global edge_density_th
	edge_density_th = 0.0
	global parent 
	parent = {}
	global l
	l = {} 
	global partition
	partition = {}
	global modularity_val
	modularity_val = 0.0
	global max_part_num
	max_part_num = 0
	global edge_count_part
	edge_count_part = {}
	global node_count_part
	node_count_part = {}
	global samp_size
	samp_size = 0
