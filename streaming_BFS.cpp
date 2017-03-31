#include<iostream>
#include<fstream>
#include<string>
#include<algorithm>
#include<map>
#include<vector>
#include<list>

using namespace std;

//static int samp_size=50;

template <typename T>
class queue{
	vector<T> array;
	public:
	void insert(T x){
		array.push_back(x);
	}
	T remove(){
		T x=array[0];
		array.erase(array.begin());
		return x;
	}
	void remove_time(map<string,int> m,int time){
		T x=array[0];
		while(m[x]<=time){
			array.erase(array.begin());
			x=array[0];
		}
	}
	void remove_element(T x){
		int cnt=0;
		for(int i=0;i<array.size();i++){
			if(array[i]==x)
				break;
			cnt++;
		}
		array.erase(array.begin()+cnt);			
	}	

	void display(){
		cout << "displaying queue\n";
		typename vector<T>::iterator i;
		for(i=array.begin();i!= array.end();i++)
			cout << *i << "\n";
	}
	int empty(){
		if(array.size()==0)
			return 1;
		return 0;
	}
	int present(T x){
		typename vector<T>::iterator i;
		i=find(array.begin(),array.end(),x);
		if(i!=array.end())
			return 1;
		else	return 0;
	}
	int size(){
		return array.size();
	}
	int sample_seed_node(){
		list<int> temp;
		int tmp[2];
		int x;
		for(int i=0;i<array.size();i++){
			x=array[i].find("\t");
			tmp[0]=stoi(array[i].substr(0,x));
			tmp[1]=stoi(array[i].substr(x+1,array[i].length()));
			temp.push_back(tmp[0]);
			temp.push_back(tmp[1]);
		}
		temp.unique();
		int randNum = rand()%(temp.size());
		auto l=temp.begin();
		advance(l,randNum);
		return *l;	
	}

	int find_incedent_edge(int x){
		vector<int> temp;
		int tmp[2],y;
		for(int i=0;i<array.size();i++){
			y=array[i].find("\t");
			tmp[0]=stoi(array[i].substr(0,y));
			tmp[1]=stoi(array[i].substr(y+1,array[i].length()));

			if(tmp[0]==x)
				temp.push_back(tmp[1]);
			if(tmp[1]==x)
				temp.push_back(tmp[0]);
		}
		//cout << "length: "<< temp.size() << endl;
		if(temp.size()>0)
			return temp[rand()%temp.size()];
		return -1;
	}

	
};

string edge_format(int a, int b){
	string e_t;
	if(a<b)
		e_t=to_string(a)+"\t"+to_string(b);
	else	e_t=to_string(b)+"\t"+to_string(a);
	return e_t;
}


int is_present(vector<int> w, int n){
	vector<int>::iterator it;
	it=find(w.begin(),w.end(),n);
	if(it!=w.end())
		return 1;
	else	return 0;
}

int present(vector<string> w,string e){
	vector<string>::iterator it;
	it=find(w.begin(),w.end(),e);
	if(it!=w.end())
		return 1;
	else	return 0;

}

void adjust(vector<int> &node, vector<string> &edge, int samp_size, char *name){
	int max,u,x;
	int tmp[2];
	vector<int> temp;
	while(node.size()>samp_size){
		max=node.size()-1;
		int randNum=rand()%max;
		u=node[randNum];
		node.erase(std::remove(node.begin(),node.end(),u),node.end());
		temp.push_back(u);
	}
	ofstream out;
	string fname = "sample_BFS_";
	fname.append(name);
	out.open(fname);
	for(int i=0;i<edge.size();i++)
	{
		x=edge[i].find("\t");
		tmp[0]=stoi(edge[i].substr(0,x));
		tmp[1]=stoi(edge[i].substr(x+1,edge[i].length()));
		if((is_present(temp,tmp[0]))||(is_present(temp,tmp[1])))
			continue;
		else	out << edge[i] << endl;
	}
	out.close();
}


int main(int argc, char* argv[]){
	queue<string> window;
	queue<int> node_queue;
	map<string,int> edge_time;
	int t1=atoi(argv[4]);
	int t_stop = atoi(argv[5]); // t_stop >> t1
	int population = atoi(argv[2]);
	int samp_size = (int)(population*atof(argv[3]));
	string e_t, e_s;
	int a,b,u,t,v,x,cnt=0,flag=0;
	vector<int> node;
	vector<string> edge; 
	ifstream in;
	in.open(argv[1]); // the graph file should be in the format [time \t node \t node]
	while(in >> t >> a >> b){
		cout << "streaming edge: " << a << " " << b << " time: " << t << endl;
		if(t>t_stop)
			break; 
		e_t=edge_format(a,b);
		edge_time[e_t]=t;
		if(t < t1)
		{
			if(!window.present(e_t)){
				window.insert(e_t);
				cnt++;
			}
		}
		else{
			if(flag==0){
				flag++;
				window.insert(e_t);
				window.display();
				u=window.sample_seed_node();
				node.push_back(u);
			}
			else{	
				v=window.find_incedent_edge(u);
				if(v==-1){                     // no incedent edge on u present
					if(!node_queue.empty()){
						u=node_queue.remove();
					}
					else{	
						u=window.sample_seed_node();
					}
					if(!is_present(node,u))
						node.push_back(u);	
				}
				else{
					e_s=edge_format(u,v);
					edge.push_back(e_s);
					if(!is_present(node,v))
						node.push_back(v);
					window.remove_element(e_s);
					node_queue.insert(v);
				}
				window.remove_time(edge_time,t-t1);
				window.insert(e_t);
			}
		}
	}
	adjust(node,edge,samp_size,argv[3]);			
	return 0;
} 
