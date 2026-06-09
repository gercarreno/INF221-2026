#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Capitulo{
    int tiempo;
    int energia;
    ll satisfaccion;
};

struct anime_ratio {
    int id_anime;
    int k_capitulos;
    double ratio;
    int tiempo_k, energia_k;
    ll satisfaccion_k;
};
struct Anime{
    int n_cap;
    ll bono;
    string nombre;
    vector<Capitulo> capitulos;
};

void backtracking(int anime_i, vector<Anime>& animes, int M, int E, ll satisfaccion_actual);
extern ll satisfaccion_global;

ll anime_greedy(vector<Anime>& animes, int M, int E);
ll anime_max(vector<Anime>& animes, int M, int E);


int calcular_tiempo(const Anime& anime, int k);
int calcular_energia(const Anime& anime, int k);
ll calcular_satisfaccion(const Anime& anime, int k);
