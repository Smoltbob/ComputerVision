#include "DesignPatterns/CompositionOverInheritance/inheritance.h"
#include <iostream>

int main() {
  std::cout << "Running the inheritance demo program" << std::endl;

  std::cout << "Instantiating player:" << std::endl;
  Player my_player{};
  std::cout << my_player.update() << std::endl;
  std::cout << my_player.collide(&my_player) << std::endl;
  std::cout << my_player.draw() << std::endl;

  std::cout << "Instantiating cloud:" << std::endl;
  Cloud my_cloud{};
  std::cout << my_cloud.update() << std::endl;
  std::cout << my_cloud.collide(&my_player)
            << std::endl; // There will be no collision
  std::cout << my_cloud.draw() << std::endl;

  std::cout << "Instantiating building:" << std::endl;
  Building my_building{};
  std::cout << my_building.update() << std::endl; // There will be no move
  std::cout << my_building.collide(&my_player) << std::endl;
  std::cout << my_building.draw() << std::endl;

  std::cout << "Instantiating trap:" << std::endl;
  Trap my_trap{};
  std::cout << my_trap.update() << std::endl; // There will be no move
  std::cout << my_trap.collide(&my_player) << std::endl;
  std::cout << my_trap.draw() << std::endl; // There will be no draw
}