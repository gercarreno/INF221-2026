#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll= long long;

int calcular_tiempo(const Anime& anime, int k) {
    int tiempo_total = 0;
    for (int j = 0; j < k; ++j) {
        tiempo_total += anime.capitulos[j].tiempo;
    }
    return tiempo_total;
}

int calcular_energia(const Anime& anime, int k) {
    int energia_total = 0;
    for (int j = 0; j < k; ++j) {
        energia_total += anime.capitulos[j].energia;
    }
    return energia_total;
}
ll calcular_satisfaccion(const Anime& anime, int k){
    ll satisfaccion_total=0;
    for (int j=0; j<k; j++){
        satisfaccion_total+= anime.capitulos[j].satisfaccion;
    }
    if(k== anime.n_cap){
        satisfaccion_total+=anime.bono;
    }
    return satisfaccion_total;
}

ll satisfaccion_global=0;
void backtracking(int anime_i, vector<Anime>& animes, int M, int E, ll satisfaccion_actual){
    int n= animes.size();
    if (anime_i==n){
        if(satisfaccion_actual > satisfaccion_global){
            satisfaccion_global=satisfaccion_actual;
        }
        return;
    }

    for(int k=0; k<=animes[anime_i].n_cap; k++){
        int tiempo_k= calcular_tiempo(animes[anime_i], k);
        int energia_k= calcular_energia(animes[anime_i], k);
        ll satisfaccion_k = calcular_satisfaccion(animes[anime_i], k);
        if(tiempo_k<= M && energia_k<=E){
            backtracking(anime_i+1, animes, M-tiempo_k, E-energia_k, satisfaccion_actual+satisfaccion_k);
        }

    }

}
