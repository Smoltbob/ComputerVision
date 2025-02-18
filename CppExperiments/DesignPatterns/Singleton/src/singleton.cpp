#include "DesignPatterns/Singleton/singleton.h"

std::string Singleton::GetValue() {
  std::string res = "value";
  return res;
}

Singleton &Singleton::Instance() {
  static Singleton instance;
  return instance;
};