# Abstract Factory

## Summary

The abstract factory is a creational design pattern that lets us produce families of related objects without specifying their concrete classes.


## Principle
This pattern lets us define a factory that can build multiple objects of a same variant / family (based on some configuration).

The main idea is to declare interfaces for each distinct product of the family, and then make the variants of these products follow the interfaces.
Then the Abstract Factory is an interface with a list of creation methods for all the products that form a family.
This interface returns abstract product types, so for each variant of product families we need a separate factory class that returns products of a particular kind.