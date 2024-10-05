from setuptools import setup, find_packages

setup(
    name='jhr',
    version='0.0.1',
    description='Codes for many body systems',
    author='EPR-copenhagen, Walser52',
    author_email='myemail@email.com, walser52@github.com',
    install_requires=['numpy', 'matplotlib', 'pandas', 'cycler'], 

    packages=find_packages(include=['my_namespace', 'my_namespace.*']),
    namespace_packages=['my_namespace'],
    

)
