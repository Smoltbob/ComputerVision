#include "DesignPatterns/CompositionOverInheritance/inheritance.h"
#include <gtest/gtest.h>

TEST(InheritanceTest, PlayerTest) {
  Player my_player{};
  EXPECT_EQ(my_player.draw(), "Hello! I am visible.");
  EXPECT_EQ(my_player.collide(&my_player), "Booom!");
  EXPECT_EQ(my_player.update(), "Moving...");
}

TEST(InheritanceTest, CloudTest) {
  Cloud my_cloud{};
  EXPECT_EQ(my_cloud.draw(), "Hello! I am visible.");
  EXPECT_EQ(my_cloud.collide(&my_cloud), "");
  EXPECT_EQ(my_cloud.update(), "Moving...");
}

TEST(InheritanceTest, BuildingTest) {
  Building my_building{};
  EXPECT_EQ(my_building.draw(), "Hello! I am visible.");
  EXPECT_EQ(my_building.collide(&my_building), "Booom!");
  EXPECT_EQ(my_building.update(), "");
}

TEST(InheritanceTest, TrapTest) {
  Trap my_trap{};
  EXPECT_EQ(my_trap.draw(), "");
  EXPECT_EQ(my_trap.collide(&my_trap), "Booom!");
  EXPECT_EQ(my_trap.update(), "");
}
