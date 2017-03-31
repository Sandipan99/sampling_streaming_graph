#include<iostream>
#include<fstream>
#include<vector>
#include<algorithm>
#include<string>
#include<map>
#include<random>

using namespace std;

//static int samp_size=100;  // select the samp size large enough to contain required number of nodes

int check_present_edge(vector<string> v,string s){
	vector<string>::iterator it;
	for(it=v.begin();it!=v.end();it++)
	{
		if(!s.compare(*it))
			return 1;
	}
	return 0;
}

int check_present_node(vector<int> v, int x){
	vector<int>::iterator it;
	for(it=v.begin();it!=v.end();it++)
	{
		if(x==*it)
			return 1;
	}
	return 0;
}

int check_present_m(map<string,double> m, string x){
	if(m.count(x)>0)
		return 1;
	else return 0;
}

string min_index(map<string,double> m){
	float min=10.0;
	string index;
	for(map<string,double>::iterator it=m.begin();it!=m.end();it++)
	{
		float x=it->second;
		if(x<min)
		{
			min=x;
			index=it->first;
		}
	}
	return index;
}

string max_index(map<string,double> m){
	float max=0.0;
	string index;
	for(map<string,double>::iterator it=m.begin();it!=m.end();it++)
	{
		float x=it->second;
		if(x>max)
		{
			max=x;
			index=it->first;
		}
	}
	return index;
}

double max_value(map<string,double> m){
	double max=0.0;
	string index;
	for(map<string,double>::iterator it=m.begin();it!=m.end();it++)
	{
		double x=it->second;
		if(x>max)
			max=x;

	}
	return max;
}

double generate_random(){
	//srand((unsigned)time(NULL));
	return (double)(rand())/RAND_MAX;
}

int full(map<string,double> v,int samp_size){
	if(v.size()==samp_size)
		return 1; 
	else	return 0;
}

void remove_edge(vector<string> edge,string e){
	int i;
	vector<string>::iterator it;
	for(it=edge.begin();it!=edge.end();it++){
		if(!e.compare(*it))
			break;
		i++;
	}
	edge.erase(edge.begin()+i);
				 		
}

void remove_node(vector<int> &node, map<string,double> edge){
	map<int,int> temp;
	vector<int> to_rem;
	int x,a,b;
	map<string,double>::iterator it;
	for(it=edge.begin();it!=edge.end();it++){
		string str=it->first;
		x=str.find("\t");
		a=stoi(str.substr(0,x));
		b=stoi(str.substr(x+1,str.length()));
		temp[a]=1;
		temp[b]=1;
	}
	for(int i=0;i<node.size();i++){
		if(temp.count(node[i])==0)
			to_rem.push_back(node[i]);
	}
	for(int i=0;i<to_rem.size();i++)
		node.erase(remove(node.begin(), node.end(), to_rem[i]), node.end());
		
}

int main(int argc, char *argv[]){
	int a,b;
	//int n=1000; // number of nodes in the original network
	double x,z;
	int t,y;
	int t_stop = atoi(argv[4]);
	int n = atoi(argv[2]);
	int samp_size = (int)((n)*atof(argv[3]));
	string e;	
	map<string,double> edge_seen;
	vector<int> node;    // node reservior
	map<string,double> edge; //format u v u<v 
	ifstream infile;
	infile.open(argv[1]);
	while(infile >> t >> a >> b){
		cout << a << " " << b << " time: " << t << endl;
		if(t>t_stop)
			break;
		if(a>b)
			e=to_string(b)+"\t"+to_string(a);
		else	e=to_string(a)+"\t"+to_string(b);
		
		if(check_present_m(edge_seen,e))  //generating uniform hash for a node. If already assigned we take that value else generate it
			x=edge_seen[e];
		else{
			x=generate_random();
			edge_seen[e]=x;
		}	
		if(!check_present_m(edge,e)){
			if(!full(edge,samp_size)){
				edge[e]=x;
				//cout << e << " added to the edge reservior" << "hash-value: " << edge[e] << endl;
				if(!check_present_node(node,a)){
					node.push_back(a);
					//cout << "adding node: " << a << endl;
				}
				if(!check_present_node(node,b)){
					node.push_back(b);
					//cout << "adding node: " << b << endl;
				}		
			}	
			else{
				if(x<max_value(edge)) 
				{
					//cout << "found edge with less hash value: " << e << "\t" << x << endl;
					string str1=max_index(edge);
					//cout << "edge to replace: " << str1 << "\t" << edge[str1] << endl;
					edge[e]=x;
					if(!check_present_node(node,a))
						node.push_back(a);
					if(!check_present_node(node,b))
						node.push_back(b);
					edge.erase(str1);
					remove_node(node,edge);
				}		
			}
		}
			
	}
	cout<< "Number of nodes: " << node.size() << endl;
	ofstream of;
	string fname = "sample_streaming_edge_sample_";
	fname.append(argv[3]);
	of.open(fname);
	map<string,double>::iterator it;
	for(it=edge.begin();it!=edge.end();it++)
		of << it->first <<"\n";
	of.close();
	return 0;
}
