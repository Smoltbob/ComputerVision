/*
Demonstrating the usage of unique pointers.
*/

#include <iostream>
#include <memory>
#include <utility>

struct MyInt {
  MyInt(int i) : i_(i) {}

  ~MyInt() { std::cout << "Destroying int " << i_ << std::endl; }

  int i_;
};

int main() {

  // A std::unique_ptr manages automatically and exclusively the lifetime of its
  // resource.
  std::unique_ptr<MyInt> uniquePtr1{new MyInt(1)};

  std::cout << "uniquePtr1.get(): " << uniquePtr1.get() << std::endl;

  // It can be instanciated without resources.
  std::unique_ptr<MyInt> uniquePtr2;
  // It can be moved.
  uniquePtr2 = std::move(uniquePtr1);
  std::cout << "uniquePtr1.get():" << uniquePtr1.get() << std::endl;
  std::cout << "uniquePtr2.get():" << uniquePtr2.get() << std::endl;

  // The underlying resource is deleted when the unique pointer goes out of
  // scope.
  { std::unique_ptr<MyInt> localPtr{new MyInt(2)}; }

  // If the constructor fails when calling new, we can get a memory leak. It's
  // better to use std::make_unique().
  std::unique_ptr<MyInt> uniquePtr3{std::make_unique<MyInt>(3)};
  std::cout << "uniquePtr3.get():" << uniquePtr3.get() << std::endl;
}