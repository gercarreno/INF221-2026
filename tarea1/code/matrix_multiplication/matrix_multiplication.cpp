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

extern vector<vector<int>> naive_multiply(const vector<vector<int>>&, const vector<vector<int>>&);
extern vector<vector<int>> strassen_multiply(const vector<vector<int>>&, const vector<vector<int>>&);

// Memoria pico (KB) en Linux, -1 en otros SO.
static long peak_kb() {
#ifdef __linux__
    rusage u{};
    getrusage(RUSAGE_SELF, &u);
    return (long)u.ru_maxrss;
#else
    return -1;
#endif
}

// Crea directorios padres si hace falta.
static void ensure_parent_dirs(const string& path) {
    filesystem::path p(path);
    auto parent = p.parent_path();
    if (!parent.empty()) filesystem::create_directories(parent);
}

// Nombre base sin directorio ni extensión.
static string basename_no_ext(const string& path) {
    size_t pos = path.find_last_of("/\\");
    string name = (pos == string::npos) ? path : path.substr(pos + 1);
    size_t dot = name.find_last_of('.');
    if (dot != string::npos) name = name.substr(0, dot);
    return name;
}

// Obtiene N buscando el primer bloque de dígitos en el nombre
static int get_n_from_filename(const string& path) {
    string name = basename_no_ext(path);
    for (size_t i = 0; i < name.size(); ++i) {
        if (name[i] >= '0' && name[i] <= '9') {
            size_t j = i;
            while (j < name.size() && name[j] >= '0' && name[j] <= '9') j++;
            string num = name.substr(i, j - i);
            try {
                int n = stoi(num);
                if (n > 0) return n;
            } catch (...) {
                // ignora
            }
            i = j;
        }
    }
    return -1;
}

// Lee matriz, asumiendo N x N, donde N viene del nombre del archivo.
static vector<vector<int>> read_matrix(const string& path) {
    int N = get_n_from_filename(path);
    if (N <= 0) throw runtime_error("No pude obtener N del nombre: " + path);

    ifstream fin(path);
    if (!fin) throw runtime_error("No se pudo abrir el archivo: " + path);

    vector<vector<int>> a(N, vector<int>(N, 0));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (!(fin >> a[i][j])) {
                throw runtime_error("Datos insuficientes (se esperaban " + to_string(N*N) + " enteros) en " + path);
            }
        }
    }
    // Nos quedamos con N x N tal como definimos.
    return a;
}

// Escribe matriz con cabecera "rows cols" y luego filas
static void write_matrix(const vector<vector<int>>& a, const string& path) {
    ensure_parent_dirs(path);
    ofstream fout(path);
    if (!fout) {
        cerr << "Error: no se pudo crear el archivo de salida: " << path << "\n";
        return;
    }
    if (a.empty() || a[0].empty()) {
        fout << "0 0\n";
        return;
    }
    fout << a.size() << " " << a[0].size() << "\n";
    for (const auto& row : a) {
        for (size_t j = 0; j < row.size(); ++j) {
            if (j) fout << ' ';
            fout << row[j];
        }
        fout << "\n";
    }
}

int main(int argc, char** argv) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (argc < 5) {
        cerr << "Uso: ./matrix_multiplication <algoritmo> <matriz1> <matriz2> <archivo_metricas>\n";
        return 1;
    }

    string alg = argv[1];
    string path1 = argv[2];
    string path2 = argv[3];
    string metrics_path = argv[4];

    vector<vector<int>> A, B, C;
    try {
        A = read_matrix(path1);
        B = read_matrix(path2);
    } catch (const exception& e) {
        cerr << "Error leyendo matrices: " << e.what() << "\n";
        return 2;
    }

    if (A.empty() || B.empty() || A[0].empty() || B[0].empty() || A[0].size() != B.size()) {
        cerr << "Error: dimensiones incompatibles para la multiplicacion.\n";
        return 3;
    }

    auto t0 = chrono::steady_clock::now();

    if (alg == "naive") {
        C = naive_multiply(A, B);
    } else if (alg == "strassen") {
        C = strassen_multiply(A, B);
    } else {
        cerr << "Error: algoritmo no reconocido: " << alg << "\n";
        return 4;
    }

    auto t1 = chrono::steady_clock::now();

    string out_dir = "data/matrix_output/";
    string out_name = basename_no_ext(path1) + "_x_" + basename_no_ext(path2) + "_out.txt";
    string out_path = out_dir + out_name;

    write_matrix(C, out_path);

    long long us = chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
    long kb = peak_kb();

    ensure_parent_dirs(metrics_path);
    bool new_file = !filesystem::exists(metrics_path);

    ofstream mf(metrics_path, ios::app);
    if (mf) {
        if (new_file) {
            mf << "algorithm,time_ns,peak_kb,mat1_dims,mat2_dims,output_file\n";
        }
        string d1 = to_string(A.size()) + "x" + to_string(A[0].size());
        string d2 = to_string(B.size()) + "x" + to_string(B[0].size());
        mf << alg << "," << us << "," << kb << ","
           << "\"" << d1 << "\"" << "," << "\"" << d2 << "\"" << ","
           << "\"" << out_path << "\"" << "\n";
    } else {
        cerr << "Advertencia: no se pudo abrir archivo de métricas: " << metrics_path << "\n";
    }

    return 0;
}