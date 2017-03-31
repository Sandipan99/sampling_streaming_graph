#include<iostream>
#include<fstream>
#include<vector>
#include<string>
#include<map>
#include<random>
#include<algorithm>

using namespace std;

//static int samp_size=50;

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

int check_present_m(map<int,double> m, int x){
	if(m.count(x)>0)
		return 1;
	else return 0;
}

int min_index(map<int,double> m){
	float min=10.0;
	int index=0;
	for(map<int,double>::iterator it=m.begin();it!=m.end();it++)
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

int max_index(map<int,double> m){
	float max=0.0;
	int index=0;
	for(map<int,double>::iterator it=m.begin();it!=m.end();it++)
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

double max_value(map<int,double> m){
	double max=0.0;
	int index=0;
	for(map<int,double>::iterator it=m.begin();it!=m.end();it++)
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

int full_v(vector<int> v, int samp_size){
	if(v.size()==samp_size)
		return 1; 
	else	return 0;
}

void remove_edge(vector<string> &edge,int y){
	cout << "remove edge consisting node: " << y << "\n";
	vector<string> to_remove;
	for(int i=0;i<edge.size();i++){
		int x=edge[i].find("\t");
		int n_a=stoi(edge[i].substr(0,x));
		int n_b=stoi(edge[i].substr(x+1,edge[i].length()));
		if ((n_a==y)or(n_b==y)){
			to_remove.push_back(edge[i]);
			cout << "removed edge: " << edge[i] << "\n";
		}	
	}
	cout << "size of edge-list: " << edge.size() << "\n";
	cout << "number of edges to remove: " << to_remove.size() << "\n";
	for(int i=0;i<to_remove.size();i++)
		edge.erase(remove(edge.begin(), edge.end(), to_remove[i]), edge.end());
	//cout << "size of edge list after removing edges: " << edge.size() << "\n";
}


int main(int argc, char* argv[]){
	int a,b,y,t;
	int t_time = atoi(argv[4]);
	int n=atoi(argv[2]); // number of nodes in the original network
	int samp_size = (int)(n*atof(argv[3]));
	double x,z;	
	map<int,double> node_seen;
	map<int,double> node;    // node reservior
	vector<string> edge; //format u v u<v 
	ifstream infile;
	infile.open(argv[1]);
	while(infile >> t >> a >> b){
		if (t > t_time)
			break;
		cout << "considering edge: "<< to_string(a)+"\t"+to_string(b) << "time" << t << "\n";
		if(check_present_m(node_seen,a))  //generating uniform hash for a node. If already assigned we take that value else generate it
			x=node_seen[a];
		else{
			x=generate_random();
			node_seen[a]=x;
		}
		// checking for a
		if(!check_present_m(node,a))  // if a is not already in the node reservior
		{
			if(node.size()<samp_size){	
				node[a]=x;
				//cout << "less than sample size " << node[a] << "\n";
				//cout << "inserting node: " << a << "\n";
			}
			else{
				if(x<max_value(node))
				{
					//cout << x << "\n";
					//cout << max_value(node) << "\n";
					//cout << "found node with a lower hash value: " << a << "\t" << x << endl;
					y=max_index(node);
					//cout << "the node to be replaced: " << y << "\t" << node[y] << endl;
					node[a]=x;
					//cout << "size of node before deletion: " << node.size() << endl;
					node.erase(y);
					//cout << "size of node after deletion: " << node.size() << endl;
					remove_edge(edge,y);
					//cout << "size of edge list after removing edges: " << edge.size() << "\n";
				}
			}	
		}

		if(check_present_m(node_seen,b))  //generating uniform hash for a node. If already assigned we take that value else generate it
			x=node_seen[b];
		else{	
			x=generate_random();
			node_seen[b]=x;
		}
		// checking for b
		if(!check_present_m(node,b)) // if b is not already in the node reservior
		{
			if(node.size()<samp_size){
				node[b]=x;
				//cout << "less than sample size " << node[b] << "\n";
				//cout << "inserting node: " << b << "\n";
			}
			else{
				if(x<max_value(node))
				{
					//cout << x << "\n";
					//cout << max_value(node) << "\n";
					//cout << "found node with a lower hash value: " << b << "\t" << x << endl;
					y=max_index(node);
					//cout << "the node to be replaced: " << y << "\t" << node[y] << endl;
					node[b]=x;
					//cout << "size of node before deletion: " << node.size() << endl;
					node.erase(y);
					//cout << "size of node after deletion: " << node.size() << endl;
					remove_edge(edge,y);
					//cout << "size of edge list after removing edges: " << edge.size() << "\n";
				}
			}	
		}
		if((check_present_m(node,a))&&(check_present_m(node,b))){   // inserting edge to edge reservior
			string str1=to_string(a);
			string str2=to_string(b);
			if(a<b){
				edge.push_back(str1+"\t"+str2);
				//cout << "inserting edge: " << str1+"\t"+str2 << "\n";
				//cout << "size of edge list: " << edge.size() << "\n"; 
			}
			else{	
				edge.push_back(str2+"\t"+str1);
				//cout << "inserting edge: " << str2+"\t"+str1 << "\n";
				//cout << "size of edge list: " << edge.size() << "\n";
			}	
		}
			
	//cout << "------------------------\n";
	}
	infile.close();
	//cout << "length of node_seen: " << node_seen.size() <<"\n";
	//cout << "length of node: " << node.size() << "\n";
	ofstream of;
	string fname = "stream_node_sample_";
	fname.append(argv[3]);
	of.open(fname);
	for(int i=0;i<edge.size();i++)
		of << edge[i]+"\n";
	of.close();
	/*map<int,double>::iterator it;
	for(it=node.begin();it!=node.end();it++)
		cout << it->first << "\t" << it->second << "\n";*/
	return 0;
}
