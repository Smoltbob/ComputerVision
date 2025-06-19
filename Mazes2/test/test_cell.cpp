#include <gtest/gtest.h>

// Example test case
TEST(CellTest, ExampleTest)
{
    int a = 1;
    int b = 1;
    EXPECT_EQ(a, b); // Test that a equals b
}

// Main function for running all tests
int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}