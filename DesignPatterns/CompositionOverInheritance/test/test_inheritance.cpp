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
