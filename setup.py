from setuptools import setup, find_packages

setup(
    name='vib_analysis',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'ase',
        'cclib',
    ],
    entry_points={
        'console_scripts': [
            'vib_analysis = vib_analysis.cli:main',
        ],
    },
    author='Dr Alister Goodfellow',
    url="https://github.com/aligfellow/vib_analysis",
    description='A package for analyzing internal coordinate changes from vibrational mode trajectories.',

)
