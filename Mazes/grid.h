#include <cstdint>

class Grid
{
    private:
        std::uint16_t rows{0U};
        std::uint16_t cols{0U};

    public:
        Grid();

        Grid(const std::int16_t&, const std::uint16_t& cols): rows(rows), cols(cols) {};
};
