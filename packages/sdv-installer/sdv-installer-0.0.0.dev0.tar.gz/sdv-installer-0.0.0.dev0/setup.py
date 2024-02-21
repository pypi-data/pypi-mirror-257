from setuptools import setup
from Cython.Build import cythonize


setup(
    name = 'sdv-installer',
    ext_modules = cythonize(["**/*.pyx"]),
    version='0.0.0.dev0',
)