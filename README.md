# ComputerVision

# How to use Bazel
1. Add your pip requirements in `requirements.in`
2. Run `bazel run requirements.update` this will trigger the `compile_pip_requirements` function in BUILD.bazel. This then builds the `requirements.txt` file, that will be used by other targets with the `requirement()` functionn.