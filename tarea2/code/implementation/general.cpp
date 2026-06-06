#include <bits/stdc++.h>
#include "anime.h"
using namespace std;

int main(){
    int n, M, E;
    vector<Anime> animes;
    Capitulo capitulo;
    cin >> n >> M >> E;
    for (int i=0; i<n; i++){
        Anime anime;
        cin >> anime.nombre >> anime.n_cap >> anime.bono;
        for (int j=0; j<anime.n_cap; j++){
            cin >> capitulo.tiempo >> capitulo.energia >> capitulo.satisfaccion;
            anime.capitulos.push_back(capitulo);
        }
        animes.push_back(anime);
    }

    //Checking bruteforce solution
    satisfaccion_global = 0;
    backtracking(0, animes, M, E, 0);
    cout << satisfaccion_global << endl;

    /* Check that vector stores the right information;
    cout << n << " " << M << " " << E << endl;
    for (int i=0; i<n; i++){
        cout << animes[i].nombre << " " << animes[i].n_cap << " " << animes[i].bono << endl;
        for (int j=0; j<animes[i].n_cap; j++){
            cout << animes[i].capitulos[j].tiempo << " "
                 << animes[i].capitulos[j].energia << " "
                << animes[i].capitulos[j].satisfaccion << endl;
        }
    }
    */
    return 0;
}
