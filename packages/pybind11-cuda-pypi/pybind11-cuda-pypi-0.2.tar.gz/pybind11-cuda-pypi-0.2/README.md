# pybind11-cuda-pypi

Template for a pybind11 CUDA project published on PyPI that installs from source at installation time with `nvcc` and `cmake`

# Install

## Local

Using CMake:

```sh
sh install.sh
python -c "from build.gpu_library import hello; hello()"
```

Using pip:

```sh
pip install .
python -c "from gpu_library import hello; hello()"
```

## [PyPI](https://pypi.org/project/pybind11-cuda-pypi/) (WIP)

```sh
pip install pybind11-cuda-pypi
python -c "from gpu_library import hello; hello()"
```
