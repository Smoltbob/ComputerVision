#include <iostream>
#include <sstream>
#include <pybind11/pybind11.h>

#include "Mazes/cell.h"

int do_something() { 
   return 42;
}


PYBIND11_MODULE(cell, m) {
    m.doc() = "Python bindings for the Cell class";

     m.def("do_something", &do_something, "A function that does something");

    pybind11::class_<Cell>(m, "Cell")
        .def(pybind11::init<>())
        .def("__repr__", [](Cell const& self) {
            std::stringstream ss;
            ss << self;
            return ss.str();
        });
}