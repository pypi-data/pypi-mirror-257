from distutils.extension import Extension

import numpy
from Cython.Build import cythonize
from setuptools import setup

define_macros = [
    ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
    ("NPY_TARGET_VERSION", "NPY_1_18_API_VERSION"),
]

setup(
    ext_modules=cythonize(
        [
            Extension(
                "lick._vendor.vectorplot.core",
                ["src/lick/_vendor/vectorplot/core.pyx"],
                include_dirs=[numpy.get_include()],
                define_macros=define_macros,
            ),
        ],
        compiler_directives={"language_level": 3},
    ),
)
