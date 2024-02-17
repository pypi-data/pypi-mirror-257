from distutils.core import setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# setup function
setup(
    name = 'mydatau',
    packages = ['mydatau'],
    version = '0.0.4',
    license = 'MIT',
    description = 'Expandable module of statistical data utilities',
    long_description=long_description,
    author = 'econcz',
    author_email = '29724411+econcz@users.noreply.github.com',
    url = 'https://github.com/econcz/mydatau',
    download_url = 'https://github.com/econcz/mydatau/archive/pypi-0_0_4.tar.gz',
    keywords = [
        'statistical data', 'utilities', 'Jupyter', 'R', 'Stata', 'Julia',
        'GAMS', 'AMPL', 'Octave', 'Matlab'
    ],
    install_requires = ['stata-kernel', 'r2py', 'oct2py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
  ],
)
