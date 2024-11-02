#include "DesignPatterns/CompositionOverInheritance/inheritance.h"
#include <iostream>

int main() {
  std::cout << "Running the inheritance demo program" << std::endl;

  std::cout << "Instantiating player:" << std::endl;
  Player my_player{};
  my_player.update();
  my_player.collide(&my_player);
  my_player.draw();

  std::cout << "Instantiating cloud:" << std::endl;
  Cloud my_cloud{};
  my_cloud.update();
  my_cloud.collide(&my_player); // There will be no collision
  my_cloud.draw();

  std::cout << "Instantiating building:" << std::endl;
  Building my_building{};
  my_building.update(); // There will be no move
  my_building.collide(&my_player);
  my_building.draw();

  std::cout << "Instantiating trap:" << std::endl;
  Trap my_trap{};
  my_trap.update(); // There will be no move
  my_trap.collide(&my_player);
  my_trap.draw(); // There will be no draw
}