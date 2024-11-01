#include <iostream>

// Defining some properties. They should be in their own headers.
class Object
{
    public:
        virtual void update() {}
        virtual void draw() {}
        virtual void collide(Object objects[]) {}
};

class Visible : public Object
{
    public:
        virtual void draw() override
        {
            // Code to draw a model
            std::cout << "Hello! I am visible." << std::endl;
        }
};

class Solid : public Object
{
    public:
        virtual void collide(Object objects[]) override
        {
            std::cout << "Booom!" << std::endl;
        }
};

class Movable : public Object
{
    public:
        virtual void update() override
        {
            std::cout << "Moving..." << std::endl;
        }
};

// Using the properties to define behaviors in new classes


int main ()
{
    std::cout << "Running the inheritance demo program" << std::endl;
}