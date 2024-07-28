from setuptools import setup, find_packages

setup(
    name='bands',
    version='0.1',
    packages=find_packages(include=['my_namespace', 'my_namespace.*']),
    namespace_packages=['my_namespace'],
    install_requires=['numpy', 'matplotlib', 'cycler',], 
)