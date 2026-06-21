# Documentación

En el presente archivo se encuentra el detalle de todas las implementaciones de la tarea.

## Reproducibilidad
### Prerrequisitos
En tu entorno de trabajo debes tener instalado:
+ `python3`
+ `g++` 
+ `python3-venv` (Opcional)

### Puesta en marcha
Primero debes crear un entorno virtual en python:
```bash
python3 -m venv .venv
```
Luego instalar todas las dependencias necesarias
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
Finalmente puedes correr el `makefile`;
```bash
make build
```

## Implementación

### Estructuras y funciones auxiliares

`anime.h`

Header compartido por todas las implementaciones. Se definen los structs, las firmas de algunas funciones

**Estructuras**

| Struct | Campos | Descripción |
|---|---|---|
| `Capitulo` | `tiempo`, `energia`, `satisfaccion` | Costo y satisfacción de un capítulo individual. |
| `Anime` | `n_cap`, `bono`, `nombre`, `capitulos` | Un anime con su cantidad de capítulos, un bono por completarlo y la lista de sus capítulos. |
| `anime_ratio` | `id_anime`, `k_capitulos`, `ratio`, `tiempo_k`, `energia_k`, `satisfaccion_k` | Usada por `greedy1.cpp` para representar la opción de ver los primeros `k` capítulos de un anime junto con su ratio satisfacción/recursos. |

**Funciones auxiliares**

- `calcular_tiempo(anime, k)`: tiempo total de ver los primeros `k` capítulos del anime.
- `calcular_energia(anime, k)`: energía total de ver los primeros `k` capítulos del anime.
- `calcular_satisfaccion(anime, k)`: satisfacción total de ver los primeros `k` capítulos.

### Algoritmos

| Archivo | Enfoque |
|---|---|
| `brute-force.cpp` | Fuerza bruta |
| `dynamic-programming.cpp` | Programación dinámica |
| `greedy1.cpp` | Heurística greedy ratio |
| `greedy2.cpp` | Heurística greedy max |

### Programa principal

`general.cpp`

Para cada caso:
- Lee el archivo de entrada (`./data/inputs/`) con la lista de animes y sus capítulos.
- Ejecuta `backtracking` (fuerza bruta, solo si `n <= 25`), `anime_greedy` (greedy ratio), `anime_max` (greedy máximo) y `knapsack_anime` (DP).
- Mide el tiempo de ejecución (`chrono::high_resolution_clock`) y la memoria pico utilizada (mediante sobrecarga de `operator new`/`operator delete`).
- Escribe los resultados individuales en `./data/outputs/` y agrega las métricas (tiempo, memoria, satisfacción) en `./data/measurements/measurements.csv`.

### Scripts

Se cuenta con dos scripts: `plot_generator.py` y `testcases_generator.py`.

#### `testcases_generator.py`

Genera los casos de prueba utilizados por `general.cpp`, guardándolos en `./data/inputs/`.

- Crea casos con distintos tamaños de `n` (número de animes): pequeños (`3, 5, 8`), medianos (`20, 40, 80`) y grandes (`100, 150, 200`), con 3 casos por cada tamaño.
- Para cada caso genera nombres de anime aleatorios, una cantidad de capítulos por anime (`q_i`, máximo 30, con un total acumulado `Q <= 700`), un bono aleatorio, y por cada capítulo valores aleatorios de tiempo, energía y satisfacción.
- También genera `M` (minutos disponibles) y `E` (energía disponible) aleatorios para cada caso.
- Soporta los flags `--small`, `--medium` y `--large` para generar solo un subconjunto; sin flags, genera todos los tamaños.

#### `plot_generator.py`

Genera las visualizaciones a partir de `./data/measurements/measurements.csv`, guardándolas en `./data/plots/`.

- `tiempo_algoritmos.png`: tiempo de ejecución vs. N, separado por algoritmo.
- `tiempo_escalamiento.png`: comparación de escalamiento entre DP/greedy (polinomial) y fuerza bruta (exponencial).
- `memoria_algoritmos.png`: uso de memoria vs. N, separado por algoritmo.
- `calidad_inputs.png`: impacto de variables de entrada (N, capítulos totales, M, E) en la calidad de las heurísticas greedy respecto al óptimo (DP).
- `calidad_greedys.png`: comparación directa de calidad entre ambas heurísticas greedy.
- `distribucion.png`: distribución estadística (boxplot) de la calidad de las heurísticas.
- `comportamiento_recursos.png`: relación entre la satisfacción total y las variables de entrada.
- `complejidad_empirica.png`: complejidad empírica de DP (en función de M·E·capítulos) y de fuerza bruta.
- `tradeoff_calidad_tiempo.png`: trade-off entre calidad de solución y tiempo de ejecución.
- `greedy_winrate.png`: cantidad de casos en que cada heurística greedy supera a la otra.

La calidad heurística se calcula como el porcentaje de la satisfacción obtenida por cada algoritmo respecto a la satisfacción óptima reportada por DP.