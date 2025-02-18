#include <iostream>

// Product.
// Define an interface class using pure virtual functions.
class Window {
public:
  Window() = default;
  Window(const Window &) = delete;
  Window &operator=(const Window &) = delete;
  virtual Window *create() = 0;
  virtual ~Window(){};
};

// Concrete Products.
// Here we implement the different constructors.
class DefaultWindow : public Window {
  DefaultWindow *create() override {
    std::cout << "Create DefaultWindow" << std::endl;
    return new DefaultWindow();
  }
};

class FancyWindow : public Window {
  FancyWindow *create() override {
    std::cout << "Create FancyWindow" << std::endl;
    return new FancyWindow();
  }
};

// Concrete Creator using dynamic dispatch
// It uses the type of window provided as parameter
// as a "switch" for selecting the correct constructor
Window *createWindow(Window &window) { return window.create(); }

int main() {
  DefaultWindow defaultWindow;
  FancyWindow fancyWindow;

  const Window *defaultWindow1 = createWindow(defaultWindow);
  const Window *fancyWindow1 = createWindow(fancyWindow);

  delete defaultWindow1;
  delete fancyWindow1;
}