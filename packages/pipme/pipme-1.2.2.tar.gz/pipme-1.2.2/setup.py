from setuptools import setup, find_packages

setup(
    name='pipme',
    version='1.2.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [ 'pipme = pipme.main:run_cli' ]
    },
    install_requires=[
        
    ],
)
