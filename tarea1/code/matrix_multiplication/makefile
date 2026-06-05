CXX      = g++
CXXFLAGS = -O2 -g -Wall -Wextra -pedantic

BIN_DIR  = bin
OBJ_DIR  = obj
TARGET   = $(BIN_DIR)/matrix_multiplication

SRCS     := $(wildcard *.cpp) $(wildcard algorithms/*.cpp)
OBJS     := $(patsubst %.cpp,$(OBJ_DIR)/%.o,$(SRCS))

.PHONY: run all clean test generate_data plot


run: clean all test plot
	@echo "Proceso completado exitosamente."

all: $(TARGET)

test: $(TARGET) generate_data
	@echo "Corriendo script de pruebas..."
	@chmod +x scripts/runner.sh
	@./scripts/runner.sh

generate_data:
	@echo "Preparando datos para las pruebas..."
	@echo "Limpiando directorios de datos..."
	@rm -f data/matrix_input/*
	@rm -f data/matrix_output/*
	@echo "Generando nuevas matrices con el script de Python..."
	@python3 scripts/matrix_generator.py

plot:
	@echo "Generando gráficos de resultados..."
	@python3 scripts/plot_generator.py

clean:
	@echo "Limpiando artefactos de compilación..."
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@rm -f data/matrix_input/*
	@rm -f data/matrix_output/*
	@rm -f data/measurements/*

# Enlazar el ejecutable final
$(TARGET): $(OBJS) | $(BIN_DIR)
	@echo "\n Enlazando ejecutable..."
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

# Compilar los archivos fuente (.cpp) a archivos objeto (.o)
$(OBJ_DIR)/%.o: %.cpp
	@echo "Compilando $<..."
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Crear directorios 'bin' y 'obj' si no existen
$(BIN_DIR) $(OBJ_DIR):
	@mkdir -p $@
