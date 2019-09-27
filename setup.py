import sys

import versioneer
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


class _build_ext(build_ext):
    """build_ext command for use when numpy headers are needed.

    https://stackoverflow.com/a/42163080/8083313
    """

    def run(self):

        # Import numpy here, only when headers are needed
        import numpy

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Call original build_ext command
        build_ext.run(self)


doc = open("README.md").read()
cfisher_ext = Extension("fisher.cfisher", ["src/cfisher.c"], extra_compile_args=["-O3"])
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
    setup_requires=["numpy"],
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
