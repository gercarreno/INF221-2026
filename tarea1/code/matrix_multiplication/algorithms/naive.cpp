/*
* Naive
* Autor: Gerardo Carreño
*
* Complejidad O(n^3)
*
* Referencias:
* - https://www.geeksforgeeks.org/dsa/strassens-matrix-multiplication/
*
*/

#include <iostream>
#include <vector>
#include <stdexcept>
using namespace std;

vector<vector<int>> naive_multiply(const vector<vector<int>> &mat1, const vector<vector<int>> &mat2) {

    // Validar que las dimensiones sean compatibles para A_{n x m} * B_{m x q}
    if (mat1.empty() || mat1[0].empty() || mat2.empty() || mat2[0].empty() || mat1[0].size() != mat2.size()) {
        throw invalid_argument("Dimensiones incompatibles para la multiplicación de matrices.");
    }

    // Dimensiones de las matrices
    size_t n = mat1.size();      // Filas de mat1
    size_t m = mat1[0].size();   // Columnas de mat1 (y filas de mat2)
    size_t q = mat2[0].size();   // Columnas de mat2

    // Matriz de resultado C_{n x q}, inicializada en ceros.
    vector<vector<int>> res(n, vector<int>(q, 0));

    // Cálculo de C[i][j] = (A[i][k] * B[k][j])
    for (size_t i = 0; i < n; i++) {
        for (size_t k = 0; k < m; k++) {   
            int tmp = mat1[i][k];           // Evitar accesos repetidos a mat1[i][k]
            for (size_t j = 0; j < q; j++) { 
                res[i][j] += tmp * mat2[k][j];
            }
        }
    }

    return res;
}