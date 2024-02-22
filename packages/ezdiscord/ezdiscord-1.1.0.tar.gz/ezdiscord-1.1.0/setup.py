from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  long_description=open('README.rst').read(),
  name='ezdiscord',
  version='1.1.0',
  description='Made discord.py easier.',
  url='',  
  author='Karmin',
  license='MIT', 
  classifiers=classifiers,
  keywords='Made discord.py easier.',
  packages=find_packages(),
  install_requires=['os', 'discord.py'] 
)