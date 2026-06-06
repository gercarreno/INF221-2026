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

void backtracking(int anime_i, vector<Anime>& animes, int M, int E, ll satisfaccion_actual);
extern ll satisfaccion_global;
