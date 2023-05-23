#include <cstdint>
#include "Mazes/cell.h"
#include <vector>

class Grid
{
    private:
        std::uint16_t rows{0U};
        std::uint16_t cols{0U};
        std::vector<std::vector<Cell>> grid{};


    public:
        Grid();

        Grid(const std::int16_t& rows, const std::uint16_t& cols): rows(rows), cols(cols) 
        {
            for (std::uint16_t  row{0U}; row < rows; ++row)
            {
                grid.push_back(std::vector<Cell>());
                for (std::uint16_t  col{0U}; col < cols; ++col)
                {
                    grid[row].push_back(Cell());
                }
            }
        };
};
