#!/usr/bin/env python
# ----------------------------------------------------------------------------
# PyGMTSAR
# 
# This file is part of the PyGMTSAR project: https://github.com/mobigroup/gmtsar
# 
# Copyright (c) 2024, Alexey Pechnikov
# 
# Licensed under the BSD 3-Clause License (see LICENSE for details)
# ----------------------------------------------------------------------------

from setuptools import setup
import urllib.request

def get_version():
    with open("pygmtsar/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split('=')[1]
                version = version.replace("'", "").replace('"', "").strip()
                return version

# read the contents of local README file
#from pathlib import Path
#this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

upstream_url = 'https://raw.githubusercontent.com/AlexeyPechnikov/pygmtsar/pygmtsar2/README.md'
response = urllib.request.urlopen(upstream_url)
long_description = response.read().decode('utf-8')

setup(
    name='pygmtsar',
    version=get_version(),
    description='PyGMTSAR (Python GMTSAR): Powerful and Accessible Satellite Interferometry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AlexeyPechnikov/gmtsar',
    author='Alexey Pechnikov',
    author_email='alexey@pechnikov.dev',
    license='BSD-3-Clause',
    packages=['pygmtsar'],
    install_requires=['xarray>=2024.1.0',
                      'numpy>=1.22.4',
                      'numba',
                      'pandas>=2.2',
                      'geopandas',
                      'distributed>=2024.1.0',
                      'dask[complete]',
                      'dask_image',
                      'joblib',
                      'tqdm',
                      'scipy>=1.12.0',
                      'shapely>=2.0.2',
                      'scikit-learn',
                      'xmltodict',
                      'rioxarray',
                      'ipywidgets',
                      'h5netcdf>=1.3.0',
                      'h5py',
                      'nc-time-axis',
                      'statsmodels>=0.14.0',
                      'pygmt',
                      'remotezip',
                      'asf_search',
                      'imageio',
                      'matplotlib',
                      'adjustText',
                      'seaborn',
                      'vtk',
                      'panel'
                      ],
#    extras_require={
#                      'vtk_support': ['vtk', 'panel']
#    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    python_requires='>=3.10'
)
