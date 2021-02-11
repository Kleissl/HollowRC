from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name='HollowRC',
      version='1.5',
      description='HollowRC',
      author='Kenneth C. Kleissl',
      packages=['HollowRC'],
      install_requires=install_requires,
      zip_safe=False)
