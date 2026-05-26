import numpy
from Cython.Build import cythonize
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

import versioneer


class _build_ext(build_ext):
    """build_ext command for use when numpy and Cython are needed.

    https://stackoverflow.com/a/42163080/8083313

    """

    def run(self):
        # Cythonize the extension (and path the `_needs_stub` attribute,
        # which is not set by Cython but required by `setuptools`)
        self.extensions = cythonize(self.extensions, force=self.force)
        for extension in self.extensions:
            extension._needs_stub = False

        # Call original build_ext command
        build_ext.run(self)


cfisher_ext = Extension(
    "fisher.cfisher",
    ["src/cfisher.pyx"],
    extra_compile_args=["-O3"],
    include_dirs=[numpy.get_include()],
)
cmdclass = {"build_ext": _build_ext}
cmdclass.update(versioneer.get_cmdclass())

setup(
    version=versioneer.get_version(),
    ext_modules=[cfisher_ext],
    cmdclass=cmdclass,
)
