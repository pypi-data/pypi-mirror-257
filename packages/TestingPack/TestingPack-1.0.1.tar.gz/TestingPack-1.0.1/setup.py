from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='TestingPack',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    author='Jayesh Vani',
    author_email='jayeshvani2@gmail.com',
    description='A Python package for reading PDF files.',
    ext_modules=cythonize(r"D:\python\New folder\my_extension\TestModule_cython.pyx"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
