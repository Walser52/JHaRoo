from setuptools import setup

setup(
    name='jhr',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for scientific computing with MPI and NumPy',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/yourusername/abinit',
    license='MIT',
    install_requires=[
        # Add runtime dependencies, e.g.:
        # 'numpy',
        # 'mpi4py',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

