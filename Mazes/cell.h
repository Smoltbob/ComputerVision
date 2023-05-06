#include <cstdint>
#include <iostream>

class Cell
{
    private:
        std::uint16_t row{0U};
        std::uint16_t col{0U};

    public:
        
        auto friend operator<<(std::ostream& os, const Cell& cell) -> std::ostream& 
        {
            os << "Cell location: row = " << cell.row <<  ", col = " << cell.col;
            return os;
        }

};