#include <cstdio>
#include <cstring>
// Solve 2-Dimension partials by Binary Indexed Tree
const int maxn = 1000010;
long long tree[maxn];
int ans[maxn], a[maxn], b[maxn], n;

int lowbit(int x)
{
    return (x & -x);
}

void culculate(int x)
{
    while (x <= n)
    {
        tree[x] += 1;
        x += lowbit(x);
    }
}

long long  count(int x)
{
    long long result = 0;
    while (x)
    {
        result = result + tree[x];
        x = x - lowbit(x);
    }
    return result;
}

int main()
{
    scanf("%d", &n);
    for (int i = 1; i <= n; i++)
    {
        scanf("%d", &a[i]);
        b[a[i]] = i;
    }
    for (int i = 1; i <= n; i++)
    {
        ans[i] += i - 1 - count(a[i] - 1);
        culculate(a[i]);
    }
    
    memset(tree, 0, sizeof(tree));

    for (int i = n; i >= 1; i--)
    {
        ans[i] += count(a[i] - 1);
        culculate(a[i]);
    }
    for (int i = 1; i <= n; i++)
    {
        printf("%d ", ans[b[i]]);
    }

    return 0;
}