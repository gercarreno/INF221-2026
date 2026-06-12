// programación dp.
//
#include <bits/stdc++.h>
#include "../anime.h"
using namespace std;
using ll= long long;

ll knapsack_anime(vector <Anime>& animes, int M, int E){
    int n=animes.size();
    //definir el vector dp
    // [n + 1][M + 1][E + 1] lleno de ceros
    vector<vector<vector<ll>>> dp(n + 1, vector<vector<ll>>(M + 1, vector<ll>(E + 1, 0)));

    //definir casos base
    dp[0][M][E]=0;
    for (int i=0; i<n; i++){
        dp[i][M][0]=0;
        dp[i][0][E]=0;
    }
    for (int i=1; i<=n; i++){
        for (int m = 0; m <= M; m++) {
            for (int e = 0; e <= E; e++) {
                dp[i][m][e]=dp[i-1][m][e];
                for (int k = 1; k <= animes[i-1].n_cap; k++) {
                    int costo_t = calcular_tiempo(animes[i-1], k);
                    int costo_e = calcular_energia(animes[i-1], k);
                    ll satisfaccion_k = calcular_satisfaccion(animes[i-1], k);
                    // definir recurrencia
                    if(m>=costo_t && e>=costo_e)
                    dp[i][m][e]= max(dp[i][m][e], dp[i-1][m-costo_t][e-costo_e]+satisfaccion_k);
                }
            }
        }
    }
    return dp[n][M][E];
}
