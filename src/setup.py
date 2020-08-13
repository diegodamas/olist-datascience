from distutils.core import setup
import os
import setuptools

#From lib install setup.py -> pip install src/.
#From requiriments (pip install pipreqs) -> pipreqs ./

setup(
    name = 'olistlib',
    version = '0.1',
    description = 'Library for the project',
    author = 'Diego Damas Puglia',
    author_email = 'diegodamas2011@gmail.com',
    packages = setuptools.find_packages()  
)