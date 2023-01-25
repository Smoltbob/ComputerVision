#include <iostream>
#include <pybind11/pybind11.h>



int do_something() { 
   return 42;
}

PYBIND11_MODULE(example, m) {
    m.def("do_something", &do_something, "A function that does something");
}