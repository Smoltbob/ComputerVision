load("@pybind11_bazel//:build_defs.bzl", "pybind_extension")
load("@rules_python//python:defs.bzl", "py_library")

def pybind_module(name, srcs, visibility, imports = [], deps = [], linkopts = []):
    """
    Build a py library out of a pybind extension *.so
    """
    pybind_extension(
        name = name,
        srcs = srcs,
        deps = deps
    )

    py_library(
        name = name,
        data = [name + ".so"],
        visibility = visibility,
    )