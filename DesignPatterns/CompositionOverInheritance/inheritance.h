#include <iostream>
#include <string>

// Defining some properties. They should be in their own headers.
class Object {
public:
  virtual std::string update() { return ""; }
  virtual std::string draw() { return ""; }
  virtual std::string collide(Object objects[]) { return ""; }
};

class Visible : virtual public Object {
public:
  virtual std::string draw() override {
    // Code to draw a model
    return "Hello! I am visible.";
  }
};

class Solid : virtual public Object {
public:
  virtual std::string collide(Object objects[]) override { return "Booom!"; }
};

class Movable : virtual public Object {
public:
  virtual std::string update() override { return "Moving..."; }
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
