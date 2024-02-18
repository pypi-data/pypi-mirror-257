# En setup.py

from setuptools import setup, find_packages

setup(
    name='GTDMfunctions',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'sympy',
        'matplotlib'
        # Otras dependencias de tu biblioteca
    ],
)
