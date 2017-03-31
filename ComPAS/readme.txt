1. The main file is "mod_opt_samp.py" and the subroutines are in folder "sampling". Its location should be same as that of "mod_opt_samp.py"

2. To run routine networkx and community api should be installed in the system.

	a) networkx can be installed in a ubuntu system using the command - sudo apt-get install networkx
 	b) community api can be downloaded and installed from http://perso.crans.org/aynaud/communities/
	      
3. The routine can be run using the command - 
	python mod_opt_samp.py <network_file> <network-size> <sampling-rate> <end_time>
	e.g. - python mod_opt_samp.py network.txt 5000 0.3 4686

	1) network file - network.txt
	   The network file should be of the format time'\t'u'\t'v where u and v are the end vertices and time is the time of arrival
	2) network size - 5000
	   Number of nodes in the original network
	3) sampling-rate - 0.3
	   Size of the sample = 0.3*5000
	4) end-time - 4686
	   Time upto which streaming is considered.

4. Out put - sampled_network.txt (the sampled network,format u'\t'v)
	     partition_file.txt (the community structure,format u'\t'C(u)) 
