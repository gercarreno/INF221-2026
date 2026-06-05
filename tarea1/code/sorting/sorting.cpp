#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <stdexcept>
#include <filesystem>

#ifdef __linux__
#include <sys/resource.h>
#endif

using namespace std;

extern void mergeSort(vector<int>&, int, int);
extern void quickSort(vector<int>&);
extern vector<int> sortArray(vector<int>&);

static long peak_kb() {
#ifdef __linux__
    rusage u{};
    getrusage(RUSAGE_SELF, &u);
    return (long)u.ru_maxrss;
#else
    return -1;
#endif
}

// crea carpetas padre si faltan
static void ensure_parent_dirs(const string& path) {
    filesystem::path p(path);
    auto parent = p.parent_path();
    if (!parent.empty()) filesystem::create_directories(parent);
}

static string out_path_from(const string& in) {
    string out = in;
    size_t pos = out.find("array_input");
    if (pos != string::npos) out.replace(pos, 11, "array_output");
    if (out.size() >= 4 && out.substr(out.size() - 4) == ".txt")
        return out.substr(0, out.size() - 4) + "_out.txt";
    return out + "_out.txt";
}

int main(int argc, char** argv) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (argc < 4) {
        cerr << "Uso: ./sorting <algoritmo> <archivo_input> <archivo_metricas>\n";
        return 1;
    }

    string alg = argv[1];
    string in_path = argv[2];
    string metrics_path = argv[3];

    ifstream fin(in_path);
    if (!fin) {
        cerr << "Error: no se pudo abrir el archivo: " << in_path << "\n";
        return 2;
    }

    vector<int> a;
    a.reserve(1024 * 1024);
    long long x;
    while (fin >> x) a.push_back((int)x);

    if (a.empty()) {
        cerr << "Advertencia: el arreglo de entrada esta vacio.\n";
    }

    auto t0 = chrono::steady_clock::now();

    if (alg == "merge") {
        if (!a.empty()) mergeSort(a, 0, (int)a.size() - 1);
    } else if (alg == "quick") {
        quickSort(a);
    } else if (alg == "sort") {
        a = sortArray(a);
    } else {
        cerr << "Error: algoritmo no reconocido: " << alg << "\n";
        return 3;
    }

    auto t1 = chrono::steady_clock::now();

    string out_path = out_path_from(in_path);
    ensure_parent_dirs(out_path);

    ofstream fout(out_path);
    if (!fout) {
        cerr << "Error: no se pudo crear el archivo de salida: " << out_path << "\n";
        return 4;
    }
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) fout << ' ';
        fout << a[i];
    }
    fout << '\n';

    long long us = chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
    long kb = peak_kb();

    ensure_parent_dirs(metrics_path);
    bool new_file = !filesystem::exists(metrics_path);

    ofstream mf(metrics_path, ios::app);
    if (mf) {
        if (new_file) {
            mf << "algorithm,time_ns,peak_kb,n_elems,input_file,output_file\n";
        }
        mf << alg << "," << us << "," << kb << "," << a.size() << ","
           << "\"" << in_path << "\"" << "," << "\"" << out_path << "\"" << "\n";
    } else {
        cerr << "Advertencia: no se pudo abrir archivo de metricas: " << metrics_path << "\n";
    }

    return 0;
}