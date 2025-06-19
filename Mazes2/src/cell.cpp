#include "cell.h"
#include <memory>
#include <unordered_map>
#include <vector>

class Cell
{
public:
    Cell();
    ~Cell();

    // Getter methods for row and colunn
    int getRow() const { return row; }
    int getColunn() const { return colunn; }

    std::vector<Cell> getLinkedCells() const
    {
        std::vector<Cell> keys;
        for (const auto &pair : links)
        {
            keys.push_back(pair.first);
        }
        return keys;
    }

    std::vector<Cell> getNeighbors() const
    {
        std::vector<Cell> neighbors;
        if (north)
            neighbors.push_back(*north);
        if (south)
            neighbors.push_back(*south);
        if (east)
            neighbors.push_back(*east);
        if (west)
            neighbors.push_back(*west);
        return neighbors;
    }

    bool isLinked(const Cell &cell) const
    {
        return links.find(cell) != links.end();
    }

    // Equality operator
    bool operator==(const Cell &other) const
    {
        return row == other.row && colunn == other.colunn;
    }

    void link(Cell &cell, const bool bidirectional = true);
    void unlink(Cell &cell, const bool bidirectional = true);

private:
    // Member variables
    int row;
    int colunn;

    std::shared_ptr<Cell> north;
    std::shared_ptr<Cell> south;
    std::shared_ptr<Cell> east;
    std::shared_ptr<Cell> west;

    std::unordered_map<Cell, bool, CellHash> links;

    Cell &operator=(const Cell &other)
    {
        if (this != &other)
        {
            row = other.row;
            colunn = other.colunn;
            north = other.north;
            south = other.south;
            east = other.east;
            west = other.west;
            links = other.links;
        }
        return *this;
    }
};

Cell::Cell() : row(0), colunn(0), north(nullptr), south(nullptr), east(nullptr), west(nullptr) {}

struct CellHash
{
    std::size_t operator()(const Cell &cell) const
    {
        return std::hash<int>()(cell.getRow()) ^ (std::hash<int>()(cell.getColunn()) << 1);
    }
};

Cell::Cell(const Cell &other)
    : row(other.row), colunn(other.colunn),
      north(other.north), south(other.south),
      east(other.east), west(other.west),
      links(other.links) {}

void Cell::link(Cell &cell, const bool bidirectional)
{
    links[cell] = true;
    if (bidirectional)
    {
        cell.link(*this, false);
    }
}

void Cell::unlink(Cell &cell, const bool bidirectional)
{
    links.erase(cell);
    if (bidirectional)
    {
        cell.unlink(*this, false);
    }
}
