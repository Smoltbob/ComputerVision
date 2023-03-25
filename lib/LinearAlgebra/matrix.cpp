#include <iostream>
#include <vector>
#include <utility>
#include <cassert>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

auto transpose(std::vector<std::vector<double>> const &matrix) -> std::vector<std::vector<double>>
{
    assert(matrix.size() > 2);
    std::vector<std::vector<double>> output{};
    for (auto const &row : matrix)
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

auto compute_determinant_3x3(std::vector<std::vector<double>> const &matrix) -> double
{
    // Since we know it's 3x3, we can use an array
    assert(matrix.size() == 3);
    for (auto const &row : matrix)
    {
        assert(row.size() == 3);
    }
    double const a{matrix[0][0]};
    double const b{matrix[0][1]};
    double const c{matrix[0][2]};
    double const d{matrix[1][0]};
    double const e{matrix[1][1]};
    double const f{matrix[1][2]};
    double const g{matrix[2][0]};
    double const h{matrix[2][1]};
    double const i{matrix[2][2]};

    return a * e * i + b * f * g +
           c * d * h - c * e * g -
           b * d * i - a * f * h;
}

PYBIND11_MODULE(matrix, m)
{
    m.def("transpose", &transpose, "Transpose a square matrix");
}