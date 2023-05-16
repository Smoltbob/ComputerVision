#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

class Cell
{
    private:
        std::uint16_t row{0U};
        std::uint16_t col{0U};

        // Accessors to the immediate neighbors
        std::shared_ptr<Cell> north{};
        std::shared_ptr<Cell> south{};
        std::shared_ptr<Cell> east{};
        std::shared_ptr<Cell> west{};

        // Keeps track of which neighboring cells are linked
        // TODO use a set or prevent linking twice
        std::vector<std::shared_ptr<Cell>> links{};

    public:

        auto friend operator<<(std::ostream& os, const Cell& cell) -> std::ostream& 
        {
            os << "Cell location: row = " << cell.row <<  ", col = " << cell.col;
            return os;
        }

        // Connects the cell to the cell parameter
        auto link(const Cell& cell, const bool& bidi) -> void
        {
            links.push_back(std::make_shared<Cell>(cell));
        }

};