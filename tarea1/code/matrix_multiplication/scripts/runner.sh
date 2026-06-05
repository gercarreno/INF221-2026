#!/bin/bash


EXECUTABLE="bin/matrix_multiplication"
INPUT_DIR="data/matrix_input"
MEASUREMENTS_DIR="data/measurements"

echo "Pruebas para la multiplicación de matrices..."

if [ ! -x "$EXECUTABLE" ]; then
  echo "Error: no encuentro el ejecutable en '$EXECUTABLE'." >&2
  exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
  echo "Error: no existe el directorio de entrada '$INPUT_DIR'." >&2
  exit 1
fi

mkdir -p "$MEASUREMENTS_DIR"

for alg in naive strassen; do
  echo "Algoritmo: '$alg'"
  METRICS_FILE="${MEASUREMENTS_DIR}/metrics_${alg}.csv"
  rm -f "$METRICS_FILE"

  found_any=0

  # Recorre entradas *_1.txt y busca su par *_2.txt
  for mat1_path in "$INPUT_DIR"/*_1.txt; do
    # Si no hay coincidencias, salimos del bucle
    if [ ! -e "$mat1_path" ]; then
      break
    fi

    mat2_path="${mat1_path%_1.txt}_2.txt"
    if [ -f "$mat2_path" ]; then
      found_any=1
      mat1_name=$(basename "$mat1_path")
      mat2_name=$(basename "$mat2_path")
      echo "Procesando: $mat1_name y $mat2_name"

      "$EXECUTABLE" "$alg" "$mat1_path" "$mat2_path" "$METRICS_FILE"
      if [ $? -ne 0 ]; then
        echo "Advertencia: falló la ejecución con $mat1_name y $mat2_name" >&2
      fi
    fi
  done

  if [ "$found_any" -eq 0 ]; then
    echo "No se encontraron pares *_1.txt / *_2.txt en '$INPUT_DIR'."
  else
    echo "Resultados en: $METRICS_FILE"
  fi
done

echo "Todas las pruebas de multiplicación han finalizado."
