# Documentación

Este proyecto contiene dos módulos principales: uno para la multiplicación de matrices y otro para el ordenamiento de arreglos. A continuación, se detalla la estructura y el uso de cada uno.

-----

## Multiplicación de matrices

Este módulo compara el rendimiento del algoritmo de multiplicación de matrices **Naive** con el algoritmo de **Strassen**.

### Programa principal

El programa principal se encuentra en `matrix_multiplication.cpp` y se encarga de:

  - Leer dos matrices desde archivos de texto.
  - Multiplicarlas utilizando el algoritmo especificado (`naive` o `strassen`).
  - Medir el tiempo de ejecución y el uso de memoria.
  - Guardar la matriz resultante y las métricas en archivos de salida.

**Algoritmos implementados:**

  - **Naive**: Implementación clásica con complejidad **O(n³)**.
  - **Strassen**: Implementación clásica (más detalles en `strassen.cpp`). !!!!Esta implementación se demora aproximadamente 20 [min] en correr todas las matrices, es un poco inviable. Si desea correr en menos tiempo el algoritmo, limitar la generación de matrices. 

**Compilación y ejecución:**
El proyecto se gestiona con un `makefile`. Para compilar y ejecutar todo el proceso (limpieza, compilación, generación de datos, pruebas y gráficos), utilice el comando:

```bash
make
```

### Scripts

  - **`matrix_generator.py`**: Este script genera pares de matrices cuadradas con diferentes propiedades (densas, diagonales, dispersas) y dominios de valores ({0,1} o {0..9}). Guarda las matrices en el directorio `data/matrix_input/`.
  - **`runner.sh`**: Ejecuta el programa principal para cada algoritmo (`naive`, `strassen`) sobre todos los pares de matrices generados, guardando las métricas de rendimiento en `data/measurements/`.
  - **`plot_generator.py`**: Lee los archivos de métricas y genera los siguientes gráficos comparativos en `data/plots/`:
      - Tiempo de ejecución vs. Dimensión de la matriz.
      - Uso de memoria vs. Dimensión de la matriz.
      - Comparativa de tiempo y memoria para la dimensión más grande.

-----

## Ordenamiento de arreglo

Este módulo evalúa el rendimiento de diferentes algoritmos de ordenamiento.

### Programa principal

El programa `sorting.cpp` lee un arreglo desde un archivo, lo ordena con el algoritmo indicado, y guarda el resultado y las métricas de rendimiento.

**Algoritmos implementados:**
  - **`mergeSort`**: Ordenamiento por mezcla, con complejidad **O(n log n)** en todos los casos.
  - **`quickSort`**: Implementado con partición de Hoare y pivote aleatorio. Su complejidad promedio es **O(n log n)**, pero puede decaer a **O(n²)** en el peor caso.
  - **`sort`**: Implementación del `std::sort` de C++, un algoritmo híbrido muy optimizado (Introsort).

**Compilación y ejecución:**
Al igual que el módulo anterior, se utiliza un `makefile`. El comando `make` ejecuta todo el ciclo.

### Scripts

  - **`array_generator.py`**: Crea archivos de texto con arreglos de diferentes tamaños, tipos (ascendente, descendente, aleatorio) y dominios de valores. Los archivos se guardan en `data/array_input/`.
  - **`runner.sh`**: Itera sobre los algoritmos (`merge`, `quick`, `sort`) y los archivos de entrada para recolectar las métricas de rendimiento, que se almacenan en `data/measurements/`.
  - **`plot_generator.py`**: Procesa los datos de métricas para generar los siguientes gráficos en `data/plots/`:
      - Tiempo de ejecución vs. Cantidad de elementos para cada tipo de dato (aleatorio, ascendente, descendente).
      - Uso de memoria vs. Cantidad de elementos.
      - Comparativa de tiempo para un tamaño de N grande (ej. 100,000).
