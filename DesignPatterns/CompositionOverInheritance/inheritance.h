#include <iostream>

// Defining some properties. They should be in their own headers.
class Object {
public:
  virtual void update() {}
  virtual void draw() {}
  virtual void collide(Object objects[]) {}
};

class Visible : virtual public Object {
public:
  virtual void draw() override {
    // Code to draw a model
    std::cout << "Hello! I am visible." << std::endl;
  }
};

class Solid : virtual public Object {
public:
  virtual void collide(Object objects[]) override {
    std::cout << "Booom!" << std::endl;
  }
};

class Movable : virtual public Object {
public:
  virtual void update() override { std::cout << "Moving..." << std::endl; }
};

// Using the properties to define behaviors in new classes
// We need virtual inheritance to avoid creating multiple copies of the base
// class.
class Player : virtual public Solid,
               virtual public Movable,
               virtual public Visible {};

// The cloud is not solid, implicitly through the base Object class
class Cloud : virtual public Movable, virtual public Visible {};

// The building is  not movable, implicitly through the base Object class
class Building : virtual public Solid, virtual public Visible {};

// The trap ie neither visible or movable
class Trap : virtual public Solid {};
