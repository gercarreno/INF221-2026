#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Capitulo{
    int tiempo;
    int energia;
    ll satisfaccion;
};

struct Anime{
    int n_cap;
    ll bono;
    string nombre;
    vector<Capitulo> capitulos;
};
