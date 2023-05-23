#include <iostream>
#include <sstream>
#include <pybind11/pybind11.h>
#include <cstdint>

#include "Mazes/grid.h"


PYBIND11_MODULE(grid, m) {
    m.doc() = "Python bindings for the Grid class";

    pybind11::class_<Grid>(m, "Grid")
        .def(pybind11::init<std::uint16_t, std::uint16_t>())
        .def("__repr__", [](Grid const& self) {
            std::stringstream ss;
            ss << "Maze";
            return ss.str();
        });
}