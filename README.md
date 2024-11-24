# ComputerVision

## Core Guidelines

1. Write readable code and explicit the algorithms.
1. Document first.
1. Reuse code.

### Additional rules

4. Geometric primitives should have their own class that carry semantic values.
   1. 2D Inhomogeous point, called Point
   1. 3D Inhomogeneous point, called Point3D
   1. 2D Homogeneous point, also Point3D. We ensure homogeneity through post / pre conditions.

## Interfaces

Each class / method has an low-level array in / out. On top of it, we build an interface that deals with geometric concepts (points, etc) and passes them down as arrays.

# How to use Bazel

1. Add your pip requirements in `requirements.in`
1. Run `bazel run requirements.update` this will trigger the `compile_pip_requirements` function in BUILD.bazel. This then builds the `requirements.txt` file, that will be used by other targets with the `requirement()` function.

# Docker

There is a `Docker` folder with a docker file for running prechecks (code formatting, linting etc).

## How To Use
Setup
```
sudo docker build -t linter Docker/
```

Run (from repo root)
```
sudo docker run -v ${PWD}:/app linter
```


# Dependencies

- Docker
- Bazel
