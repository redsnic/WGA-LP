import setuptools

setuptools.setup(
   name='WGALP',
   version='0.99',
   description='A simple tool to create bash pipeline in python for WGA and other applications',
   author='Nicolò Rossi',
   author_email='olocin.issor@gmail.com',
   install_requires=['wheel', 'pandas'],
   packages=setuptools.find_packages()
)