# compilador
CXX = g++
CXXFLAGS = -std=c++20 -O2 -Wall -Wextra -g -MMD -MP
TARGET = animaraton

# archivos .cpp en el dir
SRCS = $(wildcard *.cpp) $(wildcard */*.cpp)

# .cpp en una lista de archivos objeto .o
OBJS = $(SRCS:.cpp=.o)
DEPS = $(OBJS:.o=.d)

# compila y genera el ejecutable
all: $(TARGET)

#enlazar los objetos y crear el ejecutable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# compilar cualquier .cpp en un .o
%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@
-include $(DEPS)

clean:
	rm -f $(OBJS) $(DEPS) $(TARGET)
clean-data:
	rm -f ./data/inputs/* ./data/outputs/* ./data/measurements/*

#número de archivos
N ?= 100

data:
	python3 ./scripts/testcases_generator.py
plot:
	python3 ./scripts/plot_generator.py

# make rebuild
rebuild: clean all
.PHONY: all clean rebuild clean-data data plot
