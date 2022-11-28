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