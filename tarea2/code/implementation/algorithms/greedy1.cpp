// Greedy ratio (satisfaccion/tiempo, energia)
#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll = long long;


ll anime_greedy(vector<Anime>& animes, int M, int E){
    int n_animes= animes.size();

    vector<anime_ratio> anime;
    // el que anime que tenga mejor ratio
    ll satisfaccion_actual=0;
    for (int i=0; i<n_animes; i++){
        for (int k=1; k<=animes[i].n_cap; k++){
            int energia_k= calcular_energia(animes[i], k);
            int tiempo_k= calcular_tiempo(animes[i], k);
            ll satisfaccion_k= calcular_satisfaccion(animes[i], k);

            double ratio = (double)satisfaccion_k / ((double)tiempo_k / M + (double)energia_k / E);
            anime.push_back({i, k, ratio, tiempo_k, energia_k, satisfaccion_k});

        }
    }
    sort(anime.begin(), anime.end(), [](const anime_ratio& a, const anime_ratio& b) {
        return a.ratio > b.ratio;
    });
    vector<bool> anime_seleccionado(n_animes, false);
    int energia_restante=E;
    int tiempo_restante=M;
    for (int b=0; b<anime.size(); b++){
        if(!anime_seleccionado[anime[b].id_anime]){
            if(tiempo_restante>= anime[b].tiempo_k && energia_restante>= anime[b].energia_k){
                satisfaccion_actual+= anime[b].satisfaccion_k;
                energia_restante-=anime[b].energia_k;
                tiempo_restante-= anime[b].tiempo_k;
                anime_seleccionado[anime[b].id_anime]=true;
            }
        }
    }
    return satisfaccion_actual;

}
