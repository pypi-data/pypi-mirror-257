from setuptools import setup

setup(
   name='avrami',
   version='1.0',
   description='Module for surface nucleation measuremnts',
   author='Simona Buzzi',
   author_email='s.buzzi@tue.nl',
   packages=['avrami'],  
   install_requires=['numpy', 'scipy', 'pandas', 'matplotlib'], #external packages as dependencies
    entry_points = {         
      'console_scripts': ['avrami_fit=avrami.main:avrami_data_process'],
  }
)