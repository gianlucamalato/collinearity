#from distutils.core import setup
from setuptools import setup, Extension

with open('README.md') as f:
    long_description = f.read()


setup(
  name = 'collinearity',         # How you named your package folder (MyLib)
  packages = ['collinearity'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python library for removing collinearity in machine learning datasets',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  
  author = 'Gianluca Malato',                   # Type in your name
  author_email = 'gianluca.malato@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/gianlucamalato/collinearity',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gianlucamalato/collinearity/archive/refs/tags/0.6.tar.gz',    # I explain this later on
  keywords = ['machine learning', 'collinearity', 'supervised models'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scikit-learn',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)