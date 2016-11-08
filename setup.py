#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='GenesysParser',
      version='0.1',
      description='Client to read and parse accession (MCPD passport) information from GENESYS.',
      url='https://github.com/PBR/GenesysParser',
      author='Eliana Papoutsoglou',
      author_email='evangelia.papoutsoglou@wur.nl',
      license='MIT',
      packages=['GenesysParser'],
      install_requires=[
          'requests'
      ],
      include_package_data=True,
      zip_safe=False
)
