#include <iostream>
#include <string>

// From page 41 of move semantics

class C {
private:
  std::string name;

public:
  C(std::string const &n) : name{n} { std::cout << "DEFAULT " << name << "\n"; }

  C(C &&c_obj) : name{std::move(c_obj.name)} {
    std::cout << "MOVE " << name << "\n";
  }
};

C fun() { return C{"From fun"}; }

int main() {
  C my_c{"name"};
  C my_c2{C{
      "name"}}; // Defaults because of copy ellision. Disable with
                // -fno-elide-constructors
                // https://stackoverflow.com/questions/15040784/how-to-write-move-so-that-it-can-potentially-be-optimized-away
  C my_c3{std::move(my_c2)};
  C my_c4{fun()};
}
