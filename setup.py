import sys
from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext

version = '0.1.5'

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
        


doc = open('README.rst').read()
cfisher_ext = Extension('fisher.cfisher',
                        ['src/cfisher.c'],
                        extra_compile_args=["-O3"])


setup_options = dict(
      name='fisher-modified',
      version=version,
      description="Forked from fisher (https://github.com/brentp/fishers_exact_test). Recompile it with Cython 0.29.4 to be compatible with Python 3.7.",
      url = 'https://github.com/lilab-bcb/fishers_exact_test',
      long_description=doc,
      author="haibao tang, brent pedersen; Bo Li",
      author_email="bli28@mgh.harvard.edu",
      ext_modules=[ cfisher_ext ],
      cmdclass = {'build_ext':_build_ext},
#       install_requires=['numpy'],
      setup_requires=['numpy'],
      keywords='statistics cython',
      license='BSD',
      packages=['fisher'],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
      ],
)

setup(**setup_options)
