#include <iostream>

// Defining some properties. They should be in their own headers.
class Object
{
    public:
        virtual void update() {}
        virtual void draw() {}
        virtual void collide(Object objects[]) {}
};

class Visible : virtual public Object
{
    public:
        virtual void draw() override
        {
            // Code to draw a model
            std::cout << "Hello! I am visible." << std::endl;
        }
};

class Solid : virtual public Object
{
    public:
        virtual void collide(Object objects[]) override
        {
            std::cout << "Booom!" << std::endl;
        }
};

class Movable : virtual public Object
{
    public:
        virtual void update() override
        {
            std::cout << "Moving..." << std::endl;
        }
};

// Using the properties to define behaviors in new classes
// We need virtual inheritance to avoid creating multiple copies of the base class.
class Player: virtual public Solid, virtual public Movable, virtual public Visible
{};

// The cloud is not solid, implicitly through the base Object class
class Cloud: virtual public Movable, virtual public Visible
{};

// The building is  not movable, implicitly through the base Object class
class Building: virtual public Solid, virtual public Visible
{};

// The trap ie neither visible or movable
class Trap: virtual public Solid
{};

int main ()
{
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