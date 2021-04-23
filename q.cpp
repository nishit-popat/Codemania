#include<bits/stdc++.h>
using namespace std;
int main() {
	int t,k,ans=0;
	cin>>t;
	while(t--){
	  int a,b,i;
	  cin>>a>>b;
	  for(i=a;i<=b;i++){
        k=i%10;
        if(k==2 || k==3 || k==9){
            ans++;
        }
	  }
	  printf("%d\n",ans);
	  ans=0;
	}
	return 0;
}
