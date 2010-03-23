from distutils.core import setup, Extension
import numpy as np
#from Cython.Distutils import build_ext

version = '0.1.1'

doc = open('README.rst').read()
cfisher_ext = Extension('fisher/cfisher', ['src/cfisher.c'], include_dirs=[np.get_include()])


setup(name='fisher',
      version=version,
      description="Fast Fisher's Exact Test",
      url = 'http://github.com/brentp/fishers_exact_test',
      long_description=doc,
      author="haibao tang, brent pedersen",
      author_email="bpederse@gmail.com",
      ext_modules=[ cfisher_ext ],
      requires=['numpy'],
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
      ],
)
