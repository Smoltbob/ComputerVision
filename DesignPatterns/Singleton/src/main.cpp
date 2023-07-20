#include "DesignPatterns/Singleton/singleton.h"
#include <ctime>
#include <iostream>
#include <string>

std::string get_greet(const std::string &who) { return "Hello " + who; }

void print_localtime() {
  std::time_t result = std::time(nullptr);
  std::cout << std::asctime(std::localtime(&result));
}

int main(int argc, char **argv) {
  std::string who = "world";
  if (argc > 1) {
    who = argv[1];
  }
  std::cout << get_greet(who) << std::endl;
  print_localtime();

  Singleton *tmp = Singleton::Instance();
  std::cout << tmp->GetValue() << '\n';
  return 0;
}