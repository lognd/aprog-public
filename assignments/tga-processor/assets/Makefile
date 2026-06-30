CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
SRCS     = src/main.cpp src/tga.cpp src/operations.cpp
TARGET   = project1.out

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

clean:
	rm -f $(TARGET)
