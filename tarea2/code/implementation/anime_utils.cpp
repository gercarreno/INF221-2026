#include "anime.h"
#include <bits/stdc++.h>

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
