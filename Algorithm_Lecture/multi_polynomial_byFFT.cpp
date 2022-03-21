//Fast Fourier Transformation for polynomial multiplication
# include <iostream>
#include <bits/stdc++.h>
using namespace std;
using cd = complex<double>;
const double PI = acos(-1);

//FFT and inverse FFT
//cited from https://cp-algorithms.com/algebra/fft.html#inverse-fft
void fft(vector<cd> & a, bool invert) {
    int n = a.size();
    if (n == 1)
        return;

    vector<cd> a0(n / 2), a1(n / 2);
    for (int i = 0; 2 * i < n; i++) {
        a0[i] = a[2*i];
        a1[i] = a[2*i+1];
    }
    fft(a0, invert);
    fft(a1, invert);

    double ang = 2 * PI / n * (invert ? -1 : 1);
    cd w(1), wn(cos(ang), sin(ang));
    for (int i = 0; 2 * i < n; i++) {
        a[i] = a0[i] + w * a1[i];
        a[i + n/2] = a0[i] - w * a1[i];
        if (invert) {
            a[i] /= 2;
            a[i + n/2] /= 2;
        }
        w *= wn;
    }
}

vector<int> multiply(vector<int> &a, vector<int> &b) {
    vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) 
        n <<= 1;
    fa.resize(n);
    fb.resize(n);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; i++)
        fa[i] *= fb[i];
    fft(fa, true);

    vector<int> result(n);
    for (int i = 0; i < n; i++)
        result[i] = round(fa[i].real());
    return result;
}
int main()
{
    int n,m;
    scanf ("%d%d",&n,&m);
    vector<int> F,G,H;
    int temp;
    for (int i=0;i<=n;i++)
    {
        scanf ("%d",&temp);
        F.push_back(temp);
    }

    for (int i=0;i<=m;i++)
    {
        scanf ("%d",&temp);
        G.push_back(temp);
    }
    //Fourier Transform
    H = multiply(F,G);

    for(int i=0;i<n+m+1;i++)
    {
        printf ("%d ",H[i]);
    }


}

 
