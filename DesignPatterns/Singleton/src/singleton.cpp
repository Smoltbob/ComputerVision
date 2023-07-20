#include "DesignPatterns/Singleton/singleton.h"

Singleton *Singleton::instance_ = nullptr;

std::string Singleton::GetValue() {
  std::string res = "value";
  return res;
}

Singleton *Singleton::Instance() {
  if (instance_ == nullptr) {
    instance_ = new Singleton;
  }
  return instance_;
};