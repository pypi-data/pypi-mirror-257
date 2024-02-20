from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION= 'DetSpace package module'
LONG_DESCRIPTION = 'DetSpace package with all functions needed to obtain the data. Generate new metabolites, clean the results and SMILE comparison'

# Setting up
setup(
      name='detspace',
      version=VERSION,
      author='Hèctor Martín',
      autor_email='hector61198@gmail.com',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      install_requieres=[],
      
      keywords=['python', 'metabolic expasion'],
      classifiers= [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Operating System :: Microsoft'])