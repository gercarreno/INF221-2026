# Compilador
CXX = g++
CXXFLAGS = -std=c++20 -O2 -Wall -Wextra -g
TARGET = animaraton

# Encuentra automáticamente todos los archivos .cpp en el directorio
# (Asume que general.cpp, dynamic-programming.cpp, etc., están aquí)
SRCS = $(wildcard *.cpp) $(wildcard */*.cpp)

# Convierte la lista de .cpp en una lista de archivos objeto .o
OBJS = $(SRCS:.cpp=.o)

# Regla principal: compila todo y genera el ejecutable
all: $(TARGET)

# Regla para enlazar los objetos y crear el ejecutable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Regla genérica para compilar cualquier .cpp en un .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@
clean:
	rm -f $(OBJS) $(TARGET)

# Regla para limpiar y volver a compilar todo desde cero
# Ejecutar usando: make rebuild
rebuild: clean all

.PHONY: all clean rebuild
