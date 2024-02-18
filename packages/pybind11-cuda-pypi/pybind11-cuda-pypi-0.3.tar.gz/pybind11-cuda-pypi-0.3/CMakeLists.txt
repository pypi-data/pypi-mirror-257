cmake_minimum_required(VERSION 3.12)
project(pybind11_cuda_project)

# Find CUDA
find_package(CUDA REQUIRED)
include_directories(${CUDA_INCLUDE_DIRS})
link_directories(${CUDA_LIBRARY_DIRS})

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
include_directories(${Python3_INCLUDE_DIRS})  # Correct variable for Python include dirs

# Pybind11
add_subdirectory(pybind11)
include_directories(./pybind11/include)

# Set C++11 standard
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# CUDA library
cuda_add_library(gpu_library SHARED gpu_library.cu)
target_link_libraries(gpu_library ${Python3_LIBRARIES} ${CUDA_LIBRARIES} pybind11::module)  # Correct variable for Python libraries

set_target_properties(gpu_library PROPERTIES PREFIX "")
