#include <memory>
#include <string>

// Define the interface for each product of a house
class Door {
public:
  virtual std::string doorColor() = 0;
};

class Roof {
public:
  virtual std::string roofColor() = 0;
};

class Wall {
public:
  virtual std::string wallColor() = 0;
};

// Define some concrete classes for making different families of products
class BlueDoor : Door {
public:
  virtual std::string doorColor() override { return "Blue Door"; };
};

class RedDoor : Door {
public:
  virtual std::string doorColor() override { return "Red Door"; };
};

class BlueRoof : Roof {
public:
  virtual std::string roofColor() override { return "Blue Roof"; };
};

class RedRoof : Roof {
public:
  virtual std::string roofColor() override { return "Red Roof"; };
};

class BlueWall : Wall {
public:
  virtual std::string wallColor() override { return "Blue Wall"; };
};

class RedWall : Wall {
public:
  virtual std::string wallColor() override { return "Red Wall"; };
};

// Define our family of products, as well as some variants.

class HouseFactory {
public:
  virtual std::unique_ptr<Door> createDoor() const = 0;
  virtual std::unique_ptr<Roof> createRoof() const = 0;
  virtual std::unique_ptr<Wall> createWall() const = 0;
  virtual ~HouseFactory() = 0;
};