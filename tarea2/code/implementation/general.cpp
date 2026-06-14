#include <bits/stdc++.h>
#include <chrono>
#include <sys/resource.h>
#include "anime.h"
using namespace std;

double get_memory_mb() {
    struct rusage r_usage;
    getrusage(RUSAGE_SELF, &r_usage);
    return r_usage.ru_maxrss / 1024.0;
}

int main() {
    vector<int> ns = {3, 5, 8, 20, 40, 80, 100, 150, 200};
    int cases_per_n = 3;
    int procesados = 0;

    //archivo csv
    ofstream f_csv("./data/measurements/measurements.csv");
    f_csv << "id_archivo,n_animes,total_capitulos,minutos_m,energia_e,algoritmo,tiempo_ms,memoria_mb,satisfaccion\n";

    // Iteramos sobre los posibles tamaños y el número de caso (1 al 3)
    for (int n_val : ns) {
        for (int i = 1; i <= cases_per_n; i++) {
            string base_name = "testcases_" + to_string(n_val) + "_" + to_string(i);
            string in_path = "./data/inputs/" + base_name + ".txt";
            ifstream fin(in_path);
            if (!fin.is_open()) {
                continue;
            }

            int n, M, E;
            vector<Anime> animes;
            Capitulo capitulo;
            int total_capitulos = 0;

            fin >> n >> M >> E;
            for (int j = 0; j < n; j++) {
                Anime anime;
                fin >> anime.nombre >> anime.n_cap >> anime.bono;
                total_capitulos += anime.n_cap;
                for (int k = 0; k < anime.n_cap; k++) {
                    fin >> capitulo.tiempo >> capitulo.energia >> capitulo.satisfaccion;
                    anime.capitulos.push_back(capitulo);
                }
                animes.push_back(anime);
            }
            fin.close();

            string base_out = "./data/outputs/" + base_name;

            // medir tiempo y memoria
            chrono::time_point<chrono::high_resolution_clock> start, stop;
            double memoria;

            // bruteforce
            ofstream fout_bf(base_out + "_bf.txt");

            if (n <= 25) {
                satisfaccion_global = 0;

                start = chrono::high_resolution_clock::now();
                backtracking(0, animes, M, E, 0);
                stop = chrono::high_resolution_clock::now();
                memoria = get_memory_mb();
                auto duration_bf = chrono::duration_cast<chrono::milliseconds>(stop - start).count();

                fout_bf << satisfaccion_global << endl;
                f_csv << base_name << "," << n << "," << total_capitulos << "," << M << "," << E << ",bf," << duration_bf << "," << memoria << "," << satisfaccion_global << "\n";
            } else {
                cout << "backtracking is 'bout to get lit w/ N=" << n << endl;
                fout_bf << "0" << endl;
            }
            fout_bf.close();

            // anime_greedy
            ofstream fout_gh1(base_out + "_gh1.txt");

            start = chrono::high_resolution_clock::now();
            long long res_gh1 = anime_greedy(animes, M, E);
            stop = chrono::high_resolution_clock::now();
            memoria = get_memory_mb();
            auto duration_gh1 = chrono::duration_cast<chrono::milliseconds>(stop - start).count();

            fout_gh1 << res_gh1 << endl;
            f_csv << base_name << "," << n << "," << total_capitulos << "," << M << "," << E << ",gh1," << duration_gh1 << "," << memoria << "," << res_gh1 << "\n";
            fout_gh1.close();

            // anime_max
            ofstream fout_gh2(base_out + "_gh2.txt");

            start = chrono::high_resolution_clock::now();
            long long res_gh2 = anime_max(animes, M, E);
            stop = chrono::high_resolution_clock::now();
            memoria = get_memory_mb();
            auto duration_gh2 = chrono::duration_cast<chrono::milliseconds>(stop - start).count();

            fout_gh2 << res_gh2 << endl;
            f_csv << base_name << "," << n << "," << total_capitulos << "," << M << "," << E << ",gh2," << duration_gh2 << "," << memoria << "," << res_gh2 << "\n";
            fout_gh2.close();

            // knapsack_anime
            ofstream fout_dp(base_out + "_dp.txt");

            start = chrono::high_resolution_clock::now();
            long long res_dp = knapsack_anime(animes, M, E);
            stop = chrono::high_resolution_clock::now();
            memoria = get_memory_mb();
            auto duration_dp = chrono::duration_cast<chrono::milliseconds>(stop - start).count();

            fout_dp << res_dp << endl;
            f_csv << base_name << "," << n << "," << total_capitulos << "," << M << "," << E << ",dp," << duration_dp << "," << memoria << "," << res_dp << "\n";
            fout_dp.close();

            cout << base_name << ".txt w/ (_bf, _gh1, _gh2, _dp)" << endl;
            procesados++;
        }
    }

    f_csv.close();
    cout << "Se procesaron " << procesados << " archivos en total." << endl;

    return 0;
}
