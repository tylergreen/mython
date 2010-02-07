from distutils.core import setup

setup(name='pyscheme',
      version="1.6",
      description="PyScheme --- a Scheme implementation in Python",
      author="Danny Yoo",
      author_email="dyoo@hkn.eecs.berkeley.edu",
      url="http://hkn.eecs.berkeley.edu/~dyoo/python/pyscheme",
      package_dir =  {'pyscheme': 'src'},
      packages = ['pyscheme'],
      license="MIT License",
      )
