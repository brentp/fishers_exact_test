import sys

import versioneer
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


class _build_ext(build_ext):
    """build_ext command for use when numpy and Cython are needed.

    https://stackoverflow.com/a/42163080/8083313

    """

    def run(self):
        # Only resolve imports when they are absolutely needed
        import numpy
        from Cython.Build import cythonize

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Cythonize the extension (and path the `_needs_stub` attribute,
        # which is not set by Cython but required by `setuptools`)
        self.extensions = cythonize(self.extensions, force=self.force)
        for extension in self.extensions:
            extension._needs_stub = False

        # Call original build_ext command
        build_ext.run(self)


doc = open("README.md").read()
cfisher_ext = Extension("fisher.cfisher", ["src/cfisher.pyx"], extra_compile_args=["-O3"])
cmdclass = {"build_ext": _build_ext}
cmdclass.update(versioneer.get_cmdclass())


setup_options = dict(
    name="fisher",
    version=versioneer.get_version(),
    description="Fast Fisher's Exact Test",
    url="http://github.com/brentp/fishers_exact_test",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="Haibao Tang, Brent Pedersen",
    author_email="bpederse@gmail.com",
    ext_modules=[cfisher_ext],
    cmdclass=cmdclass,
    #       install_requires=['numpy'],
    setup_requires=["numpy", "cython"],
    keywords="statistics cython",
    license="BSD",
    packages=["fisher"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

setup(**setup_options)
