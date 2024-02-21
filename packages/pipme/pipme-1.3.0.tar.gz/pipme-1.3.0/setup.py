from setuptools import setup, find_packages

setup(
    name='pipme',
    version='1.3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [ 'pipme = pipme.main:run_cli' ]
    },
    install_requires=[
        'twine>=4.0.2',
        'beautifish>=2.2.1'
    ],
)
