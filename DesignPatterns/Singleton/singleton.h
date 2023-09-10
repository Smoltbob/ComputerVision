#ifndef DABF613C_7772_4178_B15E_3974A64956EC
#define DABF613C_7772_4178_B15E_3974A64956EC

#include <string>

/**
 * @brief The aim of the Singleton class is to only allow one instance of it to
 * exist.
 * The class itself is responsible to keep track of its instance. This means
 * that in its constructor it decides wether or not to create a new object.
 */
class Singleton {
public:
  /**
   * @brief Returns an instance of Singleton, guaranteed to be unique.
   *
   * @return Singleton& Unique instance of the class.
   */
  static Singleton &Instance();
  std::string GetValue();

  // Make sure that we cannot instanciate new objects
  Singleton(Singleton const &) = delete;
  void operator=(Singleton const &) = delete;

private:
  // Default constructor is not accessible, so that we are forced to use
  // Instance().
  Singleton(){};
};

#endif /* DABF613C_7772_4178_B15E_3974A64956EC */
