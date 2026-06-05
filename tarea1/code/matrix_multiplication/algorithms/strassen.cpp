/*
* Strassen
* Autor: Gerardo Carreño
*
* Complejidad O(n^2.81)
* Notas:
* - Se asume que A y B son matrices cuadradas de tamaño potencia de dos.
* - Sin padding y sin threshold: solo caso base n == 1.
* - A nivel teórico, el algoritmo de Strassen con complejidad O(n^2.81) debería
* ser más rápido que el algoritmo Naive O(n^3) para matrices grandes. Sin
* embargo, esta implementación en particular es drásticamente MÁS LENTA
* debido a una ineficiencia crítica en la gestión de memoria.
*
* El problema principal es la creación y copia masiva de matrices
* temporales en cada llamada recursiva.
*
* 1. En cada paso, se crean 8 nuevas submatrices
* (a11..a22, b11..b22) y los datos de las matrices originales se copian
* en ellas.
*
* 2. Resultados Intermedios
* Las funciones add y sub también crean
* nuevas matrices para devolver sus resultados, lo que se suma a la
* sobrecarga.
*
* 3. Sobrecarga de Memoria:
*  crear un vector es una operación muy costosa para el sistema
* operativo. Repetir este proceso miles de veces en la recursión genera
* un cuello de botella que anula por completo la ganancia teórica de
* reducir el número de multiplicaciones.
*
* En contraste, el algoritmo Naive, aunque realiza más operaciones
* aritméticas, es extremadamente eficiente con la memoria: crea una única
* matriz de resultado y accede a los datos de forma secuencial, lo que
* aprovecha de manera óptima la caché del procesador.
*
*
* Referencias:
* - https://www.geeksforgeeks.org/dsa/strassens-matrix-multiplication/
*/
#include <vector>
#include <stdexcept>
using namespace std;


vector<vector<int>> add(const vector<vector<int>>& A, const vector<vector<int>>& B) {
    size_t n = A.size();
    vector<vector<int>> C(n, vector<int>(n, 0));
    for (size_t i = 0; i < n; ++i)
        for (size_t j = 0; j < n; ++j)
            C[i][j] = A[i][j] + B[i][j];
    return C;
}

vector<vector<int>> sub(const vector<vector<int>>& A, const vector<vector<int>>& B) {
    size_t n = A.size();
    vector<vector<int>> C(n, vector<int>(n, 0));
    for (size_t i = 0; i < n; ++i)
        for (size_t j = 0; j < n; ++j)
            C[i][j] = A[i][j] - B[i][j];
    return C;
}

vector<vector<int>> strassen_multiply(const vector<vector<int>>& A, const vector<vector<int>>& B) {
    size_t n = A.size();

    if (n == 1) {
        vector<vector<int>> C(1, vector<int>(1));
        C[0][0] = A[0][0] * B[0][0];
        return C;
    }
    size_t s = n / 2;

    // Particionar A y B
    vector<vector<int>> a11(s, vector<int>(s)), a12(s, vector<int>(s)),
                        a21(s, vector<int>(s)), a22(s, vector<int>(s));
    vector<vector<int>> b11(s, vector<int>(s)), b12(s, vector<int>(s)),
                        b21(s, vector<int>(s)), b22(s, vector<int>(s));

    for (size_t i = 0; i < s; ++i) {
        for (size_t j = 0; j < s; ++j) {
            a11[i][j] = A[i][j];
            a12[i][j] = A[i][j + s];
            a21[i][j] = A[i + s][j];
            a22[i][j] = A[i + s][j + s];

            b11[i][j] = B[i][j];
            b12[i][j] = B[i][j + s];
            b21[i][j] = B[i + s][j];
            b22[i][j] = B[i + s][j + s];
        }
    }

    // m1..m7
    vector<vector<int>> m1 = strassen_multiply(add(a11, a22), add(b11, b22));
    vector<vector<int>> m2 = strassen_multiply(add(a21, a22), b11);
    vector<vector<int>> m3 = strassen_multiply(a11, sub(b12, b22));
    vector<vector<int>> m4 = strassen_multiply(a22, sub(b21, b11));
    vector<vector<int>> m5 = strassen_multiply(add(a11, a12), b22);
    vector<vector<int>> m6 = strassen_multiply(sub(a21, a11), add(b11, b12));
    vector<vector<int>> m7 = strassen_multiply(sub(a12, a22), add(b21, b22));

    // c11..c22
    vector<vector<int>> c11 = sub(add(m1, m4), sub(m5, m7));        // m1 + m4 - m5 + m7
    vector<vector<int>> c12 = add(m3, m5);
    vector<vector<int>> c21 = add(m2, m4);
    vector<vector<int>> c22 = add(sub(add(m1, m3), m2), m6);        // m1 - m2 + m3 + m6

    // Ensamblar C
    vector<vector<int>> C(n, vector<int>(n, 0));
    for (size_t i = 0; i < s; ++i) {
        for (size_t j = 0; j < s; ++j) {
            C[i][j]         = c11[i][j];
            C[i][j + s]     = c12[i][j];
            C[i + s][j]     = c21[i][j];
            C[i + s][j + s] = c22[i][j];
        }
    }
    return C;
}