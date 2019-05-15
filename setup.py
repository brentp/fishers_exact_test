version = '0.1.5'
import sys
# from setuptools import setup
# from setuptools.extension import Extension
from distutils.core import setup
from distutils.extension import Extension
from distutils.command.bdist import bdist
from distutils.command.build_ext import build_ext
# import setuptools

#from Cython.Distutils import build_ext
# from setuptools.command.build_ext import build_ext
# from setuptools.command. import bdist_wheel
_bdist = bdist
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
      name='fisher',
      version=version,
      description="Fast Fisher's Exact Test",
      url = 'http://github.com/brentp/fishers_exact_test',
      long_description=doc,
      author="haibao tang, brent pedersen",
      author_email="bpederse@gmail.com",
      ext_modules=[ cfisher_ext ],
      cmdclass = {'bdist': _bdist,'build_ext':_build_ext},
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

# For these actions, NumPy is not required. We want them to succeed without,
# for example when pip is used to install seqlearn without NumPy present.

# NO_NUMPY_ACTIONS = ('--help-commands', 'egg_info', '--version', 'clean')
# if not ('--help' in sys.argv[1:]
#         or len(sys.argv) > 1 and sys.argv[1] in NO_NUMPY_ACTIONS):
#     import numpy
#     setup_options['include_dirs'] = [numpy.get_include()]

setup(**setup_options)
