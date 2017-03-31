import sampling.variables as vb
import random
from copy import deepcopy
import random

def find_min(d):
	d1=deepcopy(d)
	intm=[]
	count=0
	while(count<5):
		min_=9999
		index=0
		for key in d1:
			if(d1[key]<min_):
				min_=d1[key]
				index=key
		intm.append(index)
		del d1[index]
		count+=1		
	random.shuffle(intm)
	return intm[0]
		
	
def check_full(l):
	if(len(l)>=vb.buf_len):
		return 1
	else:
		return 0

def elem_to_remove(l):
	rem_from = []
	#for val,freq in sorted(l.items(),key = lambda x:x[1]):
	for key in l:
		for i in xrange(l[key]):
			rem_from.append(key)

	random.shuffle(rem_from)

	min_ = 0
	max_ = len(rem_from) - 1

	ind = random.randint(min_,max_)
	return rem_from[ind]
