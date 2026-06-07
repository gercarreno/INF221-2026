// Greedy with max_satisfaction
#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll = long long;

//ll satisfaccion_global=0;
ll anime_max(int n, vector<Anime>& animes, int M, int E){
    sort(animes.begin(), animes.end(), [](const Anime& a, const Anime& b) {
        return a.bono > b.bono;
    });
    ll satisfaccion_total=0;
    int energia_restante=E;
    int tiempo_restante=M;
    for (int k=0; k<n; k++){
        int total_caps= animes[k].n_cap;
        //recorrer cada capitulo del anime hasta verlo completo y ver si M y E me alcanzan y lo agrego a la satisfaccion total + bono.
        int costo_tiempo= calcular_tiempo(animes[k], total_caps);
        int costo_energia= calcular_energia(animes[k], total_caps);
        int satisfaccion_k = calcular_satisfaccion(animes[k], total_caps);
        if(costo_energia<=energia_restante && costo_tiempo<= tiempo_restante){
            energia_restante-=costo_energia;
            tiempo_restante-=costo_tiempo;
            satisfaccion_total += satisfaccion_k;
        }
    }
    return satisfaccion_total;
}
