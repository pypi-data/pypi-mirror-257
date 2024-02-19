from setuptools import setup, find_packages

setup(
    name='sfutilpsg',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'graphviz'
    ],
    author='mohan chinnappan',
    author_email='mohan.chinnappan.n5@gmail.com',
    description='A utility for managing Salesforce permissions and relationships',
    url='https://github.com/mohan-chinnappan-n/sfutilpsg',
    license='MIT',
)
