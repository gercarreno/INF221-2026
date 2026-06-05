#!/bin/bash

EXECUTABLE="bin/sorting"
INPUT_DIR="data/array_input"
MEASUREMENTS_DIR="data/measurements"

echo "Pruebas de ordenamiento..."

if [ ! -x "$EXECUTABLE" ]; then
  echo "Error: no encuentro el ejecutable en '$EXECUTABLE'." >&2
  exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
  echo "Error: no existe el directorio de entrada '$INPUT_DIR'." >&2
  exit 1
fi

mkdir -p "$MEASUREMENTS_DIR"

for alg in merge quick sort; do
  echo "Algoritmo: '$alg'"
  OUTPUT_FILE="${MEASUREMENTS_DIR}/metrics_${alg}.csv"
  rm -f "$OUTPUT_FILE"

  found_any=0

  # Recorre entradas del directorio
  for input_file in "$INPUT_DIR"/*; do
    # Si no hay coincidencias, salimos del bucle
    if [ ! -e "$input_file" ]; then
      break
    fi

    if [ -f "$input_file" ]; then
      found_any=1
      filename=$(basename "$input_file")
      echo "Procesando: $filename"

      "$EXECUTABLE" "$alg" "$input_file" "$OUTPUT_FILE"
      if [ $? -ne 0 ]; then
        echo "Advertencia: falló '$alg' con $filename" >&2
      fi
    fi
  done

  if [ "$found_any" -eq 0 ]; then
    echo "No se encontraron archivos en '$INPUT_DIR'."
  else
    echo "Resultados en: $OUTPUT_FILE"
  fi
  echo "----------------------------------------------------"
done

echo "Todos los algoritmos fueron ejecutados."
