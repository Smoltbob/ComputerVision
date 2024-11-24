# The Factory Method
The factory method provides an interface for creating objects. Different implementations of that interface allow creating different objects (but they should all implement the interface and nothing else).
Then a creator class depends on this interface, and different creator subclasses will be used to create different products according to the interfaces aforementioned.
- https://en.wikipedia.org/wiki/Factory_method_pattern
- https://refactoring.guru/design-patterns/factory-methodhttps://refactoring.guru/design-patterns/factory-method

In other words, the factory method defines an interface to create a single object but lets subclasses decide which objects to create. The interface can provide a default implementation for creating objects.
Reference:
- https://www.modernescpp.com/index.php/factory-method/
- https://www.modernescpp.com/index.php/factory-method-2/

Therefore we have two "families" of classes:
- The Product class 
    - From which the Concrete Product inherits.
- The Creator, which defines the factory method.
    - From which the Concrete Creator inherits and overwrites the factory method.