import sys
from setuptools import setup
from setuptools.extension import Extension

version = '0.1.5'

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
      install_requires=['numpy'],
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
NO_NUMPY_ACTIONS = ('--help-commands', 'egg_info', '--version', 'clean')
if not ('--help' in sys.argv[1:]
        or len(sys.argv) > 1 and sys.argv[1] in NO_NUMPY_ACTIONS):
    import numpy
    setup_options['include_dirs'] = [numpy.get_include()]

setup(**setup_options)
