#ifndef DABF613C_7772_4178_B15E_3974A64956EC
#define DABF613C_7772_4178_B15E_3974A64956EC

#include <string>

class Singleton {
public:
  static Singleton *Instance();
  std::string GetValue();

protected:
  Singleton(){};

private:
  static Singleton *instance_;
};

#endif /* DABF613C_7772_4178_B15E_3974A64956EC */
