#!/usr/bin/env python
import sys, os
from distutils.core import setup
from distutils.command.install_data import install_data

class install_sitepackages(install_data):
    def finalize_options(self):
        self.warn_dir = 0
        if os.sep == '/':
            self.install_dir = os.path.join(sys.prefix, "lib", 
                                            "python"+sys.version[:3],
                                            "site-packages")
        else:
            self.install_dir = os.path.join(sys.prefix, "lib", "site-packages")

setup(name='pypissh',
      version='1.1',
      description='PyPI SSH Access',
      long_description=open("README").read(),
      author='Martin v. Loewis',
      author_email='martin@v.loewis.de',
      url='http://pypi.python.org/pypi/pypissh',
      py_modules=['pypissh'],
      data_files=['pypissh.pth'],
      cmdclass = {'install_data':install_sitepackages},
     )
