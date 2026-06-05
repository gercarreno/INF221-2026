/*
 * Quick Sort (Hoare + pivote aleatorio)
 * Autor: Gerardo Carreño
 *
 * Complejidad:
 *   - Mejor caso: O(n log n)
 *   - Caso promedio: O(n log n)
 *   - Peor caso: O(n^2) 
 *
 * Referencias:
 *  GeekforGeeks (https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/)
 */

#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <vector>
using namespace std;

// Particionamiento Hoare: usa arr[low] como pivote (después de randomizar)
int partition_hoare(vector<int>& arr, int low, int high) {
    int pivot = arr[low];
    int i = low - 1;
    int j = high + 1;

    while (true) {
        do { ++i; } while (arr[i] < pivot);
        do { --j; } while (arr[j] > pivot);

        if (i >= j) {
            return j; // punto de corte
        }
        swap(arr[i], arr[j]);
    }
}

// Randomiza el pivote y delega en Hoare
int partition_r_hoare(vector<int>& arr, int low, int high) {
    static bool seeded = false;
    if (!seeded) { srand((unsigned)time(NULL)); seeded = true; }

    int randomIndex = low + rand() % (high - low + 1);
    swap(arr[low], arr[randomIndex]); // mover pivote aleatorio a 'low'
    return partition_hoare(arr, low, high);
}

void quickSortRecursive(vector<int>& arr, int low, int high) {
    if (low < high) {
        int p = partition_r_hoare(arr, low, high);
        quickSortRecursive(arr, low, p);      // nota: incluye p
        quickSortRecursive(arr, p + 1, high); // y continúa desde p+1
    }
}

void quickSort(vector<int>& arr) {
    if (arr.empty()) {
        return;
    }
    quickSortRecursive(arr, 0, (int)arr.size() - 1);
}
