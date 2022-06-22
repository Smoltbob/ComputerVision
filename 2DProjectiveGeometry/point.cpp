#include <iostream>

class point
{
    // TOOD
    // represent using a vector ? or just 2 / 3 coordinates ? make it generic to any dimension ?
public:
    int x;
    int y;
    int z;

    /// Constructs a point at the origin
    ///
    point() = default;

    /// TODO default value for z
    point(int const &x, int const &y, int z) : x{x}, y{y}, z{z}
    {
    }

    auto operator<<(Ostream &os)
    {
        os << "{ " << x << y << z << " }";

        return os;
    }
}