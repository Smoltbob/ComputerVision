load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    sha256 = "a868059c8c6dd6ad45a205cca04084c652cfe1852e6df2d5aca036f6e5438380",
    strip_prefix = "rules_python-0.14.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.14.0.tar.gz",
)

# Only needed for PIP support:
load("@rules_python//python:pip.bzl", "pip_parse")

# Requirements for notebooks
pip_parse(
    name = "notebooks",
    requirements = "//:requirements.txt"
)

load(
    "@notebooks//:requirements.bzl",
    "install_deps"
)
install_deps()


# Setup pybind
load("@rules_python//python:repositories.bzl", "python_register_toolchains")

# If running from outside (via ./bazel-bin/...), the env and bazel python versions must match
python_register_toolchains(
    name = "python39",
    # Available versions are listed in @rules_python//python:versions.bzl.
    # We recommend using the same version your team is already standardized on.
    python_version = "3.9",
)
load("@python39//:defs.bzl", "interpreter")


http_archive(
  name = "pybind11_bazel",
  strip_prefix = "pybind11_bazel-faf56fb3df11287f26dbc66fdedf60a2fc2c6631",
  urls = ["https://github.com/pybind/pybind11_bazel/archive/faf56fb3df11287f26dbc66fdedf60a2fc2c6631.zip"],
)
# We still require the pybind library.
http_archive(
  name = "pybind11",
  build_file = "@pybind11_bazel//:pybind11.BUILD",
  strip_prefix = "pybind11-2.10.3",
  urls = ["https://github.com/pybind/pybind11/archive/v2.10.3.tar.gz"],
)
load("@pybind11_bazel//:python_configure.bzl", "python_configure")
python_configure(name = "local_config_python", python_interpreter_target = interpreter) # interpreter is required so that py_library() gets a PyInfo