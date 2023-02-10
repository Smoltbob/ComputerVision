#include <iostream>
#include <vector>
#include <utility>
#include <cassert>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


std::vector<std::vector<double>> transpose(std::vector<std::vector<double>>const& matrix) { 
   assert(matrix.size() > 2);
   std::vector<std::vector<double>> output{};
   for (auto const& row: matrix)
   {
        assert(matrix.size() == row.size());
   }
  
   for (std::size_t i = 0; i < matrix.size(); ++i)
   {
        std::vector<double> new_row{};
        for (std::size_t j = 0; j < matrix.size(); ++j)
        {
            new_row.push_back(matrix.at(j).at(i));
        }
        output.push_back(new_row);

   }
   return output;
}

PYBIND11_MODULE(matrix, m) {
    m.def("transpose", &transpose, "Transpose a square matrix");
}