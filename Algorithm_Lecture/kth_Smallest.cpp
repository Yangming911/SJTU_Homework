#include <iostream>
#pragma GCC optimize(2)
using namespace std;
//output k-th Smallest Number
//const int N = 4e7 + 1;
const int N = 10;
int n, k;
int a[N];
int a_left[N]={0}, a_right[N]={0};

void read_input_data(){
    int m;
    cin >> n >> k >> m;
    for (int i = 0; i < m; i++) {
        cin >> a[i];
    }
    unsigned int z = a[m-1];
    for (int i = m ; i < n; i++) {
        z ^= z << 13;
        z ^= z >> 17;
        z ^= z << 5;
        a[i] = z & 0x7fffffff;
    }
};

int Find(int a[],int n,int k)//Find k-th smallest number in a[n]
{
    int tmp = a[n/2];
    int a_left_num = 0, a_right_num = 0;
    for (int i = 0; i < n; i++) {
        if (i==n/2) continue;
        if (a[i] < tmp) {
            a_left[a_left_num] = a[i];
            a_left_num++;
        } else {
            a_right[a_right_num] = a[i];
            a_right_num++;
        }
    }

        if (a_left_num == k - 1) return tmp;
        else if (a_left_num > k-1) return Find(a_left, a_left_num, k);
        else return Find(a_right, a_right_num, k-a_left_num-1);
};

int main()
{
    read_input_data();
    //for(int i = 0; i < n; i++)cout << a[i] << " ";
    cout << Find(a, n, k) << endl;
    return 0;
}