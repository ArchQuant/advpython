# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Hello",
    ext_modules=cythonize(["hello.pyx", "cevolve.pyx", "mathlib.pyx", "distance.pyx"]),
)
