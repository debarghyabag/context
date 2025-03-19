#include<bits/stdc++.h>
using namespace std;
//     010110
int fun(string s)
{
    int n=s.length();
    int i=0;
    int j=n-1;
    if(n==0)
    {
        return 0;
    }
    while((i<j)&&(s.at(i)!=s.at(j)))
    {
        ++i;
        --j;
    }
    return j-i+1;

}

int main()
{
    int t,n;
    string s="";
    char c;

    cin>>t;
    while(t--)
    {
        cin>>n;
        
        for(int i=0;i<n;i++)
        {
            cin>>c;
            s=s+c;
        }
        
         cout<<fun(s)<<endl;
         s="";
    }

}