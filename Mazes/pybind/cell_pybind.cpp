#include <iostream>
#include <pybind11/pybind11.h>

#include "Mazes/cell.h"

PYBIND11_MODULE(cell, m) {
    m.doc() = "Python bindings for the Cell class";

    pybind11::class_<Cell>(m, "Cell")
        .def(pybind11::init<>());
}