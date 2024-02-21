from setuptools import setup, find_packages


setup(
   name='BIOViewer',
   version='0.1.3',
   description='A useful module to display time series biosignals',
   long_description='this module contains a lightweight viewer that is used to display biosignals',
   author='Moritz Alkofer', 
   packages=find_packages(),
   include_package_data=True,
   install_requires=[], #list dependencies
)