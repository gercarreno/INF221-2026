// Greedy with max_satisfaction
#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll = long long;

//ll satisfaccion_global=0;
ll anime_max(vector<Anime>& animes, int M, int E){
    vector<Anime> copia = animes;
    sort(copia.begin(), copia.end(), [](const Anime& a, const Anime& b) {
        return calcular_satisfaccion(a, a.n_cap) > calcular_satisfaccion(b, b.n_cap);
    });
    int n= copia.size();
    ll satisfaccion_total=0;
    int energia_restante=E;
    int tiempo_restante=M;
    for (int k=0; k<n; k++){
        int total_caps= copia[k].n_cap;
        //recorrer cada capitulo del anime hasta verlo completo y ver si M y E me alcanzan y lo agrego a la satisfaccion total + bono.
        int costo_tiempo= calcular_tiempo(copia[k], total_caps);
        int costo_energia= calcular_energia(copia[k], total_caps);
        ll satisfaccion_k = calcular_satisfaccion(copia[k], total_caps);
        if(costo_energia<=energia_restante && costo_tiempo<= tiempo_restante){
            energia_restante-=costo_energia;
            tiempo_restante-=costo_tiempo;
            satisfaccion_total += satisfaccion_k;
        }
    }
    return satisfaccion_total;
}
