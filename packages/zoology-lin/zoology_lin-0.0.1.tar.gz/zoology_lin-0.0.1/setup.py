from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r" , encoding="utf-8") as f:
    long_description = f.read()
    setup(
        name='zoology_lin',
        version='0.0.1',
        description='A zoology library for company',
        long_description=long_description,
        author='phailin',
        author_email='phailin791@hotmail.com',
        url='https://github.com/phailin/zoology_lin',
        install_requires=[],
        license='MIT',
        packages=find_packages(),
        platforms=["all"],
        classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Software Development :: Libraries'
        ],
    )