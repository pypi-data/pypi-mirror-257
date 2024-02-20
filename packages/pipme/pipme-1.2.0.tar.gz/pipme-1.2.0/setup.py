from setuptools import setup, find_packages

setup(
    name='pipme',
    version='1.2.0',
    packages=find_packages(),
    install_requires=['os','pipme','ast','requests','subprocess','re','shutil'],
)
    