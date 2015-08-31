from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='chromaway.regtestcontroller',
        entry_points={'console_scripts':
                    [
                        'server = chromaway.regtestcontroller.scripts.server:main',
                        'abe = chromaway.regtestcontroller.scripts.abe:main',
                    ]
                    }
      )
