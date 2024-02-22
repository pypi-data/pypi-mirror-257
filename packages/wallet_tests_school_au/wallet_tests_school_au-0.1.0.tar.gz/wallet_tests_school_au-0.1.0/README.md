Command to compile the code:

c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) wallet.cpp -o wallet.so