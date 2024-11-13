#include <iostream>
#include <string>
// Demonstrating the principle of composition.
// Each component is defined by a class, with subclasses for each variant.

// Defines Visibility
class VisibilityDelegate {
public:
  virtual std::string draw() = 0;
};

class NotVisible : public VisibilityDelegate {
public:
  virtual std::string draw() override { return ""; }
};

class Visible : public VisibilityDelegate {
public:
  virtual std::string draw() override { return "Hello! I am visible."; }
};

// Defines Movability
class UpdateDelegate {
public:
  virtual std::string update() = 0;
};

class NotMoveable : public UpdateDelegate {
  virtual std::string update() override { return ""; }
};

class Moveable : public UpdateDelegate {
public:
  virtual std::string update() override { return "Moving..."; }
};

// Defines solidity
class CollisionDelegate {
public:
  virtual std::string collide(Object objects[]) = 0;
};

class NotSolid : public CollisionDelegate {
public:
  virtual std::string collide(Object objects[]) override { return ""; }
};

class Solid : public CollisionDelegate {
public:
  virtual std::string collide(Object objects[]) override { return "Booom !"; }
};

// We can now define the Object class, composed of our defined properties.
class Object {
  // TODO replace pointers with references ?
  VisibilityDelegate *_v;
  UpdateDelegate *_u;
  CollisionDelegate *_c;

public:
  Object(VisibilityDelegate *v, UpdateDelegate *u, CollisionDelegate *c)
      : _v(v), _u(u), _c(c) {}

  void update() { _u->update(); };

  void draw() { _v->draw(); };

  void collide(Object objects[]) { _c->collide(objects); };
};

// Finally we  can buildd our concrete classes
class Player : public Object {
public:
  Player() : Object(new Visible(), new Moveable(), new Solid()) {}
};

class Cloud : public Object {
public:
  Cloud() : Object(new Visible(), new Moveable(), new NotSolid()) {}
};

class Building : public Object {
public:
  Building() : Object(new Visible(), new NotMoveable(), new Solid()) {}
};

class Trap : public Object {
public:
  Trap() : Object(new NotVisible(), new NotMoveable(), new Solid()) {}
};