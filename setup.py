from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("map_speed/map_speed_c_ver.pyx"),
)
