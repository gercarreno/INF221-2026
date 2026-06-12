#include <bits/stdc++.h>
#include "anime.h"
using namespace std;

int main() {
    // Si tus archivos empiezan en 1 (input_01.txt), cambia a int i = 1;
    int i = 1;

    while (true) {
        // formatear el nombre de los archivos
        ostringstream idx_stream;
        idx_stream << setw(2) << setfill('0') << i;
        string idx_str = idx_stream.str();

        // ruta inicial
        string in_path = "./data/inputs/input_" + idx_str + ".txt";
        ifstream fin(in_path);

        // !archivo de entrada, terminamos el ciclo
        if (!fin.is_open()) {
            cout << "Se procesaron " << i-1 << " archivos." << endl;
            break;
        }

        int n, M, E;
        vector<Anime> animes;
        Capitulo capitulo;

        // Leer los datos
        fin >> n >> M >> E;
        for (int j = 0; j < n; j++) {
            Anime anime;
            fin >> anime.nombre >> anime.n_cap >> anime.bono;
            for (int k = 0; k < anime.n_cap; k++) {
                fin >> capitulo.tiempo >> capitulo.energia >> capitulo.satisfaccion;
                anime.capitulos.push_back(capitulo);
            }
            animes.push_back(anime);
        }
        fin.close();

        string base_out = "./data/outputs/output_" + idx_str;

        // bruteforce
        ofstream fout_bf(base_out + "_bf.txt");

        if (n <= 25) {
            satisfaccion_global = 0;
            backtracking(0, animes, M, E, 0);
            fout_bf << "Backtracking: " << satisfaccion_global << endl;
        } else {
            cout << "backtracking is 'bout to get lit w/ N=" << n << endl;
            fout_bf << "0" << endl;
        }
        fout_bf.close();

        // anime_greedy
        ofstream fout_gh1(base_out + "_gh1.txt");
        fout_gh1 << anime_greedy(animes, M, E) << endl;
        fout_gh1.close();

        // anime_max
        ofstream fout_gh2(base_out + "_gh2.txt");
        fout_gh2 << anime_max(animes, M, E) << endl;
        fout_gh2.close();

        // knapsack_anime
        ofstream fout_dp(base_out + "_dp.txt");
        fout_dp << knapsack_anime(animes, M, E) << endl;
        fout_dp.close();

        cout << "input_" << idx_str << ".txt w/ (_bf, _gh1, _gh2, _dp)" << endl;

        // siguente archivo
        i++;
    }

    return 0;
}
