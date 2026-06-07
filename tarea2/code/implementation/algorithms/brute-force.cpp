#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll= long long;

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
