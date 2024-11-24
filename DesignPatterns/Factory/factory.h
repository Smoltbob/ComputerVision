// Product
// Note: we define the virtual destructor to make sure that the derived
// constructor will be called when deleting a derived class through a base
// pointer. Without it, only the base destructor would be called.
// https://stackoverflow.com/questions/461203/when-to-use-virtual-destructors
class Window {
public:
  virtual ~Window(){};
};

// Concrete Product
class DefaultWindow : public Window {};

class FancyWindow : public Window {};
